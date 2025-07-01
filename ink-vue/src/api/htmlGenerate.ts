import { apiClient } from './client';

/**
 * HTML生成请求参数接口
 */
export interface HTMLGenerateParams {
  theme: string;
  style: string;
  audience: string;
}

/**
 * 调用HTML生成接口
 * @param params 生成参数
 * @returns 生成的HTML内容
 */
export const generateHtml = async (params: HTMLGenerateParams): Promise<string> => {
  console.log('生成HTML参数:', params);
  try {
    const response = await apiClient.post('/api/generate-html', params, { timeout: 60000 });
    return response.data;
  } catch (error: any) {
    let errorMessage = 'HTML生成失败';
    if (error.response && error.response.data && error.response.data.detail) {
      errorMessage += `: ${error.response.data.detail}`;
    } else if (error.message) {
      errorMessage += `: ${error.message}`;
    }
    console.error(errorMessage);
    throw new Error(errorMessage);
  }
};