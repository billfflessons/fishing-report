import re, sys, html as H
from playwright.sync_api import sync_playwright
src=open(sys.argv[1]).read(); out=sys.argv[2]
date=re.search(r'Weekend of ([^<·]*)',src).group(1).strip()
texts=[H.unescape(t).strip() for t in re.findall(r'>([^<>]{2,120})</',src)]
cards=[]
for i,t in enumerate(texts):
    if t=='Flies' and i>=2: cards.append((texts[i-2],texts[i-1]))
best=cards[0]; rest=cards[1:5]
rows=''.join(f'<div class="row"><div class="tag">{H.escape(t)}</div><div class="nm">{H.escape(n)}</div></div>' for t,n in rest)
page=f'''<html><head><style>
body{{margin:0;width:1080px;height:1350px;font-family:Georgia,serif;background:#f3eee6;color:#1d1d1d}}
.top{{background:#111;color:#fff;padding:48px 64px 40px}}
.brand{{font:700 30px Georgia;letter-spacing:1px}} .brand small{{display:block;font:600 18px Arial;letter-spacing:4px;color:#7fc3cf;margin-top:6px}}
h1{{font:700 70px Georgia;margin:44px 0 8px;line-height:1.05}}
.date{{font:500 30px Arial;color:#9fd3dc}}
.best{{margin:44px 64px 0;background:#fff;border-left:14px solid rgb(46,125,138);padding:34px 40px;border-radius:8px}}
.best .tag{{font:700 24px Arial;color:#8d372a;letter-spacing:2px;text-transform:uppercase}}
.best .nm{{font:700 58px Georgia;margin-top:10px}}
.best .sub{{font:500 28px Arial;color:#555;margin-top:8px}}
.list{{margin:28px 64px 0}}
.row{{display:flex;justify-content:space-between;align-items:baseline;border-bottom:2px solid #d9d0c2;padding:22px 4px}}
.row .nm{{font:700 38px Georgia}} .row .tag{{font:600 24px Arial;color:rgb(46,125,138);order:2;text-align:right;max-width:46%}}
.foot{{position:absolute;bottom:0;left:0;right:0;background:rgb(46,125,138);color:#fff;padding:34px 64px;font:600 30px Arial}}
.foot b{{display:block;font:700 36px Georgia;margin-bottom:6px}}
</style></head><body>
<div class="top"><div class="brand">Bill Ward's<small>SCHOOL OF FLY FISHING</small></div>
<h1>Bill's Best Bets<br>for the Weekend</h1><div class="date">{H.escape(date)}</div></div>
<div class="best"><div class="tag">{H.escape(best[0])}</div><div class="nm">{H.escape(best[1])}</div><div class="sub">Flies, flows, weather and access in the full report</div></div>
<div class="list">{rows}</div>
<div class="foot"><b>Full report with flies, flows &amp; weather</b>flycastinginstruction.com/fishing-report</div>
</body></html>'''
import os; os.makedirs(os.path.dirname(os.path.abspath(out)) or '.',exist_ok=True); open('/tmp/card.html','w').write(page)
with sync_playwright() as p:
    exe='/usr/bin/google-chrome' if os.path.exists('/usr/bin/google-chrome') else None
    b=p.chromium.launch(executable_path=exe,args=['--no-sandbox']) if exe else p.chromium.launch(args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':1080,'height':1350}); pg.goto('file:///tmp/card.html')
    pg.screenshot(path=out); b.close()
print(date, best, rest)
