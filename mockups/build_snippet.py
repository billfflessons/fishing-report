"""Builds banners/homepage-gift-card-schedule.html: the date-switching homepage gift card."""
import re
exec(open("mockups/make_cards.py").read().split("CARDS = [")[0])
BF_END, XM_END = "2026-12-01", "2026-12-26"
bf_parts=[("big","BLACK FRIDAY"),("biggold","SALE · <span data-countdown>DAYS LEFT</span>"),("sub","GIFT CERTIFICATES"),("ribbon",""),("button","SAVE NOW ›"),("foot","Ends Tuesday · Emailed right away")]
xm_parts=[("kicker","★ MERRY CHRISTMAS ★"),("big","<span data-countdown>DAYS LEFT</span>"),("sub","<span data-sub>GIFT CERTIFICATES</span>"),("ribbon",""),("button","SAVE NOW ›"),("foot","Emailed right away, even on Christmas Day")]
def inner(bg,parts,small_gold=False):
    h=card(bg,parts)
    if small_gold:
        h=h.replace("font:900 30px/1.04 'DM Sans',Arial;letter-spacing:.3px;color:"+GOLD,"font:900 24px/1.15 'DM Sans',Arial;letter-spacing:.6px;color:"+GOLD+";margin-top:3px")
    return re.sub(r'^<a class="gcard" href="[^"]*" style="[^"]*">','',h)[:-4]
bf=inner(BLACK,bf_parts,True); xm=inner(GREEN,xm_parts)
mem=open("mockups/original-card-mobile.html").read().strip()
orig_phone=mem.replace(' class="lg:hidden"','')
orig_desktop=orig_phone.replace('width: 100%; max-width: 340px; margin-top: 20px;','position: absolute; top: 26px; right: 26px; z-index: 20; width: 178px;').replace('giftBowRedMobile','giftBowRed')
cd=open("mockups/countdown.js").read().replace("if (typeof module !== 'undefined') module.exports = saleCountdown;\n","")
def sale(cls,phase,bg,body,label):
    return f'<div class="bw-gift {cls}" data-phase="{phase}"><a class="bw-card" href="/fly-fishing-gift-certificates#choose" aria-label="{label}" style="background:{bg}">{body}</a></div>'
snippet=f'''<!-- HOMEPAGE GIFT CARD SCHEDULE (prepared Nov 26, 2026; design approved by Bill)
  Replaces the "MERRY CHRISTMAS" gift card: the desktop card in the hero photo's top-right corner AND the phone card under the opening text.
  BEFORE REPLACING: copy the live Christmas card's exact code out of the site and save it (Bill wants it kept).
  What it shows, by Pacific time:
    through Tue Dec 1, 2026      -> Black Friday sale card, "SALE · N DAYS LEFT", "LAST DAY" on Dec 1
    Wed Dec 2 through Mon Dec 21 -> Christmas sale card reading "CHRISTMAS SALE"
    Tue Dec 22 through Sat Dec 26 -> same card counting down, "5 DAYS LEFT" ... "LAST DAY" on Dec 26
    from Sun Dec 27              -> the original gift card (code saved Nov 20, 2026)
  Desktop (1024px and wider): 290 x 231 px, flush top-right of the hero photo, same spot and size as the Christmas card.
  Phone: up to 340 px wide, under the opening text, where the Christmas phone card is now.
  The sale cards link to the gift certificate page at the six lesson boxes (#choose). No prices change: the sale is the certificates as listed. -->
<style>
.bw-gift{{display:none}}
.bw-gift[data-on]{{display:block}}
.bw-gift .bw-card{{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;text-decoration:none;box-sizing:border-box;box-shadow:0 12px 28px rgba(0,0,0,.45),0 2px 5px rgba(0,0,0,.25);padding:4px 0 6px}}
.bw-gift-desktop .bw-card{{position:absolute;top:0;right:0;z-index:20;width:290px;height:231px;border-radius:0 0 0 8px}}
.bw-gift-phone .bw-card{{width:100%;max-width:340px;margin:20px auto 0;height:231px;border-radius:8px}}
/* the original card (from Dec 27) sat inside the page's own layout; as a block here it keeps its 340px max width */
.bw-gift[data-phase="orig"] > a{{display:block}}
@media (max-width:1023px){{.bw-gift-desktop{{display:none!important}}}}
@media (min-width:1024px){{.bw-gift-phone{{display:none!important}}}}
</style>
<!-- DESKTOP: inside the hero photo container (the same position:relative parent the Christmas card sits in) -->
{sale("bw-gift-desktop","bf",BLACK,bf,"Black Friday sale on gift certificates")}
{sale("bw-gift-desktop","xmas",GREEN,xm,"Christmas sale on gift certificates")}
<div class="bw-gift bw-gift-desktop" data-phase="orig">{orig_desktop}</div>
<!-- PHONE: where the Christmas phone card is now -->
{sale("bw-gift-phone","bf",BLACK,bf,"Black Friday sale on gift certificates")}
{sale("bw-gift-phone","xmas",GREEN,xm,"Christmas sale on gift certificates")}
<div class="bw-gift bw-gift-phone" data-phase="orig">{orig_phone}</div>
<script>
{cd}(function(){{
  var now = window.__bwGiftNow ? new Date(window.__bwGiftNow) : new Date();  /* __bwGiftNow: testing only */
  var bf = saleCountdown('{BF_END}', now), xm = bf ? null : saleCountdown('{XM_END}', now, 5, 'CHRISTMAS SALE');
  var phase = bf ? 'bf' : (xm ? 'xmas' : 'orig');
  document.querySelectorAll('.bw-gift[data-phase="' + phase + '"]').forEach(function(el){{
    el.setAttribute('data-on', '');
    el.querySelectorAll('[data-countdown]').forEach(function(s){{ s.textContent = phase === 'bf' ? bf : xm; }});
    el.querySelectorAll('[data-sub]').forEach(function(s){{ s.textContent = xm === 'CHRISTMAS SALE' ? 'GIFT CERTIFICATES' : 'GIFT CERTIFICATE SALE'; }});
  }});
}})();
</script>
'''
assert '`' not in snippet and '${{' not in snippet
open("banners/homepage-gift-card-schedule.html","w").write(snippet)
print("written", len(snippet))
