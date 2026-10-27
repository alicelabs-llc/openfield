(async () => {
  // First visit the page
  const res = await fetch('https://www.openhiggsfield.ai/');
  const html = await res.text();
  // Find any base URL embedded in HTML or __NEXT_DATA__
  const matches = html.match(/https?:\/\/[^"'\s<>]+/g) || [];
  const hfRelated = matches.filter(u => u.includes('higgs') || u.includes('hf.co') || u.includes('huggingface'));
  return {
    status: res.status,
    headers: Object.fromEntries(res.headers.entries()),
    urlMatches: [...new Set(matches)].slice(0,30),
    hfRelated
  };
})()
