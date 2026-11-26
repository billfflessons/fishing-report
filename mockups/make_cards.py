"""Mock-ups of homepage gift cards in the Christmas card's exact spot (290 x 231 px, flush top-right of the hero photo).
Composited onto Bill's screenshot of his live homepage (homepage-now-christmas.png, 1680 x 1050)."""
import html
from playwright.sync_api import sync_playwright

GREEN = "linear-gradient(180deg,rgb(31,82,54) 0%,rgb(20,58,38) 100%)"
BLACK = "linear-gradient(180deg,#161616 0%,#000 100%)"
GOLD = "rgb(232,199,102)"
RED = "rgb(140,54,43)"
BOW = ('<svg aria-hidden="true" width="62" height="41" viewBox="0 0 120 80" style="position:absolute;left:50%;top:-15px;margin-left:-31px;overflow:visible;">'
       '<path d="M56 42 L38 80 L47 76 L51 84 L62 44 Z" fill="rgb(140,54,43)"/><path d="M64 42 L82 80 L73 76 L69 84 L58 44 Z" fill="rgb(140,54,43)"/>'
       '<path d="M60 38 C42 8 6 10 12 32 C16 48 44 48 60 38 Z" fill="rgb(160,62,49)"/><path d="M60 38 C78 8 114 10 108 32 C104 48 76 48 60 38 Z" fill="rgb(160,62,49)"/>'
       '<ellipse cx="60" cy="39" rx="10" ry="9" fill="rgb(120,44,35)"/></svg>')

def card(bg, parts):
    out = []
    for kind, text in parts:
        t = text
        if kind == "kicker":
            out.append(f'<div style="font:800 11.5px \'DM Sans\',Arial;letter-spacing:2.2px;color:{GOLD};">{t}</div>')
        elif kind == "big":
            out.append(f'<div style="font:900 30px/1.04 \'DM Sans\',Arial;letter-spacing:.3px;color:#fff;margin-top:4px;">{t}</div>')
        elif kind == "biggold":
            out.append(f'<div style="font:900 30px/1.04 \'DM Sans\',Arial;letter-spacing:.3px;color:{GOLD};">{t}</div>')
        elif kind == "serif":
            out.append(f'<div style="font:700 21px/1.15 \'Playfair Display\',Georgia,serif;color:#fff;margin-top:4px;">{t}</div>')
        elif kind == "sub":
            out.append(f'<div style="font:700 16px \'Playfair Display\',Georgia,serif;letter-spacing:1.2px;color:#fff;margin-top:6px;">{t}</div>')
        elif kind == "ribbon":
            out.append(f'<div style="position:relative;align-self:stretch;margin:13px 0 0;height:11px;background:{RED};">{BOW}</div>')
        elif kind == "line":
            out.append(f'<div style="font:700 14px/1.35 \'DM Sans\',Arial;color:#fff;margin-top:20px;padding:0 14px;">{t}</div>')
        elif kind == "button":
            out.append(f'<div style="display:inline-block;margin-top:20px;background:{GOLD};color:#111;font:900 14px \'DM Sans\',Arial;letter-spacing:1.3px;padding:7px 20px;border-radius:5px;">{t}</div>')
        elif kind == "button2":
            out.append(f'<div style="display:inline-block;margin-top:8px;background:{GOLD};color:#111;font:900 14px \'DM Sans\',Arial;letter-spacing:1.3px;padding:7px 20px;border-radius:5px;">{t}</div>')
        elif kind == "foot":
            out.append(f'<div style="font:600 11.5px/1.45 \'DM Sans\',Arial;color:rgba(255,255,255,.88);margin-top:8px;">{t}</div>')
    return ('<a class="gcard" href="/fly-fishing-gift-certificates#choose" style="position:absolute;top:0;right:0;width:290px;height:231px;'
            f'box-sizing:border-box;background:{bg};border-radius:0 0 0 8px;box-shadow:0 12px 28px rgba(0,0,0,.45),0 2px 5px rgba(0,0,0,.25);'
            'text-align:center;text-decoration:none;padding:4px 0 6px;display:flex;flex-direction:column;align-items:center;justify-content:center;">'
            + "".join(out) + '</a>')

CARDS = [
  ("A", "Black Friday sale (Nov 27 – Dec 1)", "Needs the sale prices", BLACK, [
    ("big", "BLACK FRIDAY"), ("biggold", "SALE"), ("sub", "GIFT CERTIFICATES"), ("ribbon", ""),
    ("button", "SAVE NOW ›"), ("foot", "Sale ends Tuesday · Emailed right away")]),
  ("1", "Christmas sale (after Black Friday)", "Needs the sale prices to continue", GREEN, [
    ("kicker", "★ MERRY CHRISTMAS ★"), ("big", "CHRISTMAS SALE"), ("sub", "GIFT CERTIFICATES"), ("ribbon", ""),
    ("button", "SAVE NOW ›"), ("foot", "Sale ends Dec 24 · Emailed right away")]),
  ("2", "Countdown (number changes every day by itself)", "Needs the sale prices to continue", GREEN, [
    ("kicker", "★ MERRY CHRISTMAS ★"), ("big", "12 DAYS LEFT"), ("sub", "GIFT CERTIFICATE SALE"), ("ribbon", ""),
    ("button", "SAVE NOW ›"), ("foot", "Emailed right away, even on Christmas Eve")]),
  ("3", "Last-minute gift", "Works with or without a sale", GREEN, [
    ("kicker", "★ MERRY CHRISTMAS ★"), ("big", "STILL IN TIME"), ("sub", "GIFT CERTIFICATES"), ("ribbon", ""),
    ("line", "Emailed right away, even on Christmas Eve"), ("button2", "BUY ONLINE ›")]),
  ("4", "The person who has everything", "Needs the sale prices to continue", BLACK, [
    ("kicker", "GIFT CERTIFICATE SALE"), ("serif", "For the person who<br>has everything"), ("ribbon", ""),
    ("button", "SAVE NOW ›"), ("foot", "Emailed right away")]),
  ("5", "Give an experience", "Needs the sale prices to continue", GREEN, [
    ("kicker", "★ HOLIDAY SALE ★"), ("big", "GIVE AN<br>EXPERIENCE"), ("sub", "NOT ANOTHER THING"), ("ribbon", ""),
    ("button", "SAVE NOW ›"), ("foot", "Gift certificates · Emailed right away")]),
]

BG = "homepage-now-christmas.png"
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1680, "height": 1050})
    shots = []
    for key, title, note, bg, parts in CARDS:
        page = (f'<html><body style="margin:0;width:1680px;height:1050px;background:url({BG}) no-repeat 0 0;">'
                f'<div style="position:absolute;left:0;top:296px;width:1660px;height:600px;">{card(bg, parts)}</div></body></html>')
        open("_tmp.html", "w").write(page)
        pg.goto("file:///home/claude/fishing-report/mockups/_tmp.html"); pg.wait_for_timeout(200)
        e = pg.query_selector(".gcard")
        last = pg.evaluate("document.querySelector('.gcard').lastElementChild.getBoundingClientRect().bottom")
        print(key, e.bounding_box(), "last line bottom", round(last), "fits" if last <= 296 + 231 - 6 else "TOO TALL", "widest", pg.evaluate("Math.max(...[...document.querySelectorAll('.gcard > div')].map(d=>d.scrollWidth))"))
        pg.screenshot(path=f"card-{key}-homepage.png")
        pg.screenshot(path=f"_close-{key}.png", clip={"x": 1110, "y": 240, "width": 560, "height": 360})
        shots.append((key, title, note))
    # contact sheet
    cells = "".join(
        f'<div style="width:560px"><div style="font:700 20px Georgia;margin:0 0 2px">{"Black Friday card" if k=="A" else "Option "+k}: {html.escape(t)}</div>'
        f'<div style="font:600 14px Arial;color:#8a3a2e;margin-bottom:8px">{html.escape(n)}</div>'
        f'<img src="_close-{k}.png" width="560" height="360" style="display:block;border-radius:6px"></div>' for k, t, n in shots)
    sheet = ('<html><body style="margin:0;background:#efeae1;font-family:Arial;padding:24px 28px 30px;width:1184px">'
             '<div style="background:#ffd84d;font:700 16px Arial;padding:10px 14px;margin-bottom:22px">MOCK-UP ONLY: nothing on the website has been changed. '
             'Each card sits exactly where the Christmas card is now, same size, clear of the anglers\' heads.</div>'
             f'<div style="display:flex;flex-wrap:wrap;gap:26px 64px">{cells}</div></body></html>')
    open("_sheet.html", "w").write(sheet)
    pg2 = b.new_page(viewport={"width": 1240, "height": 900}); pg2.goto("file:///home/claude/fishing-report/mockups/_sheet.html"); pg2.wait_for_timeout(300)
    pg2.screenshot(path="gift-card-options.png", full_page=True)
    b.close()
