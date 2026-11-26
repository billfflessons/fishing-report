"""Black Friday sale card with a daily countdown (ends Tue Dec 1, 2026, 11:59 PM Pacific). Mock-ups on Bill's homepage screenshot."""
src = open("make_cards.py").read().split("CARDS = [")[0]
exec(src)  # brings in card(), colors, BOW
from playwright.sync_api import sync_playwright

def bf(count_text):
    return card(BLACK, [("big", "BLACK FRIDAY"),
                        ("biggold2", f"SALE · {count_text}"),
                        ("sub", "GIFT CERTIFICATES"), ("ribbon", ""),
                        ("button", "SAVE NOW ›"), ("foot", "Ends Tuesday · Emailed right away")])

# add the countdown line style to card()
_card = card
def card(bg, parts):
    html_out = _card(bg, [(k if k != "biggold2" else "biggold", t) for k, t in parts])
    return html_out.replace("font:900 30px/1.04 \\'DM Sans\\',Arial;letter-spacing:.3px;color:" + GOLD,
                            "font:900 30px/1.04 \\'DM Sans\\',Arial;letter-spacing:.3px;color:" + GOLD)

DAYS = [("Fri Nov 27", "5 DAYS LEFT"), ("Sat Nov 28", "4 DAYS LEFT"), ("Sun Nov 29", "3 DAYS LEFT"),
        ("Mon Nov 30", "2 DAYS LEFT"), ("Tue Dec 1", "LAST DAY")]

def bfcard(t):
    h = card(BLACK, [("big", "BLACK FRIDAY"), ("biggold", f"SALE · {t}"), ("sub", "GIFT CERTIFICATES"),
                     ("ribbon", ""), ("button", "SAVE NOW ›"), ("foot", "Ends Tuesday · Emailed right away")])
    # the gold countdown line a little smaller than the headline so it fits one line
    return h.replace("font:900 30px/1.04 'DM Sans',Arial;letter-spacing:.3px;color:" + GOLD,
                     "font:900 24px/1.15 'DM Sans',Arial;letter-spacing:.6px;color:" + GOLD + ";margin-top:3px")

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1680, "height": 1050})
    for i, (day, t) in enumerate(DAYS):
        page = (f'<html><body style="margin:0;width:1680px;height:1050px;background:url(homepage-now-christmas.png) no-repeat 0 0;">'
                f'<div style="position:absolute;left:0;top:296px;width:1660px;height:600px;">{bfcard(t)}</div></body></html>')
        open("_tmp.html", "w").write(page); pg.goto("file:///home/claude/fishing-report/mockups/_tmp.html"); pg.wait_for_timeout(200)
        info = pg.evaluate("""(()=>{const c=document.querySelector('.gcard');const kids=[...c.children];
          return {bottom:Math.round(kids[kids.length-1].getBoundingClientRect().bottom),
                  lines:kids.filter(k=>k.textContent.includes('SALE')).map(k=>Math.round(k.getBoundingClientRect().height)),
                  overflowX:kids.some(k=>k.scrollWidth>c.clientWidth)}})()""")
        print(day, t, info)
        if i == 0: pg.screenshot(path="card-A-homepage.png")
        pg.screenshot(path=f"_d{i}.png", clip={"x": 1370, "y": 296, "width": 290, "height": 231})
    strip = "".join(f'<div style="text-align:center"><div style="font:700 17px Georgia;margin-bottom:6px">{d}</div><img src="_d{i}.png" width="290" height="231" style="display:block;box-shadow:0 6px 16px rgba(0,0,0,.3)"></div>' for i, (d, _) in enumerate(DAYS))
    sheet = ('<html><body style="margin:0;background:#efeae1;padding:22px 26px 28px;width:1570px;font-family:Arial">'
             '<div style="background:#ffd84d;font:700 16px Arial;padding:10px 14px;margin-bottom:8px">MOCK-UP ONLY: nothing on the website has been changed.</div>'
             '<div style="font:700 22px Georgia;margin:14px 0 4px">Black Friday sale card, with countdown: what visitors see each day</div>'
             '<div style="font:15px Arial;color:#444;margin-bottom:16px">The number changes by itself at midnight Pacific time. After Tuesday night the card switches automatically to whichever card you pick for after Black Friday.</div>'
             f'<div style="display:flex;gap:22px">{strip}</div></body></html>')
    open("_sheet.html", "w").write(sheet)
    pg2 = b.new_page(viewport={"width": 1622, "height": 400}); pg2.goto("file:///home/claude/fishing-report/mockups/_sheet.html"); pg2.wait_for_timeout(300)
    pg2.screenshot(path="black-friday-countdown.png", full_page=True); b.close()
