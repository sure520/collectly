from datetime import datetime, timedelta, timezone
import requests
import os
import json
from dotenv import load_dotenv
import dashscope

load_dotenv()
# 定义北京时间 UTC+8
beijing_tz = timezone(timedelta(hours=8), name="Asia/Shanghai")

from tikhub import DouyinAPI

def get_text_from_video(video_url: str) -> str:
    """
    从视频URL中提取文本
    """
    messages = [
        {
            "role": "system",
            "content": [
                # 此处用于配置定制化识别的Context
                {"text": ""},
            ]
        },
        {
            "role": "user",
            "content": [
                {"audio": video_url},
            ]
        }
    ]
    response = dashscope.MultiModalConversation.call(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        model="qwen3-asr-flash",
        messages=messages,
        result_format="message",
        asr_options={
            "language": "zh", # 可选，若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率
            "enable_lid":True,
            "enable_itn":False
        }
    )
    if response.status_code == 200:
        text = response.output["choices"][0]["message"]["content"][0]["text"]
        return text
    else:
        print(f"Error: {response}")
        return ""
    

def main():

    domain = "https://api.tikhub.dev"
    endpoint = "/api/v1/douyin/web/fetch_one_video_by_share_url"
    share_url = f"https://www.douyin.com/user/self?modal_id=7626388390761668091&showSubTab=favorite_folder&showTab=favorite_collection"
    params = f"share_url={share_url}"
    headers = {"Authorization": f"Bearer {os.getenv('TIKHUB_API_KEY')}"}

    response = requests.get(
        f"{domain}{endpoint}?{params}",
        headers=headers
    )
    data = response.json()
    if data["code"] == 200:
        video_url = data["data"]["aweme_detail"]["music"]["play_url"]["url_list"][0]
        text = get_text_from_video(video_url)
        title = data["data"]["aweme_detail"]["caption"]
        author = data["data"]["aweme_detail"]["music"]["author"]
        update = datetime.fromtimestamp(data["data"]["aweme_detail"]["create_time"]) # 文章更新时间
        create_time = datetime.now(tz=beijing_tz)  # # 笔记收藏时间

        if text:
            print(text)
        return {
            'title': title or '抖音视频',
            'content': text or title or '抖音视频内容（需登录查看完整内容）',
            'author': author,
            'update': update.strftime("%Y-%m-%d"),
            'create_time': create_time.strftime("%Y-%m-%d"),
            'url': share_url,
            'source': '抖音',
        }
    else:
        print(f"Error: {data['message']}")
        return {
            'title': '获取抖音视频失败',
            'content': '获取抖音视频失败',
            'author': '获取抖音视频失败',
            'update': '获取抖音视频失败',
            'create_time': '获取抖音视频失败',
            'url': share_url,
            'source': '抖音',
        }


if __name__ == "__main__":
    result = main()
    print(result)
