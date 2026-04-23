from datetime import datetime, timedelta, timezone
import requests
import os
import json
from dotenv import load_dotenv
import dashscope

load_dotenv()
# 定义北京时间 UTC+8
beijing_tz = timezone(timedelta(hours=8), name="Asia/Shanghai")

def main():

    domain = "https://api.tikhub.dev"
    endpoint = "/api/v1/wechat_mp/web/fetch_mp_article_detail_json"
    share_url = f"https://mp.weixin.qq.com/s/MQQSNCrPfV-GW3kX7pEW5A"
    params = f"url={share_url}"
    headers = {"Authorization": f"Bearer {os.getenv('TIKHUB_API_KEY')}"}

    response = requests.get(
        f"{domain}{endpoint}?{params}",
        headers=headers
    )
    data = response.json()

    if data["code"] == 200:
        content = data["data"]["content"]["raw_content"][0]["text"]
        title = data["data"]["title"]
        author = data["data"]["author"]
        update = datetime.now(tz=beijing_tz)  # 文章更新时间
        create_time = datetime.now(tz=beijing_tz)  # 笔记创建时间
        
        if content:
            print(content)
        return {
            'title': title or '微信文章',
            'content': content or title or '微信内容（需登录查看完整内容）',
            'author': author,
            'update': update.strftime("%Y-%m-%d"),
            'create_time': create_time.strftime("%Y-%m-%d"),
            'url': share_url,
            'source': '微信',
        }
    else:
        print(f"Error: {data}")
        return {
            'title': '获取微信文章失败',
            'content': '获取微信文章失败',
            'author': '获取微信文章失败',
            'update': '获取微信文章失败',
            'create_time': '获取微信文章失败',
            'url': share_url,
            'source': '微信',
        }


if __name__ == "__main__":
    result = main()
    print(result)

