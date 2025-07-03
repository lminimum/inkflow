const { spawn } = require('child_process');
const path = require('path');

// 启动前端服务
const frontendProcess = spawn('npm.cmd run dev', {
  cwd: path.join(__dirname, 'ink-electron-vue'),
  stdio: 'inherit',
  shell: true
});

frontendProcess.on('close', (code) => {
  console.log(`前端服务已退出，退出码: ${code}`);
});

frontendProcess.on('error', (err) => {
  console.error('启动前端服务失败:', err);
});