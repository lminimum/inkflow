import { defineStore } from 'pinia'

export interface HtmlSectionItem {
  html: string
  file_path?: string
  html_url?: string
  section_id?: string
}

export interface FormData {
  theme: string
  style: string
  audience: string
  numSections: number
  customStyle: string
  customAudience: string
}

export const useHtmlStore = defineStore('html', {
  state: () => ({
    htmlSections: [] as HtmlSectionItem[], // 保存每个HTML片段及其文件路径
    formData: {
      theme: '',
      style: '',
      audience: '',
      numSections: 1,
      customStyle: '',
      customAudience: ''
    } as FormData,
    sectionDescriptions: [] as string[]
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
      this.sectionDescriptions = []
    },
    /**
     * 保存表单数据
     * @param data 表单数据
     */
    saveFormData(data: FormData) {
      this.formData = { ...data }
    },
    /**
     * 保存段落描述
     * @param descriptions 段落描述数组
     */
    saveSectionDescriptions(descriptions: string[]) {
      this.sectionDescriptions = [...descriptions]
    },
    /**
     * 清空所有数据
     */
    clearAll() {
      this.htmlSections = []
      this.sectionDescriptions = []
      this.formData = {
        theme: '',
        style: '',
        audience: '',
        numSections: 1,
        customStyle: '',
        customAudience: ''
      }
    }
  }
})
