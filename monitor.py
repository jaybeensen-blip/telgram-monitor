import os
import urllib.request
import urllib.error
import json

BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")

def send_telegram_message(message: str):
    if not BOT_TOKEN or not CHAT_ID:
        raise ValueError("缺少 Telegram 配置环境变量 (TG_BOT_TOKEN or TG_CHAT_ID)")
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        # Added a 10-second timeout to prevent hanging
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                print("✅ 消息推送成功！")
            else:
                print(f"⚠️ 消息推送返回状态码: {response.status}")
                
    except urllib.error.HTTPError as e:
        # Handles HTTP errors (e.g., 400 Bad Request, 401 Unauthorized)
        error_info = e.read().decode('utf-8')
        print(f"❌ Telegram API 错误: {e.code} - {error_info}")
    except urllib.error.URLError as e:
        # Handles network-level errors (e.g., DNS failure, timeout)
        print(f"❌ 网络连接失败: {e.reason}")

def run_monitor():
    status_summary = (
        "🔔 *GitHub Actions 自动化巡检报表*\n\n"
        "• *监控状态*：服务运行正常\n"
        "• *触发来源*：Python urllib 本地测试"
    )
    return status_summary

if __name__ == "__main__":
    try:
        report = run_monitor()
        send_telegram_message(report)
    except Exception as e:
        print(f"执行失败: {e}")