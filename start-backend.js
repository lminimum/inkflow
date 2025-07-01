const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// 检查后端目录是否存在
const backendDir = path.join(__dirname, 'ink-backend');
if (!fs.existsSync(backendDir)) {
  console.error(`错误: 后端目录不存在 - ${backendDir}`);
  process.exit(1);
}

// 检查requirements.txt是否存在并提示安装依赖
const requirementsPath = path.join(backendDir, 'requirements.txt');
if (fs.existsSync(requirementsPath)) {
  console.log('提示: 如需安装依赖，请运行: pip install -r', requirementsPath);
}

// 启动后端服务
console.log('正在启动后端服务...');
const backendProcess = spawn('uvicorn', [
  'src.app.main:app',  // 修正应用入口路径
  '--reload',
  '--host', '0.0.0.0',
  '--port', '3000'
], {
  cwd: backendDir,
  stdio: 'inherit',
  shell: process.platform === 'win32'  // Windows系统需要shell:true
});

backendProcess.on('spawn', () => {
  console.log('后端服务启动成功，PID:', backendProcess.pid);
  console.log('访问地址: http://localhost:3000');
});

backendProcess.on('close', (code) => {
  console.log(`后端服务已退出，退出码: ${code}`);
  if (code !== 0) {
    console.log('服务异常退出，可能的原因: 端口被占用或依赖未安装');
  }
});

backendProcess.on('error', (err) => {
  console.error('启动后端服务失败:', err);
  if (err.code === 'ENOENT') {
    console.error('找不到uvicorn命令，请确保已安装: pip install uvicorn');
  }
});

// 处理进程退出信号
process.on('SIGINT', () => {
  console.log('正在停止后端服务...');
  backendProcess.kill();
  process.exit(0);
});