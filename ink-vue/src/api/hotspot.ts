import { apiClient } from './client';

export interface HotspotItem {
  source: string;
  title: string;
  url?: string;
  hot_score?: number | string | null;
}

export interface HotspotListResponse {
  hotspots: HotspotItem[];
}

export interface AnalyzeHotspotParams {
  ai_service?: string;
  ai_model?: string;
}

export interface AnalyzeHotspotResponse {
  report: string;
}

/**
 * 获取热点榜单
 */
export const getHotspots = async (): Promise<HotspotListResponse> => {
  return await apiClient.get('/hotspots');
};

/**
 * AI分析热点榜单
 */
export const analyzeHotspots = async (params: AnalyzeHotspotParams = {}): Promise<AnalyzeHotspotResponse> => {
  return await apiClient.post('/hotspots/analyze', params);
}; 