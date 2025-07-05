import requests
import logging
import os
from typing import List, Dict, Optional
from src.services.ai_providers import AIProviderFactory
from bs4 import BeautifulSoup
from readability import Document

class HotspotService:
    def __init__(self, config_path: str = 'config.json'):
        self.config = AIProviderFactory.load_config(config_path)
        self.data_sources = self.config.get('hotspot_sources', [
            {"name": "baidu", "type": "baidu"},
            {"name": "weibo", "type": "weibo"}
        ])

    def fetch_baidu_hot(self) -> List[Dict]:
        url = "https://top.baidu.com/api/board?platform=wise&tab=realtime"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            content = data.get("data", {}).get("cards", [{}])[0].get("content", [])
            return [
                {
                    "source": "baidu",
                    "title": item.get("word"),
                    "url": item.get("url"),
                    "hot_score": item.get("hotScore")
                }
                for item in content
            ][:10]
        except Exception as e:
            logging.error(f"获取百度热搜失败: {e}")
            return []

    def fetch_weibo_hot(self) -> List[Dict]:
        url = "https://weibo.com/ajax/side/hotSearch"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            realtime = data.get("data", {}).get("realtime", [])
            return [
                {
                    "source": "weibo",
                    "title": item.get("word"),
                    "url": f"https://s.weibo.com/weibo?q={item.get('word')}",
                    "hot_score": item.get("raw_hot")
                }
                for item in realtime
            ][:10]
        except Exception as e:
            logging.error(f"获取微博热搜失败: {e}")
            return []

    def fetch_all_hotspots(self) -> List[Dict]:
        all_hotspots = []
        for source in self.data_sources:
            if source["type"] == "baidu":
                all_hotspots.extend(self.fetch_baidu_hot())
            elif source["type"] == "weibo":
                all_hotspots.extend(self.fetch_weibo_hot())
        # 按热度排序，None 视为 0
        def safe_score(x):
            v = x.get("hot_score", 0)
            try:
                return int(v) if v is not None else 0
            except Exception:
                return 0
        all_hotspots.sort(key=safe_score, reverse=True)
        return all_hotspots

    def get_hotspot_content(self, url: str) -> str:
        """
        Fetches and extracts the main content from a given hotspot URL.
        """
        if not url or not url.startswith('http'):
            return "无效或空的URL。"

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()

            doc = Document(response.text)
            title = doc.title()
            
            summary_html = doc.summary(html_partial=True)
            
            soup = BeautifulSoup(summary_html, 'html.parser')
            content_text = soup.get_text('\\n', strip=True)

            if not content_text:
                return f"标题: {title}\\n\\n无法从此页面提取正文内容。可能是一个动态加载或非标准文章页面。"

            return f"标题: {title}\\n\\n{content_text}"

        except requests.exceptions.RequestException as e:
            logging.error(f"获取热点内容失败 (Request Error) for URL {url}: {e}")
            return "获取内容失败：网络请求错误或超时。"
        except Exception as e:
            logging.error(f"解析热点内容失败 for URL {url}: {e}")
            return "获取内容失败：页面解析时发生未知错误。"

    def analyze_hotspots(self, hotspots: List[Dict], ai_service: Optional[str] = None, ai_model: Optional[str] = None) -> str:
        if not hotspots:
            return "今日无热点数据可供分析。"
        # 构建 prompt
        prompt = self.build_prompt(hotspots)
        # 选择AI服务
        config = self.config
        service = ai_service if isinstance(ai_service, str) and ai_service else config.get('defaults', {}).get('ai_service')
        if not service:
            service = 'aliyun_bailian'
        if service is None:
            service = 'aliyun_bailian'
        service = str(service)
        model = ai_model if isinstance(ai_model, str) and ai_model else config.get('defaults', {}).get('ai_model')
        if not model:
            model = 'qwen-plus'
        if model is None:
            model = 'qwen-plus'
        model = str(model)
        assert isinstance(service, str) and service, 'service must be a non-empty string'
        assert isinstance(model, str) and model, 'model must be a non-empty string'
        provider = AIProviderFactory.get_provider(service, config)
        messages = [{"role": "user", "content": prompt}]
        return provider.generate_content(messages, model)

    def build_prompt(self, hotspots: List[Dict]) -> str:
        from datetime import datetime
        today_str = datetime.now().strftime('%Y-%m-%d')
        hotspots_str = "\n".join(
            f"{idx+1}. [{item['source']}] {item['title']} (热度: {item.get('hot_score', 'N/A')})"
            for idx, item in enumerate(hotspots)
        )
        return f"""
你是一位资深的市场与行业分析师。请根据以下提供的跨平台热点事件，生成一份专业的、结构清晰的日度分析报告。\n\n**今日热点榜单 ({today_str})：**\n{hotspots_str}\n\n**报告生成要求：**\n1.  **报告标题**：以 `# {today_str} 热点分析报告` 作为一级标题。\n2.  **重点事件分析**：\n    *   在 `## 重点事件分析` 二级标题下进行。\n    *   挑选出3-5个今天最具讨论价值和商业潜力的事件。优先选择同时在多个平台出现的跨平台热点。\n    *   对每个事件，使用三级标题 `### 1. 事件标题`。\n    *   为每个事件撰写约200字的深度分析，内容需覆盖：\n        *   **事件简述**：发生了什么？\n        *   **潜在影响**：可能对相关行业、公众情绪或市场格局产生什么影响？\n        *   **舆论焦点**：公众和媒体主要在讨论哪些方面？\n3.  **综合趋势与业务建议**：\n    *   在 `## 综合趋势与业务建议` 二级标题下进行。\n    *   结合所有热点，总结出1-2个当下的宏观趋势（如：公众关注点、技术风向、消费潮流等）。\n    *   基于这些趋势，为企业（如市场、运营、公关团队）提供2-3条具体、可执行的业务建议。\n\n请确保报告语言专业、分析深刻、逻辑严谨，并严格按照上述Markdown格式输出。\n""" 