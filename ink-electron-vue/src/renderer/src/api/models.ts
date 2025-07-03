import { apiClient } from './client'
import { type ModelListResponse } from '../types'

export const fetchModels = async (): Promise<ModelListResponse> => {
  try {
    return await apiClient.get('/models')
  } catch (error) {
    console.error('获取模型列表失败:', error)
    throw error
  }
}
