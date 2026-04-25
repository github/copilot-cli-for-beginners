const fs = require('fs');
const {spawn} = require('child_process');
const path = require('path');

const cfgPath = path.join(process.cwd(), 'samples', 'mcp-configs', 'mcp-config.json');
if (!fs.existsSync(cfgPath)) {
  console.error('mcp-config.json not found at', cfgPath);
  process.exit(1);
}

const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));

function startService(name, svc) {
  const env = Object.assign({}, process.env, svc.env || {});
  const child = spawn(svc.command, svc.args, {stdio: 'inherit', env});
  child.on('exit', (code) => console.log(`${name} exited with ${code}`));
  child.on('error', (err) => console.error(`${name} failed:`, err));
  console.log(`Started ${name} (pid=${child.pid})`);
}

for (const [name, svc] of Object.entries(cfg.mcpServers || {})) {
  if (name === 'context7' || name === 'filesystem') {
    startService(name, svc);
  }
}

// keep process alive so devcontainer doesn't background-kill the command
setInterval(() => {}, 1e6);
