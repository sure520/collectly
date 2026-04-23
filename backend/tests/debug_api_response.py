import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
import aiohttp
import json
from datetime import datetime
from app.utils.config import get_settings

settings = get_settings()

async def debug_api_responses():
    """调试并记录 TikHub API 返回的原始内容到日志文件"""
    
    log_file = Path(__file__).parent / "api_debug_log.txt"
    
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"=== TikHub API 调试日志 ===\n")
        f.write(f"生成时间: {datetime.now()}\n")
        f.write(f"API URL: {settings.TIKHUB_API_URL}\n")
        f.write(f"API Key: {settings.TIKHUB_API_KEY[:10]}...\n")
        f.write("=" * 80 + "\n\n")
        
        # 测试抖音
        f.write("\n" + "=" * 80 + "\n")
        f.write("【1. 抖音 API 测试】\n")
        f.write("=" * 80 + "\n")
        douyin_url = "https://www.douyin.com/user/self?from_tab_name=main&modal_id=7629643476111543595&showTab=favorite_collection"
        f.write(f"测试链接: {douyin_url}\n\n")
        
        try:
            async with aiohttp.ClientSession() as session:
                endpoint = "/api/v1/douyin/web/fetch_one_video_by_share_url"
                params = f"share_url={douyin_url}"
                headers = {"Authorization": f"Bearer {settings.TIKHUB_API_KEY}"}
                
                f.write(f"请求 URL: {settings.TIKHUB_API_URL}{endpoint}?{params}\n")
                f.write(f"请求头: {headers}\n\n")
                
                async with session.get(
                    f"{settings.TIKHUB_API_URL}{endpoint}?{params}",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    f.write(f"响应状态码: {response.status}\n")
                    f.write(f"响应头: {dict(response.headers)}\n\n")
                    
                    data = await response.json()
                    f.write(f"响应 JSON:\n")
                    f.write(json.dumps(data, ensure_ascii=False, indent=2))
                    f.write("\n\n")
                    
                    if data.get("code") == 200:
                        f.write("✓ API 调用成功\n")
                        aweme_detail = data["data"]["aweme_detail"]
                        f.write(f"视频标题: {aweme_detail.get('caption', 'N/A')}\n")
                        f.write(f"作者: {aweme_detail.get('author', {}).get('nickname', 'N/A')}\n")
                        f.write(f"创建时间: {aweme_detail.get('create_time', 'N/A')}\n")
                        
                        video_urls = aweme_detail.get("music", {}).get("play_url", {}).get("url_list", [])
                        f.write(f"视频 URL 列表: {video_urls}\n")
                    else:
                        f.write(f"✗ API 调用失败\n")
                        f.write(f"错误码: {data.get('code', 'N/A')}\n")
                        f.write(f"错误信息: {data.get('message', 'N/A')}\n")
        except Exception as e:
            f.write(f"✗ 请求异常: {str(e)}\n")
        
        # 测试B站
        f.write("\n" + "=" * 80 + "\n")
        f.write("【2. B站 API 测试】\n")
        f.write("=" * 80 + "\n")
        bilibili_url = "https://www.bilibili.com/video/BV1L7Jvz4ENz/?spm_id_from=333.1387.favlist.content.click&vd_source=ba077cb5048f0562112e9d805ce8721f"
        f.write(f"测试链接: {bilibili_url}\n\n")
        
        try:
            async with aiohttp.ClientSession() as session:
                endpoint = "/api/v1/bilibili/web/fetch_one_video_v3"
                params = f"url={bilibili_url}"
                headers = {"Authorization": f"Bearer {settings.TIKHUB_API_KEY}"}
                
                f.write(f"请求 URL: {settings.TIKHUB_API_URL}{endpoint}?{params}\n")
                f.write(f"请求头: {headers}\n\n")
                
                async with session.get(
                    f"{settings.TIKHUB_API_URL}{endpoint}?{params}",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    f.write(f"响应状态码: {response.status}\n")
                    f.write(f"响应头: {dict(response.headers)}\n\n")
                    
                    data = await response.json()
                    f.write(f"响应 JSON:\n")
                    f.write(json.dumps(data, ensure_ascii=False, indent=2))
                    f.write("\n\n")
                    
                    if data.get("code") == 200:
                        f.write("✓ API 调用成功\n")
                        video_detail = data["data"]
                        f.write(f"视频标题: {video_detail.get('title', 'N/A')}\n")
                        f.write(f"作者: {video_detail.get('owner', {}).get('name', 'N/A')}\n")
                        f.write(f"发布时间: {video_detail.get('pubdate', 'N/A')}\n")
                    else:
                        f.write(f"✗ API 调用失败\n")
                        f.write(f"错误码: {data.get('code', 'N/A')}\n")
                        f.write(f"错误信息: {data.get('message', 'N/A')}\n")
        except Exception as e:
            f.write(f"✗ 请求异常: {str(e)}\n")
        
        # 测试知乎
        f.write("\n" + "=" * 80 + "\n")
        f.write("【3. 知乎 API 测试】\n")
        f.write("=" * 80 + "\n")
        zhihu_url = "https://zhuanlan.zhihu.com/p/2019366800190625461"
        f.write(f"测试链接: {zhihu_url}\n\n")
        
        try:
            async with aiohttp.ClientSession() as session:
                article_id = zhihu_url.split("/")[-1]
                endpoint = "/api/v1/zhihu/web/fetch_column_article_detail"
                params = f"article_id={article_id}"
                headers = {"Authorization": f"Bearer {settings.TIKHUB_API_KEY}"}
                
                f.write(f"请求 URL: {settings.TIKHUB_API_URL}{endpoint}?{params}\n")
                f.write(f"请求头: {headers}\n\n")
                
                async with session.get(
                    f"{settings.TIKHUB_API_URL}{endpoint}?{params}",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    f.write(f"响应状态码: {response.status}\n")
                    f.write(f"响应头: {dict(response.headers)}\n\n")
                    
                    data = await response.json()
                    f.write(f"响应 JSON (前5000字符):\n")
                    json_str = json.dumps(data, ensure_ascii=False, indent=2)
                    f.write(json_str[:5000])
                    if len(json_str) > 5000:
                        f.write(f"\n... (内容过长，已截断，总长度: {len(json_str)} 字符)\n")
                    f.write("\n\n")
                    
                    if data.get("code") == 200:
                        f.write("✓ API 调用成功\n")
                        article_detail = data["data"]
                        f.write(f"文章标题: {article_detail.get('title', 'N/A')}\n")
                        f.write(f"作者: {article_detail.get('author', {}).get('name', 'N/A')}\n")
                        f.write(f"更新时间: {article_detail.get('updated', 'N/A')}\n")
                        content = article_detail.get("content", "")
                        f.write(f"内容长度: {len(content)} 字符\n")
                    else:
                        f.write(f"✗ API 调用失败\n")
                        f.write(f"错误码: {data.get('code', 'N/A')}\n")
                        f.write(f"错误信息: {data.get('message', 'N/A')}\n")
        except Exception as e:
            f.write(f"✗ 请求异常: {str(e)}\n")
    
    print(f"调试日志已保存到: {log_file}")
    print(f"请查看日志文件了解 API 返回的详细内容")

if __name__ == "__main__":
    asyncio.run(debug_api_responses())
