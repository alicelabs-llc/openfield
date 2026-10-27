import json, urllib.request, ssl

TOKEN = "86f56136e9bdbe4a6fe60d0b8f2e4c277f407590"
HEADERS = {"Authorization": f"token {TOKEN}", "Content-Type": "application/json", "Accept": "application/json", "User-Agent": "Mozilla/5.0"}
CTX = ssl.create_default_context()

body = """Closes #863.

## Summary

Adds a toggle button to the poll component that lets users hide poll results (progress bars and percentages) until they have voted.

## What changed

### `poll.component.ts`
- Added `hideResults` signal (default: false) — toggled by the user
- Added `showResultsOverride` signal — set to true when the user clicks "Show results" while results are hidden
- Added `shouldShowResults` getter — returns `true` if the user has already voted, or if results aren't hidden, or if the user explicitly asked to show them
- Added `toggleHideResults()` and `showResultsButton()` methods
- Imported `MatIconModule` and `MatMenuModule` for the toggle UI

### `poll.component.html`
- When `shouldShowResults` is false: only shows the checkbox/radio options (no progress bars)
- When `shouldShowResults` is false: shows a "Show results" button so users can peek if they want
- When the poll is open and the user hasn't voted: shows a toggle button (eye icon) to hide/show results

### `poll.component.scss`
- Added `.hide-results-toggle` style for the toggle button

## Translation keys needed

The following keys should be added to the i18n files:
- `poll.showResults` — "Show results"
- `poll.showResultsToggle` — "Show results toggle"  
- `poll.hideResultsToggle` — "Hide results toggle"

## Behaviour

1. Default: results visible (progress bars + percentages shown as before)
2. User clicks the eye icon → results hidden (only options shown)
3. While hidden, a "Show results" button appears → user can peek
4. After voting, results always show (no point hiding after voted)
5. Toggle persists only for the current view (not across sessions — that would need a setting in the settings service, which is a bigger change)
"""

payload = {
    "title": "feat(poll): add option to hide poll results before voting",
    "head": "eddyflores100:feature/hide-poll-results",
    "base": "main",
    "body": body,
}
req = urllib.request.Request(
    "https://codeberg.org/api/v1/repos/wafrn/wafrn/pulls",
    data=json.dumps(payload).encode(),
    headers=HEADERS,
    method="POST",
)
try:
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        d = json.loads(resp.read().decode())
    print(f"PR #{d.get('number')} created: {d.get('html_url')}")
    print(f"  mergeable: {d.get('mergeable','?')}")
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()[:400]}")
