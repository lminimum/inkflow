import { apiClient } from './client'

export interface CookieAccount {
  name: string
  is_active: boolean
  is_valid?: boolean | null // null表示尚未验证
}

export interface ApiResponse<T = unknown> {
  success: boolean
  message?: string
  accounts?: T
  active_account?: string
  is_valid?: boolean
}

/**
 * 获取所有Cookie账号列表
 */
export const getCookieAccounts = async (): Promise<ApiResponse<CookieAccount[]>> => {
  try {
    return await apiClient.get('/cookies/accounts')
  } catch (error: unknown) {
    return { success: false, message: '请求失败' + error }
  }
}

/**
 * 添加一个新的Cookie账号
 * @param accountName 要添加的账号名称
 */
export const addCookieAccount = async (accountName: string): Promise<ApiResponse> => {
  try {
    return await apiClient.post('/cookies/add', { account_name: accountName })
  } catch (error: unknown) {
    return { success: false, message: '请求失败' + error }
  }
}

/**
 * 删除一个Cookie账号
 * @param accountName 要删除的账号名称
 */
export const deleteCookieAccount = async (accountName: string): Promise<ApiResponse> => {
  try {
    return await apiClient.post('/cookies/delete', { account_name: accountName })
  } catch (error: unknown) {
    return { success: false, message: '请求失败' + error }
  }
}

/**
 * 验证一个Cookie账号的有效性
 * @param accountName 要验证的账号名称
 */
export const validateCookieAccount = async (accountName: string): Promise<ApiResponse> => {
  try {
    return await apiClient.post('/cookies/validate', { account_name: accountName })
  } catch (error: unknown) {
    return { success: false, message: '请求失败' + error }
  }
}

/**
 * 设置当前活动的Cookie账号
 * @param accountName 要激活的账号名称
 */
export const setActiveCookieAccount = async (accountName: string): Promise<ApiResponse> => {
  try {
    return await apiClient.post('/cookies/set_active', { account_name: accountName })
  } catch (error: unknown) {
    return { success: false, message: '请求失败' + error }
  }
}

/**
 * 获取当前活动的Cookie账号
 */
export const getActiveCookieAccount = async (): Promise<ApiResponse> => {
  try {
    return await apiClient.get('/cookies/get_active')
  } catch (error: unknown) {
    return { success: false, message: '请求失败' + error }
  }
}
