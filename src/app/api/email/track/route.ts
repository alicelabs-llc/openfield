import { NextRequest, NextResponse } from 'next/server';
import { appendFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';

// Tracking directory shared with the email campaign scripts.
const TRACKING_DIR = '/home/z/my-project/download/email_campaigns/tracking';
const OPENS_LOG = join(TRACKING_DIR, 'opens.jsonl');

// 1x1 transparent GIF (43 bytes). Browsers will render it as an invisible dot.
const PIXEL_GIF = Buffer.from(
  'R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7',
  'base64'
);

export async function GET(req: NextRequest) {
  const url = new URL(req.url);
  const c = url.searchParams.get('c') || 'unknown';
  const r = url.searchParams.get('r') || 'unknown';

  const ip =
    req.headers.get('x-forwarded-for')?.split(',')[0]?.trim() ||
    req.headers.get('x-real-ip') ||
    'unknown';
  const ua = req.headers.get('user-agent') || 'unknown';
  const referer = req.headers.get('referer') || 'unknown';

  // Append the open record. Fail silently if the log can't be written — never
  // break the pixel response, because that would hurt deliverability and the
  // recipient would see a broken-image icon in some clients.
  try {
    if (!existsSync(TRACKING_DIR)) mkdirSync(TRACKING_DIR, { recursive: true });
    const entry = JSON.stringify({
      ts: new Date().toISOString(),
      c, // campaign id (e.g. "alicelabs_final")
      r, // recipient id (8-char hex assigned by the sender script)
      ip,
      ua: ua.slice(0, 200),
      referer: referer.slice(0, 200),
    });
    appendFileSync(OPENS_LOG, entry + '\n', 'utf-8');
  } catch (e) {
    // Intentionally swallow — see comment above.
  }

  return new NextResponse(PIXEL_GIF, {
    status: 200,
    headers: {
      'Content-Type': 'image/gif',
      'Content-Length': PIXEL_GIF.length.toString(),
      'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0',
      'Pragma': 'no-cache',
      'Expires': '0',
    },
  });
}

// Always run dynamically — never cache the pixel response at the edge.
export const dynamic = 'force-dynamic';
