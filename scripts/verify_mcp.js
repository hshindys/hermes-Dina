#!/usr/bin/env node
// MCP liveness probe for obsidian-mcp bridge
// On Windows, npx is a .cmd file, not a binary — use cmd.exe /c to launch it
const { spawn } = require('child_process');

const CMD_EXE = 'cmd.exe';
const CMD_ARGS = ['/c', 'npx', '-y', 'obsidian-mcp', 'D:/document/Dina'];

const VAULT_NAME = 'dina';

function send(proc, msg) {
  proc.stdin.write(JSON.stringify(msg) + '\n');
}

function readLine(proc, timeoutMs) {
  return new Promise((resolve) => {
    const timer = setTimeout(() => resolve(null), timeoutMs);
    proc.stdout.on('data', (data) => {
      clearTimeout(timer);
      proc.stdout.removeAllListeners('data');
      const lines = data.toString().trim().split('\n');
      for (const line of lines) {
        try {
          resolve(JSON.parse(line.trim()));
          return;
        } catch (e) {}
      }
    });
  });
}

async function main() {
  console.log('MCP Bridge Liveness Check');
  console.log('='.repeat(44));

  const proc = spawn(CMD_EXE, CMD_ARGS, { stdio: ['pipe', 'pipe', 'pipe'] });

  send(proc, { jsonrpc: '2.0', id: 1, method: 'initialize', params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'verify-mcp', version: '1.0' } } });

  const initResult = await readLine(proc, 5000);
  const initOk = initResult && !!initResult.result;
  console.log('Initialized:     ', initOk ? 'OK' : 'FAIL');

  send(proc, { jsonrpc: '2.0', method: 'notifications/initialized', params: {} });

  send(proc, { jsonrpc: '2.0', id: 2, method: 'tools/list', params: {} });
  const toolsResult = await readLine(proc, 5000);
  const tools = (toolsResult && toolsResult.result && toolsResult.result.tools) || [];
  console.log('Tools registered:', tools.length);

  send(proc, { jsonrpc: '2.0', id: 3, method: 'tools/call', params: { name: 'list-available-vaults', arguments: {} } });
  const vaultResult = await readLine(proc, 5000);
  let vault = 'unknown';
  if (vaultResult && vaultResult.result && vaultResult.result.content) {
    for (const c of vaultResult.result.content) {
      if (c.type === 'text') {
        const lines = c.text.split('\n').filter(l => l.trim());
        if (lines.length) vault = lines[lines.length - 1].trim().toLowerCase();
      }
    }
  }
  console.log('Vault:           ', vault);

  proc.stdin.end();
  setTimeout(() => proc.kill(), 500);

  const healthy = initOk && tools.length >= 10 && vault === VAULT_NAME;
  console.log('='.repeat(44));
  console.log('Overall:         ', healthy ? 'HEALTHY' : 'ISSUES');
  process.exit(healthy ? 0 : 1);
}

main().catch(e => { console.error(e); process.exit(1); });