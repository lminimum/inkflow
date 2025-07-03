import { defineStore } from 'pinia'

export interface HtmlSectionItem {
  html: string
  file_path?: string
  html_url?: string
  section_id?: string
}

export const useHtmlStore = defineStore('html', {
  state: () => ({
    htmlSections: [] as HtmlSectionItem[] // 保存每个HTML片段及其文件路径
  }),
  actions: {
    /**
     * 追加一个HTML片段到数组
     * @param item HTML片段及路径
     */
    addHtmlSection(item: HtmlSectionItem) {
      this.htmlSections.push(item)
    },
    /**
     * 清空所有HTML片段
     */
    clearHtml() {
      this.htmlSections = []
    }
  }
})
