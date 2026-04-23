import httpx
import asyncio
import json


async def test_parse():
    url = "http://localhost:8000/parse"
    
    # 测试抖音链接
    test_urls = [
        "https://www.douyin.com/user/self?from_tab_name=main&modal_id=7626388390761668091&showSubTab=video&showTab=favorite_collection",
        "https://www.example.com",
        "https://httpbin.org/html"
    ]
    
    async with httpx.AsyncClient() as client:
        for test_url in test_urls:
            print(f"\n{'='*60}")
            print(f"测试URL: {test_url}")
            print('='*60)
            
            try:
                response = await client.post(
                    url,
                    json={"url": test_url, "include_summary": True, "timeout": 30},
                    timeout=60.0
                )
                
                result = response.json()
                print(f"状态: {'成功' if result['success'] else '失败'}")
                print(f"标题: {result.get('title', 'N/A')}")
                print(f"作者: {result.get('author', 'N/A')}")
                print(f"字数: {result.get('word_count', 0)}")
                print(f"处理时间: {result.get('processing_time', 0):.2f}秒")
                
                if result.get('summary'):
                    print(f"\n摘要:\n{result['summary'][:200]}...")
                
                if result.get('content'):
                    content_preview = result['content'][:300].replace('\n', ' ')
                    print(f"\n内容预览:\n{content_preview}...")
                
                if result.get('error'):
                    print(f"\n错误: {result['error']}")
                    
            except Exception as e:
                print(f"请求异常: {e}")


async def test_health():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:8000/health")
            print(f"健康检查: {response.json()}")
        except Exception as e:
            print(f"健康检查失败: {e}")


if __name__ == "__main__":
    print("开始测试链接解析服务...")
    asyncio.run(test_health())
    asyncio.run(test_parse())