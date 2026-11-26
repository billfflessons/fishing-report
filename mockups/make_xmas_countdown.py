"""Christmas sale card with countdown, Dec 2-26, 2026. Mock-ups on Bill's homepage screenshot."""
import subprocess, json
exec(open("make_cards.py").read().split("CARDS = [")[0])
from playwright.sync_api import sync_playwright

DAYS = [("Dec 2 – Dec 21", "2026-12-02T12:00:00-08:00"), ("Tue Dec 22", "2026-12-22T12:00:00-08:00"),
        ("Thu Dec 24", "2026-12-24T12:00:00-08:00"), ("Fri Dec 25", "2026-12-25T12:00:00-08:00"), ("Sat Dec 26", "2026-12-26T12:00:00-08:00")]
# use the real tested countdown code for each day's text
texts = json.loads(subprocess.check_output(["node", "-e",
    "const f=require('./countdown.js');console.log(JSON.stringify(" + json.dumps([d for _, d in DAYS]) + ".map(t=>f('2026-12-26',new Date(t),5,'CHRISTMAS SALE'))))"]))

import re
texts = [re.sub(r'^(\d+) DAYS LEFT$', r'JUST \1 DAYS', t) for t in texts]
def xcard(t):
    return card(GREEN, [("kicker", "★ MERRY CHRISTMAS ★"), ("big", t), ("sub", "GIFT CERTIFICATES" if t == "CHRISTMAS SALE" else "GIFT CERTIFICATE SALE"), ("ribbon", ""),
                        ("button", "SAVE NOW ›"), ("foot", "Emailed right away, even on Christmas Day")])

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1680, "height": 1050})
    for i, ((day, _), t) in enumerate(zip(DAYS, texts)):
        page = (f'<html><body style="margin:0;width:1680px;height:1050px;background:url(homepage-now-christmas.png) no-repeat 0 0;">'
                f'<div style="position:absolute;left:0;top:296px;width:1660px;height:600px;">{xcard(t)}</div></body></html>')
        open("_tmp.html", "w").write(page); pg.goto("file:///home/claude/fishing-report/mockups/_tmp.html"); pg.wait_for_timeout(200)
        info = pg.evaluate("(()=>{const c=document.querySelector('.gcard');const k=[...c.children];return {bottom:Math.round(k[k.length-1].getBoundingClientRect().bottom),overflowX:k.some(x=>x.scrollWidth>c.clientWidth)}})()")
        print(day, t, info)
        if i == 0: pg.screenshot(path="card-xmas-countdown-homepage.png")
        pg.screenshot(path=f"_d{i}.png", clip={"x": 1370, "y": 296, "width": 290, "height": 231})
    strip = "".join(f'<div style="text-align:center"><div style="font:700 17px Georgia;margin-bottom:6px">{d}</div><img src="_d{i}.png" width="290" height="231" style="display:block;box-shadow:0 6px 16px rgba(0,0,0,.3)"></div>' for i, (d, _) in enumerate(DAYS))
    sheet = ('<html><body style="margin:0;background:#efeae1;padding:22px 26px 28px;width:1570px;font-family:Arial">'
             '<div style="background:#ffd84d;font:700 16px Arial;padding:10px 14px;margin-bottom:8px">MOCK-UP ONLY: nothing on the website has been changed.</div>'
             '<div style="font:700 22px Georgia;margin:14px 0 4px">Christmas sale card, Dec 2 – 26: "Christmas Sale" first, countdown for the last 5 days</div>'
             '<div style="font:15px Arial;color:#444;margin-bottom:16px">Goes up by itself on Wednesday, Dec 2. From Tuesday, Dec 22 it counts down, changing at midnight Pacific time. On Dec 27 the card switches back to your original gift card by itself.</div>'
             f'<div style="display:flex;gap:22px">{strip}</div></body></html>')
    open("_sheet.html", "w").write(sheet)
    pg2 = b.new_page(viewport={"width": 1622, "height": 400}); pg2.goto("file:///home/claude/fishing-report/mockups/_sheet.html"); pg2.wait_for_timeout(300)
    pg2.screenshot(path="christmas-countdown.png", full_page=True); b.close()
