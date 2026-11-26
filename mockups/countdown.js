// Days left in a sale that ends at the end of `endDate` (YYYY-MM-DD), counted in Pacific time.
// Returns null after the sale has ended.
function saleCountdown(endDate, now) {
  now = now || new Date();
  var pt = new Intl.DateTimeFormat('en-CA', {timeZone: 'America/Los_Angeles', year: 'numeric', month: '2-digit', day: '2-digit'}).format(now);
  var today = Date.UTC(+pt.slice(0, 4), +pt.slice(5, 7) - 1, +pt.slice(8, 10));
  var end = Date.UTC(+endDate.slice(0, 4), +endDate.slice(5, 7) - 1, +endDate.slice(8, 10));
  var left = Math.round((end - today) / 86400000) + 1;
  if (left < 1) return null;
  return left === 1 ? 'LAST DAY' : left + ' DAYS LEFT';
}
if (typeof module !== 'undefined') module.exports = saleCountdown;
