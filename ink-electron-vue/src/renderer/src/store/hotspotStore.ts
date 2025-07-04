import { defineStore } from 'pinia'
import { getHotspots, type HotspotItem } from '../api/hotspot'

interface HotspotState {
  hotspots: HotspotItem[]
  fetched: boolean
  loading: boolean
  error: string | null
}

export const useHotspotStore = defineStore('hotspots', {
  state: (): HotspotState => ({
    hotspots: [],
    fetched: false,
    loading: false,
    error: null
  }),

  getters: {
    baiduHotspots: (state): HotspotItem[] => {
      return state.hotspots.filter((h) => h.source === 'baidu').slice(0, 8)
    },
    weiboHotspots: (state): HotspotItem[] => {
      return state.hotspots.filter((h) => h.source === 'weibo').slice(0, 5)
    },
    groupedHotspots: (state): Record<string, HotspotItem[]> => {
      if (!state.hotspots) return {}
      return state.hotspots.reduce(
        (acc, item) => {
          const source = item.source || '其他'
          if (!acc[source]) {
            acc[source] = []
          }
          acc[source].push(item)
          return acc
        },
        {} as Record<string, HotspotItem[]>
      )
    }
  },

  actions: {
    async fetchHotspots() {
      if (this.fetched || this.loading) {
        return // 如果已经获取过或正在获取，则不执行
      }

      this.loading = true
      this.error = null
      try {
        const response = await getHotspots()
        this.hotspots = response.hotspots
        this.fetched = true
      } catch (err) {
        this.error = '无法加载热点内容，请稍后再试。'
        console.error('Failed to fetch hotspots:', err)
      } finally {
        this.loading = false
      }
    }
  }
})
