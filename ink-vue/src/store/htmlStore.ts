import { defineStore } from 'pinia';

export const useHtmlStore = defineStore('html', {
    state: () => ({
        htmlSections: [] as string[], // 只保存每个HTML片段
    }),
    actions: {
        /**
         * 追加一个HTML片段到数组
         * @param html HTML片段
         */
        addHtmlSection(html: string) {
            this.htmlSections.push(html);
        },
        /**
         * 清空所有HTML片段
         */
        clearHtml() {
            this.htmlSections = [];
        }
    }
});
