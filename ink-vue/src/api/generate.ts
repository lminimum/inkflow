import {  type Message } from '../types';
import {apiClient} from './client';

/**
 * 调用AI生成接口
 * @param messages 对话消息数组
 * @param model 使用的模型名称
 * @param service 使用的服务名称
 * @returns 生成的内容结果
 */
export const generateContent = async (messages: Message[], model: string = 'deepseek-ai/DeepSeek-R1-Distill-Qwen-32B', service: string = 'siliconflow'): Promise<any> => {
  console.log('generateContent', messages, model, service);
  try {
    const response = await apiClient.post('/generate', {
        messages,
        model,
        service
    }, { timeout: 30000 });
    return response;
  } catch (error: any) {
      let errorMessage = '生成内容失败';
      if (error.response && error.response.data && error.response.data.detail) {
        errorMessage += `: ${error.response.data.detail}`;
      } else if (error.message) {
        errorMessage += `: ${error.message}`;
      }
      console.error(errorMessage);
      throw new Error(errorMessage);
    }
};