require('dotenv').config();
const express = require('express');
const cors = require('cors');
const { OpenAI } = require('@langchain/openai');
const { Anthropic } = require('@langchain/anthropic');
const { Ollama } = require('@langchain/ollama');
const fetch = require('node-fetch').default;

const app = express();
const port = process.env.PORT || 3002;

app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
  res.send('AI Content Creation Backend is running!');
});

app.get('/api/models', async (req, res) => {
  try {
    const response = await fetch('https://ollama.campus.lk233.link/v1/models');
    const data = await response.json();
    res.json(data);
  } catch (error) {
    console.error('Error fetching models:', error);
    res.status(500).json({ error: 'Failed to fetch models list' });
  }
});

app.post('/api/generate', async (req, res) => {
  console.log('收到生成请求:', { model: req.body.model, promptPreview: req.body.prompt?.substring(0, 50) });
  try {
    const { prompt, model } = req.body;
    
    if (!prompt || !model) {
      console.log('缺少必要参数:', { hasPrompt: !!prompt, hasModel: !!model });
      return res.status(400).json({ error: 'Prompt and model are required' });
    }
    console.log('开始初始化模型:', model);

    let llm;
    switch (model) {
      case 'openai':
        llm = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
        break;
      case 'anthropic':
        llm = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
        break;
      case 'ollama':
        llm = new Ollama({
          baseUrl: 'https://ollama.campus.lk233.link/',
          model: 'llama3.2:latest',
          timeout: 30000
        });
        console.log('Ollama模型初始化完成，准备调用API');
        break;
      default:
        return res.status(400).json({ error: 'Unsupported model' });
    }

    console.log('开始调用模型生成内容...');
    const response = await llm.invoke(prompt);
    console.log('模型生成成功，响应长度:', response.length);
    res.json({ content: response });
  } catch (error) {
    console.error('生成内容错误:', error.stack);
    res.status(500).json({ error: 'Failed to generate content', details: error.message });
  }
});

app.listen(port, () => {
  console.log(`Backend server running on http://localhost:${port}`);
});