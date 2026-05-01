import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
import re
from app.services.platform_parser import PlatformParser, process_url


def load_test_urls() -> dict:
    url_file = Path(__file__).parent.parent.parent / "tests" / "test_url.txt"
    content = url_file.read_text(encoding="utf-8")

    sections = {}
    current_platform = None
    current_type = None
    buffer = []

    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue

        platform_match = re.match(r"^(.+?)测试用例（(.+?)）[：:]$", line)
        if platform_match:
            if current_platform and buffer:
                sections.setdefault(current_platform, {})[current_type] = list(buffer)
                buffer = []
            current_platform = platform_match.group(1)
            current_type = platform_match.group(2)
            continue

        platform_match2 = re.match(r"^(.+?)测试用例[：:]$", line)
        if platform_match2:
            if current_platform and buffer:
                sections.setdefault(current_platform, {})[current_type or "默认"] = list(buffer)
                buffer = []
            current_platform = platform_match2.group(1)
            current_type = None
            continue

        url = line.strip()
        if url.startswith("http"):
            buffer.append(url)

    if current_platform and buffer:
        sections.setdefault(current_platform, {})[current_type or "默认"] = list(buffer)

    return sections


def print_result(title: str, result):
    print(f"\n  ✅ {title} 解析成功:")
    print(f"     标题：{result.title}")
    content_preview = result.content[:80].replace("\n", " ") if result.content else "(空)"
    print(f"     内容：{content_preview}...")
    print(f"     作者：{result.author}")
    print(f"     来源：{result.source}")
    print(f"     标签数：{len(result.tags)}")
    print(f"     知识点数：{len(result.knowledge_points)}")


async def test_url_processing():
    print("=" * 60)
    print("1. 测试 URL 处理函数 (process_url)")
    print("=" * 60)

    test_cases = [
        ("抖音短链", "https://v.douyin.com/GiwKX3xWbD4/"),
        ("B站短链", "https://b23.tv/XZeyxg6"),
        ("B站长链带追踪", "https://www.bilibili.com/video/BV1aTp1zRENj/?spm_id_from=333.1387.favlist.content.click&vd_source=ba077cb5048f0562112e9d805ce8721f"),
        ("B站长链带分P", "https://www.bilibili.com/video/BV1aTp1zRENj?spm_id_from=333.788.videopod.episodes&vd_source=ba077cb5048f0562112e9d805ce8721f&p=2"),
        ("知乎链接带追踪", "https://zhuanlan.zhihu.com/p/731785401?share_code=UaCZQIyom9Iu&utm_psn=2031311064101544538"),
        ("小红书链接", "https://www.xiaohongshu.com/explore/69e4ff92000000002102c20a?xsec_token=ABNq2ZZ0Q9oow_EwSy-N9d7LTDU5gStg381dNEAIv6LwU=&xsec_source=pc_collect"),
        ("抖音长链带modal_id", "https://www.douyin.com/user/self?modal_id=7627013109139475762&showSubTab=favorite_folder&showTab=favorite_collection"),
    ]

    for name, raw_url in test_cases:
        try:
            cleaned = process_url(raw_url)
            print(f"  [{name}]")
            print(f"    原始: {raw_url[:80]}")
            print(f"    处理: {cleaned}")
        except Exception as e:
            print(f"  [{name}] 处理失败: {e}")
        print()


async def test_platform_parsing():
    print("=" * 60)
    print("2. 测试平台解析 (调用 TikHub API)")
    print("=" * 60)

    sections = load_test_urls()
    parser = PlatformParser()

    for platform, types in sections.items():
        print(f"\n{'─' * 50}")
        print(f"  📦 {platform}")
        print(f"{'─' * 50}")

        for url_type, urls in types.items():
            print(f"\n  📂 {url_type} ({len(urls)} 个)")

            for i, url in enumerate(urls, 1):
                print(f"\n  ── 测试 #{i} ──")
                print(f"     链接: {url[:90]}...")
                try:
                    result = await parser.parse(url)
                    print_result(f"{platform}", result)
                except Exception as e:
                    print(f"  ❌ 解析失败: {e}")


async def main():
    await test_url_processing()
    print("\n\n")
    await test_platform_parsing()


if __name__ == "__main__":
    asyncio.run(main())
