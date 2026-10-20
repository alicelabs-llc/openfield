// Agent Bridge — service worker (background.js)
// Polls GitHub raw file for commands, POSTs responses to webhook.site.
// No tokens, no ntfy.sh, no port forwarding. Pure HTTP polling.
//
// Architecture:
//   Agent → GitHub repo file (command.json) → Extension polls → executes
//   Extension → webhook.site POST → Agent reads via webhook.site API
//
// The extension needs NO credentials. The GitHub repo is public (read-only
// for the extension). The webhook.site URL is included in each command.

const COMMAND_URL = "https://api.github.com/repos/eddyflores100-lang/agent-bridge-relay/contents/command.json";
const GITHUB_TOKEN = "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";
const POLL_INTERVAL_MS = 2000; // Fast poll while SW is alive
const ALARM_NAME = "agent-bridge-poll";

let polling = false;
let pollTimer = null;
let lastCmdSeq = 0;
let activeTabId = null;
let commandLog = [];

// ============================================================================
// Use chrome.alarms for persistent polling (survives SW restarts)
// setInterval alone doesn't work in MV3 — Chrome kills the SW after 30s idle.
// chrome.alarms wakes the SW back up.
// ============================================================================

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === ALARM_NAME && polling) {
    poll();
  }
});

chrome.runtime.onStartup.addListener(() => {
  // Restore polling state on browser restart
  chrome.storage.local.get(["connected"], (data) => {
    if (data.connected) {
      startPolling();
    }
  });
});

// ============================================================================
// Polling
// ============================================================================

async function startPolling() {
  if (polling) return;
  polling = true;
  // Sync lastCmdSeq from GitHub on start so we don't replay old commands
  try {
    const resp = await fetch(COMMAND_URL, {
      headers: {
        "Authorization": `token ${GITHUB_TOKEN}`,
        "Accept": "application/vnd.github+json",
        "Cache-Control": "no-cache",
      },
    });
    if (resp.ok) {
      const data = await resp.json();
      const content = atob(data.content);
      const cmd = JSON.parse(content);
      lastCmdSeq = cmd.cmd_seq || 0;
      logToSidepanel(`✅ Polling started (synced seq=${lastCmdSeq})`);
    } else {
      logToSidepanel(`✅ Polling started (sync failed: ${resp.status})`);
    }
  } catch (e) {
    logToSidepanel(`✅ Polling started (sync error: ${e.message})`);
  }
  chrome.storage.local.set({ connected: true });

  // Create a repeating alarm — Chrome minimum is 0.5 min (30s)
  // This wakes the SW if it was killed. setInterval handles the fast path.
  await chrome.alarms.create(ALARM_NAME, { periodInMinutes: 0.5 }); // 30s minimum

  // Also use setInterval as a fast-path (works while SW is alive)
  pollTimer = setInterval(poll, POLL_INTERVAL_MS);

  // Keep the SW alive by reading chrome.storage every 20s
  // This prevents Chrome from killing the SW for inactivity
  keepAlive();
}

function keepAlive() {
  if (!polling) return;
  chrome.storage.local.get(["connected"]).catch(() => {});
  setTimeout(keepAlive, 20000);
}

function stopPolling() {
  polling = false;
  if (pollTimer) {
    clearInterval(pollTimer);
    pollTimer = null;
  }
  chrome.alarms.clear(ALARM_NAME);
  chrome.storage.local.set({ connected: false });
  logToSidepanel("🔌 Polling stopped");
}

async function poll() {
  try {
    // Use GitHub API with auth token — bypasses CDN cache entirely
    // Returns base64-encoded content, which we decode
    const resp = await fetch(COMMAND_URL, {
      headers: {
        "Authorization": `token ${GITHUB_TOKEN}`,
        "Accept": "application/vnd.github+json",
        "Cache-Control": "no-cache",
      },
    });
    if (!resp.ok) {
      console.error("[Agent Bridge] Poll failed:", resp.status);
      return;
    }
    const data = await resp.json();
    // GitHub API returns content as base64
    const content = atob(data.content);
    let cmd;
    try {
      cmd = JSON.parse(content);
    } catch (e) {
      console.error("[Agent Bridge] JSON parse error:", e);
      return;
    }

    // Check if this is a new command
    if (cmd.cmd_seq !== undefined && cmd.cmd_seq > lastCmdSeq) {
      console.log("[Agent Bridge] New command:", cmd.cmd_seq, cmd.action);
      lastCmdSeq = cmd.cmd_seq;
      await handleCommand(cmd);
    }
  } catch (e) {
    console.error("[Agent Bridge] Poll error:", e);
  }
}

// ============================================================================
// Response publishing (POST to webhook.site URL from the command)
// ============================================================================

async function publishResponse(respUrl, obj) {
  if (!respUrl) {
    console.warn("[Agent Bridge] No resp_url in command, cannot publish response");
    return;
  }
  try {
    await fetch(respUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(obj),
    });
  } catch (e) {
    console.error("[Agent Bridge] Failed to publish response:", e);
  }
}

// ============================================================================
// Command handler
// ============================================================================

async function handleCommand(cmd) {
  logToSidepanel(`→ ${cmd.action}${cmd.url ? " " + cmd.url : ""}${cmd.selector ? " " + cmd.selector : ""}`);

  // Ensure we have an active tab
  if (!activeTabId) {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab) activeTabId = tab.id;
  }

  const resp = { id: cmd.cmd_seq, action: cmd.action };
  try {
    const result = await executeAction(cmd);
    resp.ok = true;
    resp.result = result;
  } catch (e) {
    resp.ok = false;
    resp.error = e.message || String(e);
  }
  await publishResponse(cmd.resp_url, resp);
}

async function executeAction(cmd) {
  const action = cmd.action;
  const args = cmd.args || {};

  switch (action) {
    case "ping":
      return { pong: true, ts: Date.now() };

    case "open": {
      const tab = await chrome.tabs.create({ url: args.url, active: true });
      activeTabId = tab.id;
      await waitForTabComplete(tab.id);
      const t = await chrome.tabs.get(tab.id);
      return { tabId: tab.id, url: t.url, title: t.title };
    }

    case "navigate": {
      await chrome.tabs.update(activeTabId, { url: args.url });
      await waitForTabComplete(activeTabId);
      const t = await chrome.tabs.get(activeTabId);
      return { url: t.url, title: t.title };
    }

    case "snapshot": {
      const result = await chrome.scripting.executeScript({
        target: { tabId: activeTabId },
        func: snapshotFunc,
      });
      return result[0]?.result;
    }

    case "click": {
      const r = await chrome.scripting.executeScript({
        target: { tabId: activeTabId },
        func: clickFunc,
        args: [args.selector],
      });
      return { clicked: r[0]?.result };
    }

    case "fill": {
      const r = await chrome.scripting.executeScript({
        target: { tabId: activeTabId },
        func: fillFunc,
        args: [args.selector, args.value],
      });
      return { filled: r[0]?.result };
    }

    case "gettext": {
      const r = await chrome.scripting.executeScript({
        target: { tabId: activeTabId },
        func: getTextFunc,
        args: [args.selector],
      });
      return { text: r[0]?.result };
    }

    case "geturl": {
      const t = await chrome.tabs.get(activeTabId);
      return { url: t.url, title: t.title, tabId: t.id };
    }

    case "listtabs": {
      const tabs = await chrome.tabs.query({});
      return {
        tabs: tabs.map((t) => ({
          id: t.id, url: t.url, title: t.title, active: t.active,
        })),
        activeTabId,
      };
    }

    case "switchtab": {
      await chrome.tabs.update(args.tabId, { active: true });
      activeTabId = args.tabId;
      const t = await chrome.tabs.get(args.tabId);
      return { url: t.url, title: t.title };
    }

    case "eval": {
      const r = await chrome.scripting.executeScript({
        target: { tabId: activeTabId },
        func: new Function("return (" + args.code + ")"),
      });
      return { result: r[0]?.result };
    }

    case "screenshot": {
      const t = await chrome.tabs.get(activeTabId);
      const dataUrl = await chrome.tabs.captureVisibleTab(t.windowId, { format: "png" });
      return { sizeBytes: dataUrl.length, dataUrl };
    }

    case "wait": {
      await new Promise((r) => setTimeout(r, Math.min(args.ms || 1000, 30000)));
      return { waited: args.ms || 1000 };
    }

    case "press": {
      await chrome.scripting.executeScript({
        target: { tabId: activeTabId },
        func: pressFunc,
        args: [args.key || "Enter"],
      });
      return { pressed: args.key || "Enter" };
    }

    case "scroll": {
      await chrome.scripting.executeScript({
        target: { tabId: activeTabId },
        func: scrollFunc,
        args: [args.direction || "down", args.amount || 500],
      });
      return { scrolled: true };
    }

    default:
      throw new Error(`Unknown action: ${action}`);
  }
}

// ============================================================================
// Injected page functions
// ============================================================================

function snapshotFunc() {
  const s = 'a, button, input, select, textarea, [role="button"], [onclick], [contenteditable]';
  const els = Array.from(document.querySelectorAll(s));
  const elements = els
    .filter((el) => {
      const r = el.getBoundingClientRect();
      return r.width > 0 && r.height > 0;
    })
    .slice(0, 200)
    .map((el, i) => {
      const text = (el.innerText || el.value || el.placeholder || "").replace(/\s+/g, " ").trim().substring(0, 80);
      let selector;
      if (el.id) selector = `#${el.id}`;
      else if (el.name) selector = `${el.tagName.toLowerCase()}[name="${el.name}"]`;
      else {
        const path = [];
        let node = el;
        while (node && node !== document.body) {
          const idx = Array.from(node.parentNode?.children || []).indexOf(node) + 1;
          path.unshift(`${node.tagName.toLowerCase()}:nth-child(${idx})`);
          node = node.parentNode;
        }
        selector = path.join(" > ");
      }
      return { ref: `e${i}`, tag: el.tagName.toLowerCase(), type: el.type || el.getAttribute("role") || "", text, name: el.name || "", href: el.href || "", placeholder: el.placeholder || "", selector };
    });
  return { url: location.href, title: document.title, elements };
}

function clickFunc(selector) {
  const el = document.querySelector(selector);
  if (!el) return false;
  el.scrollIntoView({ behavior: "instant", block: "center" });
  el.click();
  return true;
}

function fillFunc(selector, value) {
  const el = document.querySelector(selector);
  if (!el) return false;
  el.focus();
  el.value = value;
  el.dispatchEvent(new Event("input", { bubbles: true }));
  el.dispatchEvent(new Event("change", { bubbles: true }));
  return true;
}

function getTextFunc(selector) {
  const el = document.querySelector(selector);
  if (!el) return null;
  return el.innerText || el.value || el.textContent;
}

function pressFunc(key) {
  const t = document.activeElement || document.body;
  ["keydown", "keypress", "keyup"].forEach((type) => {
    t.dispatchEvent(new KeyboardEvent(type, { key, code: key, bubbles: true, cancelable: true }));
  });
  if (key === "Enter") {
    const form = t.closest("form");
    if (form) form.submit();
  }
  return true;
}

function scrollFunc(direction, amount) {
  const dy = direction === "up" ? -amount : amount;
  window.scrollBy(0, dy);
  return { x: window.scrollX, y: window.scrollY };
}

// ============================================================================
// Helpers
// ============================================================================

function waitForTabComplete(tabId) {
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => {
      chrome.tabs.onUpdated.removeListener(listener);
      reject(new Error("Tab did not complete in 30s"));
    }, 30000);
    function listener(id, info) {
      if (id === tabId && info.status === "complete") {
        clearTimeout(timeout);
        chrome.tabs.onUpdated.removeListener(listener);
        setTimeout(() => resolve(), 500);
      }
    }
    chrome.tabs.onUpdated.addListener(listener);
  });
}

function logToSidepanel(msg) {
  commandLog.push({ ts: Date.now(), msg });
  if (commandLog.length > 100) commandLog.shift();
  chrome.runtime.sendMessage({ type: "log", entry: { ts: Date.now(), msg } }).catch(() => {});
}

// ============================================================================
// Tab tracking
// ============================================================================

chrome.tabs.onActivated.addListener((info) => { activeTabId = info.tabId; });

// ============================================================================
// Lifecycle
// ============================================================================

chrome.runtime.onInstalled.addListener(async () => {
  if (chrome.sidePanel?.setPanelBehavior) {
    await chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true });
  }
  logToSidepanel("Extension installed. Click Connect to start.");
});

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === "connect") { startPolling(); sendResponse({ ok: true }); return true; }
  if (msg.type === "disconnect") { stopPolling(); sendResponse({ ok: true }); return true; }
  if (msg.type === "status") { sendResponse({ connected: polling, lastCmdSeq, activeTabId }); return false; }
  if (msg.type === "getLog") { sendResponse({ log: commandLog }); return false; }
});
