(() => {
  const body = document.body.innerText;
  const budgets = (body.match(/\$[\d,]+(?:\s*-\s*\$[\d,]+)?(?:\s*(?:USD|AUD|CAD))?/g) || []).slice(0,5);
  const bidCount = (body.match(/(\d+)\s*bids?/i) || [])[1];
  const avgBid = (body.match(/avg[^]{0,80}/i) || [])[0];
  let desc = '';
  const candidates = ['[class*="description"]','[class*="Description"]','[class*="project-details"]','main'];
  for (const sel of candidates) {
    const el = document.querySelector(sel);
    if (el && el.innerText.length > 200) { desc = el.innerText.substring(0, 2000); break; }
  }
  if (!desc) desc = body.substring(0, 2000);
  return { title: document.title, url: window.location.href, budgets, bidCount, avgBid, bodyLen: body.length, desc };
})()
