const { spawn } = require('child_process');
const path = require('path');

// 启动后端服务
const backendProcess = spawn('conda', [
  'run', '-n', 'ink-backend',
  'uvicorn', 'main:app',
  '--host', '0.0.0.0',
  '--port', '3000',
  '--reload'
], {
  cwd: path.join(__dirname, 'ink-backend'),
  stdio: 'inherit'
});

backendProcess.on('error', (err) => {
  console.error('后端服务启动失败:', err);
});

// 延迟2秒后启动前端服务
setTimeout(() => {
  const frontendProcess = spawn('npm', ['run', 'dev'], {
    cwd: path.join(__dirname, 'ink-vue'),
    stdio: 'inherit',
    shell: true
  });

  frontendProcess.on('error', (err) => {
    console.error('前端服务启动失败:', err);
  });

  // 监听前端进程退出
  frontendProcess.on('close', (code) => {
    console.log(`前端服务退出，代码: ${code}`);
    // 如果前端退出，也关闭后端
    backendProcess.kill();
  });
}, 2000);

// 监听后端进程退出
backendProcess.on('close', (code) => {
  console.log(`后端服务退出，代码: ${code}`);
});

// 处理Ctrl+C退出
process.on('SIGINT', () => {
  console.log('正在关闭所有服务...');
  backendProcess.kill();
  process.exit();
});