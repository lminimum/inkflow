import requests
from deepseek import DeepSeek
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
import json
from datetime import datetime
import os
import logging
import markdown # 用于将Markdown转为HTML

# --- 配置日志 ---
# 设置日志记录，可以同时输出到控制台和文件
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("reporter.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def load_config():
    """从 config.json 加载配置"""
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        # 优先使用环境变量中的API Key
        config["deepseek_api_key"] = os.getenv("API-KEY", config.get("deepseek_api_key"))
        if not config.get("deepseek_api_key"):
            raise ValueError("DeepSeek API key not found in config.json or environment variables.")
        return config
    except FileNotFoundError:
        logging.error("错误: 配置文件 config.json 未找到。请从 config.example.json 复制并填写。")
        exit()
    except (json.JSONDecodeError, ValueError) as e:
        logging.error(f"错误: 配置文件解析失败: {e}")
        exit()

class HotspotReporter:
    def __init__(self, config):
        self.config = config
        try:
            self.ds = DeepSeek(api_key=self.config["deepseek_api_key"])
        except Exception as e:
            logging.error(f"初始化 DeepSeek 客户端失败: {e}")
            raise
        
        # 使用分派表（Dispatch Table）实现可扩展的数据源获取
        self.fetcher_map = {
            "baidu": self._fetch_baidu_hot,
            "weibo": self._fetch_weibo_hot,
        }
        os.makedirs(self.config["output_dir"], exist_ok=True)

    def _make_request(self, url, source_name):
        """统一的网络请求函数"""
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"获取 {source_name} 热搜失败: {e}")
            return None

    def fetch_hotspots(self, source):
        """从指定平台获取热点数据"""
        fetcher = self.fetcher_map.get(source)
        if fetcher:
            return fetcher()
        else:
            logging.warning(f"未找到名为 '{source}' 的数据源获取方法。")
            return []

    def _fetch_baidu_hot(self):
        """获取百度热搜"""
        url = "https://top.baidu.com/api/board?platform=wise&tab=realtime"
        data = self._make_request(url, "百度")
        if not data:
            return []
        
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

    def _fetch_weibo_hot(self):
        """获取微博热搜"""
        url = "https://weibo.com/ajax/side/hotSearch"
        data = self._make_request(url, "微博")
        if not data:
            return []

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

    def generate_report(self, all_hotspots):
        """使用DeepSeek生成综合分析报告"""
        if not all_hotspots:
            return "今日无热点数据可供分析。"

        prompt = self._build_prompt(all_hotspots)
        try:
            # 假设DeepSeek SDK的用法，请根据实际情况调整
            # response = self.ds.chat.completions.create(...)
            # 沿用原代码的ds.generate
            response = self.ds.generate(prompt, max_tokens=2500, model="deepseek-chat")
            report_text = response.choices[0].text
            # 确保报告以标题开头
            today_str = datetime.now().strftime('%Y-%m-%d')
            if not report_text.strip().startswith(f"# {today_str}"):
                report_text = f"# {today_str} 热点分析报告\n\n" + report_text
            return report_text
        except Exception as e:
            logging.error(f"DeepSeek 分析失败: {e}")
            return f"报告生成失败，错误: {e}"

    def _build_prompt(self, hotspots):
        """构建用于生成报告的提示词"""
        hotspots_str = "\n".join(
            f"{idx+1}. [{item['source']}] {item['title']} (热度: {item.get('hot_score', 'N/A')})"
            for idx, item in enumerate(hotspots)
        )
        today_str = datetime.now().strftime('%Y-%m-%d')

        return f"""
你是一位资深的市场与行业分析师。请根据以下提供的跨平台热点事件，生成一份专业的、结构清晰的日度分析报告。

**今日热点榜单 ({today_str})：**
{hotspots_str}

**报告生成要求：**
1.  **报告标题**：以 `# {today_str} 热点分析报告` 作为一级标题。
2.  **重点事件分析**：
    *   在 `## 重点事件分析` 二级标题下进行。
    *   挑选出3-5个今天最具讨论价值和商业潜力的事件。优先选择同时在多个平台出现的跨平台热点。
    *   对每个选定的事件，使用三级标题 `### 1. 事件标题`。
    *   为每个事件撰写约200字的深度分析，内容需覆盖：
        *   **事件简述**：发生了什么？
        *   **潜在影响**：可能对相关行业、公众情绪或市场格局产生什么影响？
        *   **舆论焦点**：公众和媒体主要在讨论哪些方面？
3.  **综合趋势与业务建议**：
    *   在 `## 综合趋势与业务建议` 二级标题下进行。
    *   结合所有热点，总结出1-2个当下的宏观趋势（如：公众关注点、技术风向、消费潮流等）。
    *   基于这些趋势，为企业（如市场、运营、公关团队）提供2-3条具体、可执行的业务建议。

请确保报告语言专业、分析深刻、逻辑严谨，并严格按照上述Markdown格式输出。
"""

    def save_report(self, report_content):
        """将报告保存到本地文件"""
        today = datetime.now().strftime("%Y-%m-%d")
        filename = os.path.join(self.config["output_dir"], f"{today}_hotspot_report.md")
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(report_content)
            logging.info(f"报告已成功保存到 {filename}")
        except IOError as e:
            logging.error(f"保存报告到 {filename} 失败: {e}")

    def send_report_email(self, report_content):
        """通过邮件发送报告，支持HTML格式"""
        email_config = self.config["email"]
        today = datetime.now().strftime("%Y-%m-%d")
        subject = f"{today} 热点分析报告"

        # 创建一个多部分消息
        msg = MIMEMultipart("alternative")
        msg["From"] = email_config["sender"]
        msg["To"] = email_config["receiver"]
        msg["Subject"] = subject

        # 创建纯文本和HTML版本
        text_part = MIMEText(report_content, "plain", "utf-8")
        html_part = MIMEText(markdown.markdown(report_content), "html", "utf-8")
        
        # 将两个版本都附加到邮件中，HTML版本会优先显示
        msg.attach(text_part)
        msg.attach(html_part)

        try:
            with smtplib.SMTP_SSL(email_config["smtp_server"], email_config["smtp_port"]) as server:
                server.login(email_config["sender"], email_config["password"])
                server.sendmail(
                    email_config["sender"],
                    email_config["receiver"].split(','), # 支持多个收件人
                    msg.as_string()
                )
            logging.info("邮件报告发送成功！")
        except smtplib.SMTPException as e:
            logging.error(f"邮件发送失败: {e}")

def main_job(config):
    """主任务流程"""
    logging.info("="*20 + " 开始执行热点报告任务 " + "="*20)
    
    reporter = HotspotReporter(config)

    all_hotspots = []
    for source in config["data_sources"]:
        hotspots = reporter.fetch_hotspots(source)
        if hotspots:
            all_hotspots.extend(hotspots)
            logging.info(f"从 {source} 成功获取到 {len(hotspots)} 条热点。")
    
    if not all_hotspots:
        logging.warning("未能从任何数据源获取到热点，任务提前结束。")
        return

    # 按热度分数排序（处理可能不存在'hot_score'的情况）
    all_hotspots.sort(key=lambda x: x.get("hot_score", 0), reverse=True)

    report = reporter.generate_report(all_hotspots)

    if "报告生成失败" not in report and "今日无热点" not in report:
        logging.info("报告生成成功。")
        reporter.save_report(report)
        reporter.send_report_email(report)
    else:
        logging.warning(f"报告生成存在问题: {report}")

    logging.info("="*20 + " 本次任务执行完成 " + "="*20 + "\n")

if __name__ == "__main__":
    try:
        config = load_config()
        
        # 首次立即执行
        main_job(config)

        # 设置定时任务
        schedule_times = config.get("schedule_times", ["10:00", "16:00"])
        for t in schedule_times:
            schedule.every().day.at(t).do(main_job, config)
        
        logging.info(f"热点监控系统已启动，将在每天的 {', '.join(schedule_times)} 执行。")
        
        while True:
            schedule.run_pending()
            time.sleep(30) # 减少CPU占用，30秒检查一次即可

    except (KeyboardInterrupt, SystemExit):
        logging.info("程序被用户中断，正在退出...")
    except Exception as e:
        logging.critical(f"程序启动时发生致命错误: {e}", exc_info=True)