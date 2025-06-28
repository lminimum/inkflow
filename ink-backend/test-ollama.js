const fetch = require('node-fetch').default;

async function testOllamaAPI() {
  const url = 'http://localhost:3002/api/generate';
  const testPrompt = '请简要介绍水墨画的特点';

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        prompt: testPrompt,
        model: 'ollama'
      }),
    });

    const result = await response.json();
    console.log('测试结果:', result);

    if (response.ok) {
      console.log('Ollama API 测试成功!');
      console.log('生成内容:', result.content);
    } else {
      console.error('Ollama API 测试失败:', result.error);
    }
  } catch (error) {
    console.error('请求发生错误:', error);
  }
}

testOllamaAPI();