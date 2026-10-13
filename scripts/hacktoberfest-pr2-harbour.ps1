# ============================================================
# HACKTOBERFEST SCRIPT 2 — harbour #41 (filter control chars in push_history)
# ============================================================
# Repo: https://github.com/Ishannaik/harbour
# Issue: #41 — persist: filter control characters and newlines in push_history
# Fix: 1 archivo Rust (src/persist.rs), +32 -2 líneas, con test nuevo

$ErrorActionPreference = "Stop"
$workspace = "C:\Users\Usuario\hacktoberfest-harbour"
New-Item -ItemType Directory -Path $workspace -Force | Out-Null
Set-Location $workspace

if (Test-Path harbour) { Remove-Item harbour -Recurse -Force }
gh repo clone Ishannaik/harbour harbour
Set-Location harbour
git checkout -b fix/41-filter-control-chars-history

$rustPath = "src\persist.rs"
$bytes = [System.IO.File]::ReadAllBytes("$PWD\$rustPath")
$content = [System.Text.Encoding]::UTF8.GetString($bytes)

# 1. Modificar push_history para sanitizar control chars
$old = @'
    /// Records a query at the front, de-duplicated, capped.
    pub fn push_history(&self, existing: &mut Vec<String>, query: &str) -> io::Result<()> {
        let query = query.trim();
        if query.is_empty() {
            return Ok(());
        }
        existing.retain(|q| q != query);
        existing.insert(0, query.to_owned());
        existing.truncate(HISTORY_CAP);
        self.save_history(existing)
    }
'@

$new = @'
    /// Records a query at the front, de-duplicated, capped.
    pub fn push_history(&self, existing: &mut Vec<String>, query: &str) -> io::Result<()> {
        let query = query.trim();
        if query.is_empty() {
            return Ok(());
        }
        // Strip ASCII control characters and newlines so they cannot corrupt
        // the on-disk history file (one entry per line) or be used to inject
        // extra phantom entries via a pasted multi-line query. Tabs and other
        // horizontal whitespace are kept so queries like `foo\tbar` survive.
        let sanitized: String = query
            .chars()
            .filter(|&c| c == '\t' || !c.is_control())
            .collect();
        if sanitized.is_empty() {
            return Ok(());
        }
        existing.retain(|q| q != &sanitized);
        existing.insert(0, sanitized);
        existing.truncate(HISTORY_CAP);
        self.save_history(existing)
    }
'@

$content = $content.Replace($old, $new)

# 2. Agregar test nuevo despues de blank_queries_are_not_recorded
$old_test = @'
    #[test]
    fn blank_queries_are_not_recorded() {
        let store = temp_store("blank");
        let mut history = Vec::new();
        store.push_history(&mut history, "   ").unwrap();
        assert!(history.is_empty());
    }
'@

$new_test = @'
    #[test]
    fn blank_queries_are_not_recorded() {
        let store = temp_store("blank");
        let mut history = Vec::new();
        store.push_history(&mut history, "   ").unwrap();
        assert!(history.is_empty());
    }

    #[test]
    fn control_chars_and_newlines_are_stripped_from_history() {
        // A pasted multi-line query must not become two phantom entries.
        // Carriage returns, line feeds, vertical tabs, form feeds, ESC and
        // other ASCII control bytes are stripped so the on-disk history file
        // (one entry per line) stays parseable. Tabs survive because users
        // sometimes paste formatted queries.
        let store = temp_store("ctrl");
        let mut history = Vec::new();
        store.push_history(&mut history, "dune\r\nshogun").unwrap();
        store.push_history(&mut history, "asan\x1bne").unwrap(); // \x1b = ESC
        store.push_history(&mut history, "tab\tsurvives").unwrap();
        assert_eq!(
            history,
            vec!["tab\tsurvives", "dasne", "duneshogun"],
            "control chars stripped, newlines do not split, tabs kept"
        );
    }
'@

$content = $content.Replace($old_test, $new_test)

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText("$PWD\$rustPath", $content, $utf8NoBom)

git diff --stat
git add $rustPath
git -c user.name="Edison Flores" -c user.email="eddyflores100-lang@protonmail.com" commit -m "persist: strip control characters and newlines from push_history" -m "Closes #41." -m "push_history() previously stored the trimmed query as-is, including any ASCII control characters embedded in it. Two failure modes resulted: (1) A pasted multi-line query (e.g. dune\r\nshogun) would corrupt the on-disk history file: each entry is written one per line, so the embedded newline silently split the single entry into two phantom entries on the next load. (2) Control bytes like ESC, vertical tabs, form feeds and NUL made it into the history file and were echoed back into the UI history picker, occasionally messing up the terminal that rendered them. Strip every char where char::is_control() returns true, except tab which is meaningful in pasted structured queries. Empty-after-sanitisation queries are dropped just like blank queries already are. Adds a regression test that pastes a multi-line query, an ESC-riddled query and a tab-containing query, asserting the resulting history is exactly what a user would expect: three entries, no phantom splits, tabs preserved."

gh repo fork Ishannaik/harbour --clone=false
git remote rename origin upstream 2>$null
git remote remove origin 2>$null
git remote add origin "https://github.com/eddyflores100-lang/harbour.git"
git push -u origin fix/41-filter-control-chars-history

gh pr create --repo Ishannaik/harbour --base main --head eddyflores100-lang:fix/41-filter-control-chars-history --title "persist: strip control characters and newlines from push_history" --body "Closes #41. push_history() previously stored the trimmed query as-is, including ASCII control characters. Strip them so multi-line pasted queries do not corrupt the on-disk history file. Tabs kept (meaningful in structured queries). Adds a regression test."
