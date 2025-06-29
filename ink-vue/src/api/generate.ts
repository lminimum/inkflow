import { type GenerateResponse } from '../types';
import {apiClient} from './client';

/**
 * 调用AI生成接口
 * @param prompt 用户输入的提示词
 * @param currentContent 当前编辑的内容
 * @returns 生成的内容结果
 */
export const generateContent = async (prompt: string, model: string = 'deepseek-ai/DeepSeek-R1-Distill-Qwen-32B', service: string = 'siliconflow'): Promise<GenerateResponse> => {
  try {
    return await apiClient.post('/generate', {
      prompt,
      model,
      service
    });
  } catch (error) {
    console.error('生成内容失败:', error);
    throw error;
  }
};