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
    endpoint = "/api/v1/zhihu/web/fetch_column_article_detail"
    share_url = "https://zhuanlan.zhihu.com/p/2019366800190625461"
    params = f"article_id={share_url.split('/')[-1]}"
    headers = {"Authorization": f"Bearer {os.getenv('TIKHUB_API_KEY')}"}

    response = requests.get(
        f"{domain}{endpoint}?{params}",
        headers=headers
    )
    data = response.json()
    if data["code"] == 200:
        content = data["data"]["content"]
        title = data["data"]["title"]
        author = data["data"]["author"]["name"]
        update = datetime.fromtimestamp(data["data"]["updated"]) # 文章更新时间
        create_time = datetime.now(tz=beijing_tz)  # # 笔记收藏时间

        if content:
            print(content)
        return {
            'title': title or '知乎文章',
            'content': content or title or '知乎内容（需登录查看完整内容）',
            'author': author,
            'update': update.strftime("%Y-%m-%d"),
            'create_time': create_time.strftime("%Y-%m-%d"),
            'url': share_url,
            'source': '知乎',
        }
    else:
        print(f"Error: {data}")
        return {
            'title': '获取知乎文章失败',
            'content': '获取知乎文章失败',
            'author': '获取知乎文章失败',
            'update': '获取知乎文章失败',
            'create_time': '获取知乎文章失败',
            'url': share_url,
            'source': '知乎',
        }


if __name__ == "__main__":
    result = main()
    print(result)

