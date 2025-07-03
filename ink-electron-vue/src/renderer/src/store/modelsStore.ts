import { defineStore } from 'pinia'
import { fetchModels } from '../api/models'
import { type ModelListResponse } from '../types'

export const useModelsStore = defineStore('models', {
  state: () => ({
    models: {} as ModelListResponse,
    isLoading: false,
    error: null as string | null
  }),
  getters: {
    modelOptions(state) {
      const options: { value: string; label: string; provider: string }[] = []
      for (const service in state.models) {
        state.models[service].forEach((model) => {
          options.push({
            value: model,
            label: model
              .split('-')
              .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
              .join(' '),
            provider: service
          })
        })
      }
      return options
    }
  },
  actions: {
    async loadModels() {
      this.isLoading = true
      this.error = null
      try {
        this.models = await fetchModels()
      } catch (err) {
        this.error = 'Failed to load models'
        console.error(err)
      } finally {
        this.isLoading = false
      }
    }
  }
})
