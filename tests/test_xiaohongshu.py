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
    endpoint = "/api/v1/xiaohongshu/app/get_note_info"
    share_url = "https://www.xiaohongshu.com/explore/69cbc340000000001a02329e?xsec_token=AB6PThxy4qFPZb2koEH4GWhkDIqU-4ImQlD4wxxS6HjVs=&xsec_source=pc_collect"
    params = f"note_id={share_url.split('?')[0].split('/')[-1]}"
    headers = {"Authorization": f"Bearer {os.getenv('TIKHUB_API_KEY')}"}

    response = requests.get(
        f"{domain}{endpoint}?{params}",
        headers=headers
    )
    data = response.json()
    if data["code"] == 200:
        content = data["data"]["data"][0]["note_list"][0]["desc"]
        title = data["data"]["data"][0]["note_list"][0]["title"]
        author = data["data"]["data"][0]["note_list"][0]["user"]["name"]
        update = datetime.fromtimestamp(data["data"]["data"][0]["note_list"][0]["time"]) # 文章更新时间
        note_create_time = datetime.now(tz=beijing_tz)  # # 笔记收藏时间

        if content:
            print(content)
        return {
            'title': title or '小红书文章',
            'content': content or title or '小红书内容（需登录查看完整内容）',
            'author': author,
            'update': update.strftime("%Y-%m-%d"),
            'create_time': note_create_time.strftime("%Y-%m-%d"),
            'url': share_url,
            'source': '小红书',
        }
    else:
        print(f"Error: {data}")
        return {
            'title': '获取知乎文章失败',
            'content': '获取小红书文章失败',
            'author': '获取小红书文章失败',
            'update': '获取小红书文章失败',
            'create_time': '获取小红书文章失败',
            'url': share_url,
            'source': '小红书',
        }


if __name__ == "__main__":
    result = main()
    print(result)

