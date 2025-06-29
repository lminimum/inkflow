const { spawn } = require('child_process');
const path = require('path');

// 启动后端服务
const backendProcess = spawn('uvicorn', [
  'main:app',
  '--reload',
  '--host', '0.0.0.0',
  '--port', '3000'
], {
  cwd: path.join(__dirname, 'ink-backend'),
  stdio: 'inherit'
});

backendProcess.on('close', (code) => {
  console.log(`后端服务已退出，退出码: ${code}`);
});

backendProcess.on('error', (err) => {
  console.error('启动后端服务失败:', err);
});