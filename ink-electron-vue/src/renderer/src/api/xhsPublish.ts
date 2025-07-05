import { apiClient } from './client'

export interface XHSPublishParams {
  title: string
  content: string
  topics?: string[]
  location?: string
  images?: string[]
  videos?: string[]
}

export interface XHSPublishResponse {
  success: boolean
  message: string
  output?: string
  error?: string
}

/**
 * 调用后端小红书发布接口
 * @param params 发布参数
 * @returns 发布结果
 */
export const publishToXHS = async (params: XHSPublishParams): Promise<XHSPublishResponse> => {
  try {
    const responseData = await apiClient.post('/publish/xhs', params)

    if (
      responseData &&
      typeof responseData === 'object' &&
      'success' in responseData &&
      typeof (responseData as { success: unknown }).success === 'boolean'
    ) {
      return responseData as unknown as XHSPublishResponse
    } else {
      throw new Error('后端返回格式不正确')
    }
  } catch (error) {
    if (error instanceof Error) {
      return {
        success: false,
        message: `发布请求失败: ${error.message}`
      }
    }
    return {
      success: false,
      message: '发布请求失败，未知错误'
    }
  }
}
