import asyncio
from app.services.platform_parser import PlatformParser
from app.services.content_manager import ContentManager

async def test_content_manager():
    """测试内容存储和去重机制"""
    parser = PlatformParser()
    content_manager = ContentManager()
    
    # 测试链接
    test_urls = [
        "https://zhuanlan.zhihu.com/p/2019366800190625461",  # 知乎
        "https://www.bilibili.com/video/BV1L7Jvz4ENz/?spm_id_from=333.1387.favlist.content.click&vd_source=ba077cb5048f0562112e9d805ce8721f"  # B站
    ]
    
    # 解析并存储内容
    content_ids = []
    for url in test_urls:
        print(f"解析并存储: {url}")
        try:
            content = await parser.parse(url)
            content_id = await content_manager.save(content)
            content_ids.append(content_id)
            print(f"存储成功，ID: {content_id}")
        except Exception as e:
            print(f"存储失败: {e}")
    
    # 测试去重
    print("\n测试去重...")
    try:
        # 再次存储相同的内容
        content = await parser.parse(test_urls[0])
        duplicate_id = await content_manager.save(content)
        print(f"再次存储相同内容，ID: {duplicate_id}")
        print(f"去重测试: {'成功' if duplicate_id == content_ids[0] else '失败'}")
    except Exception as e:
        print(f"去重测试失败: {e}")
    
    # 测试获取内容
    print("\n测试获取内容...")
    for content_id in content_ids:
        try:
            content = await content_manager.get(content_id)
            print(f"获取内容成功: {content.title}")
        except Exception as e:
            print(f"获取内容失败: {e}")
    
    # 测试获取所有内容
    print("\n测试获取所有内容...")
    try:
        all_content = await content_manager.get_all()
        print(f"获取所有内容成功，共 {len(all_content)} 条")
        for item in all_content:
            print(f"  - {item['title']} ({item['source']})")
    except Exception as e:
        print(f"获取所有内容失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_content_manager())