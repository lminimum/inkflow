import { apiClient } from './client';

/**
 * HTML生成初始请求参数接口 (用于标题、CSS、内容生成)
 */
export interface HTMLGenerateParams {
  theme: string;
  style: string;
  audience: string;
}

/**
 * 标题生成响应接口
 */
export interface TitleResponse {
  title: string;
}

/**
 * CSS生成响应接口
 */
export interface CSSResponse {
  css_style: string;
}

/**
 * 内容生成请求参数接口
 */
export interface ContentRequestParams {
  title: string;
  theme: string;
  style: string;
  audience: string;
}

/**
 * 内容生成响应接口
 */
export interface ContentResponse {
  content: string;
}

/**
 * 内容分割请求参数接口
 */
export interface SectionsRequestParams {
  content: string;
  num_sections: number;
}

/**
 * 内容分割响应接口
 */
export interface SectionsResponse {
  sections: string[]; // 文本内容片段列表
}

/**
 * 单个内容区块HTML生成请求参数接口
 */
export interface SectionHTMLRequestParams {
  title: string;
  description: string; // 内容描述，即分割后的文本片段
  css_style: string;
}

/**
 * 单个内容区块HTML生成响应接口
 */
export interface SectionHTMLResponse {
  html: string; // 单个内容区块的HTML片段
  file_path?: string; // 新增：后端返回的文件路径
}

/**
 * 构建最终HTML请求参数接口
 */
export interface BuildRequestParams {
  title: string;
  css_style: string;
  sections: string[]; // HTML内容片段列表 (由 generateSectionHtml 生成)
}

/**
 * 调用生成标题接口
 * @param params 生成参数 (theme, style, audience)
 * @returns 标题响应对象
 */
export const generateTitle = async (params: HTMLGenerateParams): Promise<TitleResponse> => {
  console.log('生成标题参数:', params);
  console.log('Attempting apiClient.post for /generate-html/title'); // 添加日志
  try {
    // apiClient.post returns the data payload directly due to interceptor
    const responseData: unknown = await apiClient.post('/generate-html/title', params); // 接收拦截器返回的数据，类型为 unknown
    console.log('generateTitle response data (after interceptor):', responseData);

    // 检查返回的数据是否符合 TitleResponse 结构
    if (!responseData || typeof responseData !== 'object' || typeof (responseData as any).title !== 'string' || !(responseData as any).title) {
      throw new Error("从后端获取标题失败或标题格式不正确。");
    }

    return responseData as TitleResponse; // 将检查后的数据断言为 TitleResponse
  } catch (error: any) {
    console.error('生成标题失败:', error);
    throw error;
  }
};

/**
 * 调用生成CSS接口
 * @param params 生成参数 (style)
 * @returns CSS样式响应对象
 */
export const generateCss = async (params: HTMLGenerateParams): Promise<CSSResponse> => {
  console.log('生成CSS参数:', params);
  console.log('Attempting apiClient.post for /generate-html/css'); // 添加日志
  try {
    // apiClient.post returns the data payload directly due to interceptor
    const responseData: unknown = await apiClient.post('/generate-html/css', params); // 接收拦截器返回的数据，类型为 unknown
    console.log('generateCss response data (after interceptor):', responseData);

    // 检查返回的数据是否符合 CSSResponse 结构
    if (!responseData || typeof responseData !== 'object' || typeof (responseData as any).css_style !== 'string' || !(responseData as any).css_style) {
      throw new Error("从后端获取CSS失败或CSS格式不正确。");
    }

    return responseData as CSSResponse; // 将检查后的数据断言为 CSSResponse
  } catch (error: any) {
    console.error('生成CSS失败:', error);
    throw error;
  }
};

/**
 * 调用生成内容接口
 * @param params 生成参数 (title, theme, style, audience)
 * @returns 内容响应对象
 */
export const generateContent = async (params: ContentRequestParams): Promise<ContentResponse> => {
  console.log('生成内容参数:', params);
  console.log('Attempting apiClient.post for /generate-html/content'); // 添加日志
  try {
    // apiClient.post returns the data payload directly due to interceptor
    const responseData: unknown = await apiClient.post('/generate-html/content', params); // 接收拦截器返回的数据，类型为 unknown
    console.log('generateContent response data (after interceptor):', responseData);

    // 检查返回的数据是否符合 ContentResponse 结构
    if (!responseData || typeof responseData !== 'object' || typeof (responseData as any).content !== 'string' || !(responseData as any).content) {
      throw new Error("从后端获取内容失败或内容格式不正确。");
    }

    return responseData as ContentResponse; // 将检查后的数据断言为 ContentResponse
  } catch (error: any) {
    console.error('生成内容失败:', error);
    throw error;
  }
};

/**
 * 调用内容分割接口
 * @param params 分割参数 (content, num_sections)
 * @returns 内容片段列表响应对象
 */
export const splitContentIntoSections = async (params: SectionsRequestParams): Promise<SectionsResponse> => {
  console.log('内容分割参数:', params);
  console.log('Attempting apiClient.post for /generate-html/sections'); // 添加日志
  try {
    // apiClient.post returns the data payload directly due to interceptor
    const responseData: unknown = await apiClient.post('/generate-html/sections', params); // 接收拦截器返回的数据，类型为 unknown
    console.log('splitContentIntoSections response data (after interceptor):', responseData);

    // 检查返回的数据是否符合 SectionsResponse 结构
    if (!responseData || typeof responseData !== 'object' || !Array.isArray((responseData as any).sections) || (responseData as any).sections.length === 0) {
      throw new Error("从后端分割内容失败或内容格式不正确。");
    }

    return responseData as SectionsResponse; // 将检查后的数据断言为 SectionsResponse
  } catch (error: any) {
    console.error('分割内容失败:', error);
    throw error;
  }
};

/**
 * 调用生成单个内容区块HTML接口
 * @param params 生成参数 (title, description, css_style)
 * @returns 单个内容区块HTML响应对象
 */
export const generateSectionHtml = async (params: SectionHTMLRequestParams): Promise<SectionHTMLResponse> => {
  try {
    const responseData: unknown = await apiClient.post('/generate-html/section_html', params);
    // 检查返回的数据格式
    if (responseData && typeof responseData === 'object' && typeof (responseData as any).html === 'string') {
      // 支持 file_path 字段
      return {
        html: (responseData as any).html,
        file_path: (responseData as any).file_path || undefined
      };
    } else {
      throw new Error("从后端获取内容区块HTML失败或格式不正确。");
    }
  } catch (error: any) {
    throw error;
  }
};