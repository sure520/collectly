import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from app.services.platform_parser import PlatformParser

def print_result(title: str, result):
    """打印解析结果的所有属性"""
    print(f"\n{title}解析成功:")
    print(f"  标题：{result.title}")
    print(f"  内容：{result.content[:100]}..." if len(result.content) > 100 else f"  内容：{result.content}")
    print(f"  作者：{result.author}")
    print(f"  更新时间：{result.update}")
    print(f"  创建时间：{result.create_time}")
    print(f"  原文链接：{result.url}")
    print(f"  来源平台：{result.source}")
    print(f"  标签：{result.tags}")
    print(f"  知识点：{result.knowledge_points}")
    print(f"  摘要：{result.summary}")

async def test_parser():
    """测试平台链接解析功能"""
    parser = PlatformParser()
    
    # # 测试抖音链接
    # print("=" * 60)
    # print("测试抖音链接...")
    # douyin_url = "https://www.douyin.com/user/self?from_tab_name=main&modal_id=7629643476111543595&showTab=favorite_collection"
    # try:
    #     douyin_result = await parser.parse(douyin_url)
    #     print_result("抖音", douyin_result)
    # except Exception as e:
    #     print(f"抖音解析失败：{e}")
    
    # # 测试 B 站链接
    # print("\n" + "=" * 60)
    # print("测试 B 站链接...")
    # bilibili_url = "https://www.bilibili.com/video/BV1L7Jvz4ENz/?spm_id_from=333.1387.favlist.content.click&vd_source=ba077cb5048f0562112e9d805ce8721f"
    # try:
    #     bilibili_result = await parser.parse(bilibili_url)
    #     print_result("B 站", bilibili_result)
    # except Exception as e:
    #     print(f"B 站解析失败：{e}")
    
    # # 测试知乎链接
    # print("\n" + "=" * 60)
    # print("测试知乎链接...")
    # zhihu_url = "https://zhuanlan.zhihu.com/p/2019366800190625461"
    # try:
    #     zhihu_result = await parser.parse(zhihu_url)
    #     print_result("知乎", zhihu_result)
    # except Exception as e:
    #     print(f"知乎解析失败：{e}")

    # 测试微信公众号链接
    print("\n" + "=" * 60)
    print("测试微信公众号链接...")
    wechat_url = "https://mp.weixin.qq.com/s/MQQSNCrPfV-GW3kX7pEW5A"
    try:
        wechat_result = await parser.parse(wechat_url)
        print_result("微信公众号", wechat_result)
    except Exception as e:
        print(f"微信公众号解析失败：{e}")
    
    # # 测试小红书链接
    # print("\n" + "=" * 60)
    # print("测试小红书链接...")
    # xiaohongshu_url = "https://www.xiaohongshu.com/explore/69cbc340000000001a02329e?xsec_token=AB6PThxy4qFPZb2koEH4GWhkDIqU-4ImQlD4wxxS6HjVs=&xsec_source=pc_collect"
    # try:
    #     xiaohongshu_result = await parser.parse(xiaohongshu_url)
    #     print_result("小红书", xiaohongshu_result)
    # except Exception as e:
    #     print(f"小红书解析失败：{e}")

if __name__ == "__main__":
    asyncio.run(test_parser())
