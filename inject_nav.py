# -*- coding: utf-8 -*-
"""给课程全部 HTML 页面注入全局目录抽屉（纯 CSS checkbox 驱动）。"""
import re, sys

D = r"C:\workspace\crypto-learning\wallet-dev-learning"

GROUPS = [
    ("总站", [("index.html", "课程目录（门户）"), ("overview.html", "系列总览（速查版）")]),
    ("公共基础", [("00-common.html", "篇 00 · 密码学 / HD 钱包 / 签名")]),
    ("Bitcoin", [("01-btc.html", "篇 01 · BTC 概念与钱包"),
                 ("02-btc-script.html", "篇 02 · 脚本与交易编程"),
                 ("03-btc-ecosystem.html", "篇 03 · 生态与 BTCfi")]),
    ("Ethereum", [("04-eth.html", "篇 04 · ETH 概念与钱包"),
                  ("05-solidity.html", "篇 05 · Solidity 合约语法"),
                  ("06-eth-defi.html", "篇 06 · DeFi 原理与实战")]),
    ("Solana", [("07-sol.html", "篇 07 · SOL 概念与钱包"),
                ("08-sol-anchor.html", "篇 08 · Rust 与 Anchor 合约"),
                ("09-sol-defi.html", "篇 09 · SOL DeFi 实战")]),
    ("TRON", [("10-tron.html", "篇 10 · TRON 概念与钱包"),
              ("11-tron-tvm.html", "篇 11 · TVM 合约开发"),
              ("12-tron-defi.html", "篇 12 · DeFi 与 USDT 支付")]),
    ("Sui", [("13-sui.html", "篇 13 · SUI 概念与钱包"),
             ("14-sui-move.html", "篇 14 · Move 合约开发"),
             ("15-sui-defi.html", "篇 15 · SUI DeFi 实战")]),
]

DRAWER_CSS = """
<style id="nav-drawer-css">
.nav-toggle{display:none}
.nav-fab{position:fixed;right:22px;bottom:22px;z-index:90;background:#2563eb;color:#fff;padding:10px 18px;border-radius:999px;box-shadow:0 4px 14px rgba(37,99,235,.35);cursor:pointer;font-size:13.5px;font-weight:600;user-select:none}
.nav-fab:hover{background:#1d4ed8}
.nav-mask{position:fixed;inset:0;background:rgba(15,23,42,.35);z-index:98;opacity:0;pointer-events:none;transition:opacity .2s}
.nav-drawer{position:fixed;top:0;right:-330px;width:300px;max-width:85vw;height:100vh;background:#fff;z-index:99;box-shadow:-4px 0 24px rgba(15,23,42,.15);transition:right .25s;overflow-y:auto;padding-bottom:30px}
.nav-toggle:checked~.nav-drawer{right:0}
.nav-toggle:checked~.nav-mask{opacity:1;pointer-events:auto}
.nav-drawer-head{position:sticky;top:0;background:#fff;z-index:1;display:flex;justify-content:space-between;align-items:center;padding:14px 18px;border-bottom:1px solid #e4e7ee;font-size:14px}
.nav-close{cursor:pointer;font-size:20px;color:#8a92a6;padding:0 6px;line-height:1}
.nav-close:hover{color:#2563eb}
.nav-drawer .nav-group{font-size:11px;color:#8a92a6;letter-spacing:.08em;font-weight:700;padding:14px 18px 4px;text-transform:uppercase;margin:0}
.nav-drawer nav a{display:block;padding:7px 18px;font-size:13px;color:#4a5265;text-decoration:none}
.nav-drawer nav a:hover{background:#eef4ff;color:#2563eb}
.nav-drawer nav a.cur{background:#eef4ff;color:#2563eb;font-weight:600;border-left:3px solid #2563eb;padding-left:15px}
</style>
"""

def build_drawer(cur):
    h = ['<input type="checkbox" id="nav-toggle" class="nav-toggle">',
         '<label for="nav-toggle" class="nav-fab" title="打开全站目录">&#9776; 全部目录</label>',
         '<label for="nav-toggle" class="nav-mask"></label>',
         '<div class="nav-drawer">',
         '<div class="nav-drawer-head"><b>系列教程目录</b><label for="nav-toggle" class="nav-close">&times;</label></div>',
         '<nav>']
    for gname, items in GROUPS:
        h.append(f'<div class="nav-group">{gname}</div>')
        for fn, t in items:
            cls = ' class="cur"' if fn == cur else ''
            h.append(f'<a href="{fn}"{cls}>{t}</a>')
    h.append('</nav></div>')
    return "\n".join(h)

files = ["index.html", "overview.html"] + [fn for _, items in GROUPS for fn, _ in items if fn not in ("index.html", "overview.html")]

changed, skipped = [], []
for fn in files:
    path = D + "\\" + fn
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "nav-drawer" in content:
        skipped.append(fn)
        continue
    drawer = build_drawer(fn)
    # overview.html 未引用外部样式表，需内联抽屉 CSS
    if "assets/style.css" not in content:
        content = content.replace("</head>", DRAWER_CSS + "\n</head>", 1)
    content, n = re.subn(r"<body[^>]*>", lambda m: m.group(0) + "\n" + drawer, content, count=1)
    if n == 0:
        skipped.append(fn + "(no <body>)")
        continue
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    changed.append(fn)

print("changed:", len(changed))
for c in changed:
    print("  +", c)
print("skipped:", skipped)
