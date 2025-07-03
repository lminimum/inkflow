import { apiClient } from './client'

export interface HtmlToImageParams {
  html_path: string
  output_path?: string
  width?: number
  height?: number
  full_page?: boolean
  wait_time?: number
}

export interface HtmlToImageResponse {
  success: boolean
  output_path?: string
  image_url?: string
  file_size?: number
  msg?: string
}

/**
 * 调用后端 HTML 转图片接口
 * @param params html 转 image 参数
 * @returns HtmlToImageResponse
 */
export const htmlToImage = async (params: HtmlToImageParams): Promise<HtmlToImageResponse> => {
  const responseData: unknown = await apiClient.post('/html-to-image', params)
  if (
    responseData &&
    typeof responseData === 'object' &&
    'success' in responseData &&
    typeof (responseData as { success: unknown }).success === 'boolean'
  ) {
    return responseData as HtmlToImageResponse
  } else {
    throw new Error('后端返回格式不正确')
  }
}
