#!/usr/bin/env node
// ============================================================
// ZOLO NEWS — SELFTEST del servidor MCP (sin depender del núcleo)
// Subagente 125-C · AliceLabs
//
// Prueba de PROTOCOLO end-to-end: spawnea `node src/mcp/server.js`
// como proceso hijo y habla JSON-RPC 2.0 por stdin/stdout (framing
// newline-delimited, igual que StdioServerTransport).
//
// Secuencia: initialize → notifications/initialized → tools/list
//            → (extra, sin núcleo) tools/call zolo_set_mood inválido
//
// NO se llama ninguna tool que dependa de src/news.js / weather.js /
// mood.js / scriptWriter.js: la única tools/call del test falla EN LA
// VALIDACIÓN (humor inválido), antes de importar el núcleo, y la
// configuración se carga del fallback config.json (el núcleo 125-A
// puede o no existir al momento de este test).
//
// Uso:  node src/mcp/selftest.js   → imprime "MCP SELFTEST OK" (exit 0)
// ============================================================

import { spawn } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SERVER_PATH = path.resolve(__dirname, 'server.js');

const fallos = [];
const log = (...a) => console.log(...a);

// ---------- proceso hijo ----------
const hijo = spawn(process.execPath, [SERVER_PATH], { stdio: ['pipe', 'pipe', 'pipe'] });
let stderrHijo = '';
hijo.stderr.on('data', (d) => { stderrHijo += d.toString(); });
hijo.on('error', (e) => {
  console.error('MCP SELFTEST FALLO: no se pudo spawnear server.js:', e.message);
  process.exit(1);
});

// ---------- framing newline-delimited JSON ----------
let buffer = '';
const pendientes = new Map();

hijo.stdout.on('data', (d) => {
  buffer += d.toString();
  let idx;
  while ((idx = buffer.indexOf('\n')) >= 0) {
    const linea = buffer.slice(0, idx).trim();
    buffer = buffer.slice(idx + 1);
    if (!linea) continue;
    let msg;
    try { msg = JSON.parse(linea); } catch { continue; } // ignora ruido no-JSON
    if (msg?.id !== undefined && msg?.id !== null && pendientes.has(msg.id)) {
      pendientes.get(msg.id)(msg);
      pendientes.delete(msg.id);
    }
  }
});

function enviar(msg) {
  hijo.stdin.write(JSON.stringify(msg) + '\n');
}

function pedir(msg, timeoutMs = 10000) {
  return new Promise((resolve, reject) => {
    const t = setTimeout(() => {
      pendientes.delete(msg.id);
      reject(new Error(`timeout de ${timeoutMs}ms esperando respuesta id=${msg.id} (${msg.method})`));
    }, timeoutMs);
    pendientes.set(msg.id, (resp) => { clearTimeout(t); resolve(resp); });
    enviar(msg);
  });
}

// ---------- watchdog global ----------
const WATCHDOG = setTimeout(() => {
  console.error('MCP SELFTEST FALLO: timeout global de 30s');
  console.error('stderr del servidor:\n' + (stderrHijo.slice(-2000) || '(vacío)'));
  hijo.kill('SIGKILL');
  process.exit(1);
}, 30000);

try {
  // ---------- 1) initialize ----------
  const init = await pedir({
    jsonrpc: '2.0', id: 1, method: 'initialize',
    params: {
      protocolVersion: '2024-11-05',
      capabilities: {},
      clientInfo: { name: 'zolo-selftest', version: '1.0.0' },
    },
  });
  if (init.error) fallos.push(`initialize devolvió error: ${init.error.message || JSON.stringify(init.error)}`);
  const servidor = init.result?.serverInfo;
  if (servidor?.name !== 'zolo-news') {
    fallos.push(`serverInfo.name esperado "zolo-news", llegó "${servidor?.name}"`);
  }
  log(`· initialize OK — servidor: ${servidor?.name} v${servidor?.version} · protocolo ${init.result?.protocolVersion}`);

  // ---------- 2) notificación initialized ----------
  enviar({ jsonrpc: '2.0', method: 'notifications/initialized' });

  // ---------- 3) tools/list ----------
  const lista = await pedir({ jsonrpc: '2.0', id: 2, method: 'tools/list' });
  if (lista.error) fallos.push(`tools/list devolvió error: ${lista.error.message || JSON.stringify(lista.error)}`);
  const tools = lista.result?.tools || [];
  const nombres = tools.map((t) => t.name);
  const esperadas = ['zolo_get_news', 'zolo_get_weather', 'zolo_get_bulletin', 'zolo_set_mood'];
  for (const esperada of esperadas) {
    if (!nombres.includes(esperada)) fallos.push(`falta la tool ${esperada} en tools/list`);
  }
  if (tools.length !== 4) fallos.push(`se esperaban 4 tools, llegaron ${tools.length}: ${nombres.join(', ')}`);
  for (const t of tools) {
    if (!t.description) fallos.push(`la tool ${t.name} no tiene description`);
    if (t.inputSchema?.type !== 'object') fallos.push(`la tool ${t.name} no declara inputSchema tipo object`);
  }
  log(`· tools/list OK — ${tools.length} tools: ${nombres.join(', ')}`);

  // ---------- 4) tools/call SIN núcleo (ruta de error validada) ----------
  // "inexistente" no está en cfg.mood.allowed → la validación de zolo_set_mood
  // rechaza ANTES de importar src/mood.js → la prueba no depende del núcleo.
  const call = await pedir({
    jsonrpc: '2.0', id: 3, method: 'tools/call',
    params: { name: 'zolo_set_mood', arguments: { mood: 'inexistente' } },
  });
  const texto = call?.result?.content?.[0]?.text || '';
  if (call.error) fallos.push(`tools/call devolvió error de protocolo (se esperaba isError): ${call.error.message || ''}`);
  if (!texto.startsWith('ERROR:')) fallos.push(`se esperaba "ERROR: ..." para mood inválido, llegó: "${texto.slice(0, 120)}"`);
  else if (!texto.includes('Valores permitidos')) fallos.push('el error de mood inválido no lista los valores permitidos');
  if (call.result?.isError !== true) fallos.push('tools/call con error debería marcar isError:true');
  log(`· tools/call (ruta de error, sin núcleo) OK — "${texto.slice(0, 80)}..."`);
} catch (e) {
  fallos.push(e?.message || String(e));
}

// ---------- veredicto ----------
clearTimeout(WATCHDOG);
hijo.kill('SIGTERM');

setTimeout(() => {
  if (fallos.length) {
    console.error('MCP SELFTEST FALLO: ' + fallos.join(' | '));
    if (stderrHijo.trim()) console.error('stderr del servidor:\n' + stderrHijo.slice(-2000));
    process.exit(1);
  }
  log('MCP SELFTEST OK');
  process.exit(0);
}, 150);
