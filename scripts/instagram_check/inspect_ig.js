(() => {
  const body = document.body.innerText;
  const url = window.location.href;
  const title = document.title;
  // Look for Instagram-specific elements
  const usernameEl = document.querySelector('a[href*="/"][role="link"], header a, [class*="Username"]');
  const username = usernameEl ? usernameEl.textContent.trim().substring(0,80) : null;
  const verifiedBadge = document.querySelector('[title*="Verified"], svg[aria-label*="Verified"]');
  // Capture meta tags for OG tags
  const ogTitle = document.querySelector('meta[property="og:title"]')?.content;
  const ogDesc = document.querySelector('meta[property="og:description"]')?.content;
  const ogImage = document.querySelector('meta[property="og:image"]')?.content;
  // Is this a login wall?
  const hasLoginWall = /log in|sign up|login to see|create an account/i.test(body.substring(0,500));
  // Is this an error page?
  const isNotFound = /sorry.*doesn't exist|page.*not available|link.*may be broken|content.*unavailable/i.test(body.substring(0,500));
  return {
    title,
    final_url: url,
    bodyLen: body.length,
    bodyPreview: body.substring(0, 1500),
    username,
    verifiedBadge: !!verifiedBadge,
    ogTitle, ogDesc, ogImage,
    hasLoginWall,
    isNotFound
  };
})()
