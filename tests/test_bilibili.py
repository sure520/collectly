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
    endpoint = "/api/v1/bilibili/web/fetch_one_video_v3"
    share_url = f"https://www.bilibili.com/video/BV1L7Jvz4ENz/?spm_id_from=333.1387.favlist.content.click&vd_source=ba077cb5048f0562112e9d805ce8721f"
    params = f"url={share_url}"
    headers = {"Authorization": f"Bearer {os.getenv('TIKHUB_API_KEY')}"}

    response = requests.get(
        f"{domain}{endpoint}?{params}",
        headers=headers
    )
    data = response.json()
    if data["code"] == 200:
        content = data["data"]["title"]  # 长视频视频没有文本内容，所以用标题代替
        title = data["data"]["title"]
        author = data["data"]["owner"]["name"]
        update = datetime.fromtimestamp(data["data"]["pubdate"])  # 文章更新时间
        create_time = datetime.now(tz=beijing_tz)  # 笔记创建时间
        
        if content:
            print(content)
        return {
            'title': title or 'bilibili视频',
            'content': content or title or 'bilibili视频内容（需登录查看完整内容）',
            'author': author,
            'update': update.strftime("%Y-%m-%d"),
            'create_time': create_time.strftime("%Y-%m-%d"),
            'url': share_url,
            'source': 'bilibili',
        }
    else:
        print(f"Error: {data}")
        return {
            'title': '获取bilibili视频失败',
            'content': '获取bilibili视频失败',
            'author': '获取bilibili视频失败',
            'update': '获取bilibili视频失败',
            'create_time': '获取bilibili视频失败',
            'url': share_url,
            'source': 'bilibili',
        }


if __name__ == "__main__":
    result = main()
    print(result)

