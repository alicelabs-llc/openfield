// Side panel — simplified (no channel ID needed, GitHub repo is hardcoded)
const $ = (id) => document.getElementById(id);

function logMsg(msg, type = "") {
  const log = $("logContainer");
  const time = new Date().toLocaleTimeString("en-US", { hour12: false });
  const entry = document.createElement("div");
  entry.className = `log-entry ${type}`;
  entry.innerHTML = `<span class="ts">${time}</span>${msg}`;
  log.appendChild(entry);
  log.scrollTop = log.scrollHeight;
}

function setStatus(connected) {
  const el = $("status");
  el.className = `status ${connected ? "connected" : "disconnected"}`;
  el.innerText = connected ? "🟢 Connected — listening for commands" : "⚪ Disconnected";
  $("connectBtn").disabled = connected;
  $("disconnectBtn").disabled = !connected;
}

function init() {
  setStatus(false);
  chrome.runtime.sendMessage({ type: "status" }, (resp) => {
    if (chrome.runtime.lastError || !resp) { setStatus(false); return; }
    setStatus(resp.connected);
  });
  chrome.runtime.sendMessage({ type: "getLog" }, (resp) => {
    if (resp && resp.log) {
      resp.log.forEach((e) => logMsg(e.msg));
    }
  });
}

chrome.runtime.onMessage.addListener((msg) => {
  if (msg.type === "log" && msg.entry) logMsg(msg.entry.msg);
});

$("connectBtn").addEventListener("click", () => {
  logMsg("Connecting...");
  chrome.runtime.sendMessage({ type: "connect" }, (resp) => {
    if (resp && resp.ok) { setStatus(true); logMsg("✅ Polling started"); }
    else logMsg("❌ Failed to connect", "err");
  });
});

$("disconnectBtn").addEventListener("click", () => {
  chrome.runtime.sendMessage({ type: "disconnect" }, () => {
    setStatus(false);
    logMsg("🔌 Disconnected");
  });
});

init();
