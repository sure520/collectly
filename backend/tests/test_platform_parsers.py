#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专门测试各种平台解析的测试文件
覆盖平台: 抖音、小红书、微信公众号、B站、知乎、CSDN
测试范围: URL处理、平台检测、各解析器独立测试、集成测试
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
import re
import time
from datetime import datetime

from app.services.platform_parser import (
    PlatformParser,
    process_url,
    extract_url,
    resolve_short_url,
    clean_pure_url,
)


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


class TestStats:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.start_time = None
        self.errors = []

    def start(self):
        self.start_time = time.time()

    def add_pass(self):
        self.passed += 1

    def add_fail(self, msg: str):
        self.failed += 1
        self.errors.append(msg)

    def add_skip(self):
        self.skipped += 1

    def elapsed(self) -> float:
        if self.start_time is None:
            return 0
        return time.time() - self.start_time

    def summary(self) -> str:
        total = self.passed + self.failed + self.skipped
        lines = [
            "",
            "=" * 60,
            "  测试汇总",
            "=" * 60,
            f"  总计: {total}  通过: {self.passed}  失败: {self.failed}  跳过: {self.skipped}",
            f"  耗时: {self.elapsed():.2f}s",
        ]
        if self.errors:
            lines.append("")
            lines.append("  失败详情:")
            for err in self.errors:
                lines.append(f"    - {err}")
        return "\n".join(lines)


stats = TestStats()


def check(title: str, condition: bool, detail: str = ""):
    if condition:
        print(f"  ✅ {title}")
        stats.add_pass()
    else:
        msg = f"{title} {detail}".strip()
        print(f"  ❌ {msg}")
        stats.add_fail(msg)


def skip(title: str, reason: str = ""):
    msg = f"  ⏭️  {title}" + (f" ({reason})" if reason else "")
    print(msg)
    stats.add_skip()


async def test_1_url_extraction():
    print("=" * 60)
    print("1. URL 提取测试 (extract_url)")
    print("=" * 60)

    cases = [
        ("纯链接", "https://www.douyin.com/video/12345", "https://www.douyin.com/video/12345"),
        ("抖音分享文案", "6.17 复制打开抖音，看看【涛哥AIGC实战的作品】太好用了 https://v.douyin.com/GiwKX3xWbD4/ HVl:/", "https://v.douyin.com/GiwKX3xWbD4/"),
        ("B站分享文案", "【4月最新Claude Code使用安装教程-哔哩哔哩】 https://b23.tv/XZeyxg6", "https://b23.tv/XZeyxg6"),
        ("小红书短链", "http://xhslink.com/o/8YzrpsvySjv 把口令复制下来", "http://xhslink.com/o/8YzrpsvySjv"),
        ("微信公众号链接", "https://mp.weixin.qq.com/s/Bwmr8vmAgsBz4g5S8SWX7g", "https://mp.weixin.qq.com/s/Bwmr8vmAgsBz4g5S8SWX7g"),
        ("知乎链接", "https://zhuanlan.zhihu.com/p/731785401?share_code=xxx", "https://zhuanlan.zhihu.com/p/731785401?share_code=xxx"),
        ("非链接文本", "这是一段普通文本", "这是一段普通文本"),
        ("空字符串", "", ""),
    ]

    for name, raw, expected in cases:
        result = extract_url(raw)
        check(f"{name}: 提取 → {result[:60]}", result == expected, f"期望 {expected[:60]}")


async def test_2_url_cleaning():
    print("\n" + "=" * 60)
    print("2. URL 净化测试 (clean_pure_url)")
    print("=" * 60)

    cases = [
        (
            "抖音长链带modal_id",
            "https://www.douyin.com/user/self?modal_id=7627013109139475762&showSubTab=favorite_folder",
            "https://www.douyin.com/video/7627013109139475762",
        ),
        (
            "B站长链带追踪参数",
            "https://www.bilibili.com/video/BV1aTp1zRENj/?spm_id_from=333.1387.favlist.content.click&vd_source=ba077cb",
            "https://www.bilibili.com/video/BV1aTp1zRENj",
        ),
        (
            "B站长链带分P",
            "https://www.bilibili.com/video/BV1aTp1zRENj?spm_id_from=333.788.videopod.episodes&vd_source=ba077cb&p=2",
            "https://www.bilibili.com/video/BV1aTp1zRENj?p=2",
        ),
        (
            "知乎链接清洗",
            "https://zhuanlan.zhihu.com/p/731785401?share_code=UaCZQIyom9Iu&utm_psn=2031311064101544538",
            "https://zhuanlan.zhihu.com/p/731785401",
        ),
        (
            "小红书长链清洗",
            "https://www.xiaohongshu.com/explore/69e4ff92000000002102c20a?xsec_token=ABNq2ZZ0Q9oow_EwSy-N9d7LTDU5gStg381dNEAIv6LwU=&xsec_source=pc_collect",
            "https://www.xiaohongshu.com/explore/69e4ff92000000002102c20a?xsec_token=ABNq2ZZ0Q9oow_EwSy-N9d7LTDU5gStg381dNEAIv6LwU=&xsec_source=pc_collect",
        ),
    ]

    for name, raw, expected in cases:
        result = clean_pure_url(raw)
        check(f"{name}: 净化 → {result[:80]}", result == expected, f"期望 {expected[:80]}")


async def test_3_process_url_integration():
    print("\n" + "=" * 60)
    print("3. URL 综合处理测试 (process_url)")
    print("=" * 60)

    cases = [
        (
            "微信公众号直通",
            "https://mp.weixin.qq.com/s/Bwmr8vmAgsBz4g5S8SWX7g",
            "https://mp.weixin.qq.com/s/Bwmr8vmAgsBz4g5S8SWX7g",
        ),
        (
            "知乎链接处理",
            "https://zhuanlan.zhihu.com/p/731785401?share_code=UaCZQIyom9Iu&utm_psn=2031311064101544538",
            "https://zhuanlan.zhihu.com/p/731785401",
        ),
        (
            "B站纯净长链",
            "https://www.bilibili.com/video/BV1aTp1zRENj",
            "https://www.bilibili.com/video/BV1aTp1zRENj",
        ),
    ]

    for name, raw, expected in cases:
        result = process_url(raw)
        check(f"{name}: 处理 → {result[:80]}", result == expected, f"期望 {expected[:80]}")


async def test_4_platform_detection():
    print("\n" + "=" * 60)
    print("4. 平台检测测试 (_detect_platform)")
    print("=" * 60)

    parser = PlatformParser()

    cases = [
        ("抖音", "https://www.douyin.com/video/7627013109139475762", "抖音"),
        ("抖音短链", "https://v.douyin.com/GiwKX3xWbD4/", "抖音"),
        ("小红书", "https://www.xiaohongshu.com/explore/69e4ff92000000002102c20a", "小红书"),
        ("微信公众号", "https://mp.weixin.qq.com/s/Bwmr8vmAgsBz4g5S8SWX7g", "微信公众号"),
        ("B站", "https://www.bilibili.com/video/BV1aTp1zRENj", "B站"),
        ("B站短链", "https://b23.tv/XZeyxg6", "B站"),
        ("知乎", "https://zhuanlan.zhihu.com/p/731785401", "知乎"),
        ("CSDN", "https://blog.csdn.net/example/article/details/123456", "CSDN"),
        ("不支持的平台", "https://www.example.com/article/123", ""),
        ("空字符串", "", ""),
    ]

    for name, url, expected in cases:
        result = parser._detect_platform(url)
        check(f"{name}: {url[:50]} → {result or '(空)'}", result == expected, f"期望 {expected or '(空)'} 实际 {result}")


async def test_5_parse_url_validation():
    print("\n" + "=" * 60)
    print("5. 解析 URL 验证测试 (无效/特殊输入)")
    print("=" * 60)

    parser = PlatformParser()

    invalid_cases = [
        ("不支持的域名", "https://www.example.com/article/123"),
        ("非HTTP文本", "这是一段普通文本"),
        ("空字符串", ""),
    ]

    for name, url in invalid_cases:
        try:
            result = await parser.parse(url)
            check(f"{name}: 应当抛出异常但未抛出", False, f"意外返回 {result.title}")
        except ValueError as e:
            check(f"{name}: 正确拒绝 → {str(e)[:60]}", True)
        except Exception as e:
            check(f"{name}: 意外异常类型", False, f"{type(e).__name__}: {str(e)[:60]}")


async def test_6_douyin_parser():
    print("\n" + "=" * 60)
    print("6. 抖音解析器测试 (DouyinParser)")
    print("=" * 60)

    from app.services.parsers.douyin import DouyinParser
    parser = DouyinParser()

    sections = load_test_urls()
    douyin_sections = sections.get("抖音链接", {})

    if not douyin_sections:
        skip("抖音", "未找到测试URL")
        return

    for url_type, urls in douyin_sections.items():
        print(f"\n  📂 {url_type} ({len(urls)} 个)")
        for i, url in enumerate(urls[:2], 1):
            print(f"\n  ── 测试 #{i} ──")
            print(f"     URL: {url[:80]}...")
            try:
                start = time.time()
                result = await parser.parse(url)
                elapsed = time.time() - start
                print(f"  ✅ 解析成功 ({elapsed:.1f}s)")
                print(f"     标题: {result.title}")
                print(f"     作者: {result.author}")
                print(f"     来源: {result.source}")
                content_preview = (result.content[:60].replace("\n", " ") if result.content else "(空)")
                print(f"     内容: {content_preview}...")
                print(f"     标签数: {len(result.tags)}")
                print(f"     知识点数: {len(result.knowledge_points)}")
                check(f"抖音 {url_type} #{i}: {result.title[:30]}",
                      result.source == "抖音" and len(result.title) > 0)
            except Exception as e:
                print(f"  ❌ 解析失败: {type(e).__name__}: {str(e)[:100]}")
                check(f"抖音 {url_type} #{i}", False, str(e)[:80])


async def test_7_xiaohongshu_parser():
    print("\n" + "=" * 60)
    print("7. 小红书解析器测试 (XiaohongshuParser)")
    print("=" * 60)

    from app.services.parsers.xiaohongshu import XiaohongshuParser
    parser = XiaohongshuParser()

    sections = load_test_urls()
    xhs_sections = sections.get("小红书", {})

    if not xhs_sections:
        skip("小红书", "未找到测试URL")
        return

    for url_type, urls in xhs_sections.items():
        print(f"\n  📂 {url_type} ({len(urls)} 个)")
        for i, url in enumerate(urls[:2], 1):
            print(f"\n  ── 测试 #{i} ──")
            print(f"     URL: {url[:80]}...")
            try:
                start = time.time()
                result = await parser.parse(url)
                elapsed = time.time() - start
                print(f"  ✅ 解析成功 ({elapsed:.1f}s)")
                print(f"     标题: {result.title}")
                print(f"     作者: {result.author}")
                print(f"     来源: {result.source}")
                content_preview = (result.content[:60].replace("\n", " ") if result.content else "(空)")
                print(f"     内容: {content_preview}...")
                print(f"     标签数: {len(result.tags)}")
                print(f"     知识点数: {len(result.knowledge_points)}")
                check(f"小红书 {url_type} #{i}: {result.title[:30]}",
                      result.source == "小红书" and len(result.title) > 0)
            except Exception as e:
                print(f"  ❌ 解析失败: {type(e).__name__}: {str(e)[:100]}")
                check(f"小红书 {url_type} #{i}", False, str(e)[:80])


async def test_8_bilibili_parser():
    print("\n" + "=" * 60)
    print("8. B站解析器测试 (BilibiliParser)")
    print("=" * 60)

    from app.services.parsers.bilibili import BilibiliParser
    parser = BilibiliParser()

    sections = load_test_urls()
    bilibili_sections = sections.get("bilibili", {})

    if not bilibili_sections:
        skip("B站", "未找到测试URL")
        return

    for url_type, urls in bilibili_sections.items():
        print(f"\n  📂 {url_type} ({len(urls)} 个)")
        for i, url in enumerate(urls[:2], 1):
            print(f"\n  ── 测试 #{i} ──")
            print(f"     URL: {url[:80]}...")
            try:
                start = time.time()
                result = await parser.parse(url)
                elapsed = time.time() - start
                print(f"  ✅ 解析成功 ({elapsed:.1f}s)")
                print(f"     标题: {result.title}")
                print(f"     作者: {result.author}")
                print(f"     来源: {result.source}")
                print(f"     标签数: {len(result.tags)}")
                print(f"     知识点数: {len(result.knowledge_points)}")
                check(f"B站 {url_type} #{i}: {result.title[:30]}",
                      result.source == "B站" and len(result.title) > 0)
            except Exception as e:
                print(f"  ❌ 解析失败: {type(e).__name__}: {str(e)[:100]}")
                check(f"B站 {url_type} #{i}", False, str(e)[:80])


async def test_9_weixin_parser():
    print("\n" + "=" * 60)
    print("9. 微信公众号解析器测试 (WeixinParser)")
    print("=" * 60)

    from app.services.parsers.weixin import WeixinParser
    parser = WeixinParser()

    sections = load_test_urls()
    weixin_sections = sections.get("微信公章号链接", {})

    if not weixin_sections:
        skip("微信公众号", "未找到测试URL")
        return

    for url_type, urls in weixin_sections.items():
        print(f"\n  📂 {url_type} ({len(urls)} 个)")
        for i, url in enumerate(urls[:2], 1):
            print(f"\n  ── 测试 #{i} ──")
            print(f"     URL: {url[:80]}...")
            try:
                start = time.time()
                result = await parser.parse(url)
                elapsed = time.time() - start
                print(f"  ✅ 解析成功 ({elapsed:.1f}s)")
                print(f"     标题: {result.title}")
                print(f"     作者: {result.author}")
                print(f"     来源: {result.source}")
                content_preview = (result.content[:60].replace("\n", " ") if result.content else "(空)")
                print(f"     内容: {content_preview}...")
                print(f"     标签数: {len(result.tags)}")
                print(f"     知识点数: {len(result.knowledge_points)}")
                check(f"微信公众号 {url_type} #{i}: {result.title[:30]}",
                      result.source == "微信公众号" and len(result.title) > 0)
            except Exception as e:
                print(f"  ❌ 解析失败: {type(e).__name__}: {str(e)[:100]}")
                check(f"微信公众号 {url_type} #{i}", False, str(e)[:80])


async def test_10_zhihu_parser():
    print("\n" + "=" * 60)
    print("10. 知乎解析器测试 (ZhihuParser)")
    print("=" * 60)

    from app.services.parsers.zhihu import ZhihuParser
    parser = ZhihuParser()

    sections = load_test_urls()
    zhihu_sections = sections.get("知乎", {})

    if not zhihu_sections:
        skip("知乎", "未找到测试URL")
        return

    for url_type, urls in zhihu_sections.items():
        print(f"\n  📂 {url_type} ({len(urls)} 个)")
        for i, url in enumerate(urls[:2], 1):
            print(f"\n  ── 测试 #{i} ──")
            print(f"     URL: {url[:80]}...")
            try:
                start = time.time()
                result = await parser.parse(url)
                elapsed = time.time() - start
                print(f"  ✅ 解析成功 ({elapsed:.1f}s)")
                print(f"     标题: {result.title}")
                print(f"     作者: {result.author}")
                print(f"     来源: {result.source}")
                content_preview = (result.content[:60].replace("\n", " ") if result.content else "(空)")
                print(f"     内容: {content_preview}...")
                print(f"     标签数: {len(result.tags)}")
                print(f"     知识点数: {len(result.knowledge_points)}")
                check(f"知乎 {url_type} #{i}: {result.title[:30]}",
                      result.source == "知乎" and len(result.title) > 0)
            except Exception as e:
                print(f"  ❌ 解析失败: {type(e).__name__}: {str(e)[:100]}")
                check(f"知乎 {url_type} #{i}", False, str(e)[:80])


async def test_11_csdn_parser():
    print("\n" + "=" * 60)
    print("11. CSDN解析器测试 (CsdnParser)")
    print("=" * 60)

    from app.services.parsers.csdn import CsdnParser
    parser = CsdnParser()

    sections = load_test_urls()
    csdn_sections = sections.get("CSDN", {})

    if not csdn_sections:
        print("  ⚠️ test_url.txt 中未包含 CSDN 测试链接，使用内置链接测试")
        csdn_sections = {"默认": ["https://blog.csdn.net/qq_34417471/article/details/147104046"]}

    for url_type, urls in csdn_sections.items():
        print(f"\n  📂 {url_type} ({len(urls)} 个)")
        for i, url in enumerate(urls[:2], 1):
            print(f"\n  ── 测试 #{i} ──")
            print(f"     URL: {url[:80]}...")
            try:
                start = time.time()
                result = await parser.parse(url)
                elapsed = time.time() - start
                print(f"  ✅ 解析成功 ({elapsed:.1f}s)")
                print(f"     标题: {result.title}")
                print(f"     作者: {result.author}")
                print(f"     来源: {result.source}")
                content_preview = (result.content[:60].replace("\n", " ") if result.content else "(空)")
                print(f"     内容: {content_preview}...")
                print(f"     标签数: {len(result.tags)}")
                print(f"     知识点数: {len(result.knowledge_points)}")
                check(f"CSDN {url_type} #{i}: {result.title[:30]}",
                      result.source == "CSDN" and len(result.title) > 0)
            except Exception as e:
                print(f"  ❌ 解析失败: {type(e).__name__}: {str(e)[:100]}")
                check(f"CSDN {url_type} #{i}", False, str(e)[:80])


async def test_12_short_url_resolution():
    print("\n" + "=" * 60)
    print("12. 短链还原测试 (resolve_short_url)")
    print("=" * 60)

    short_url_cases = [
        ("B站短链", "https://b23.tv/XZeyxg6", "bilibili.com"),
        ("抖音短链", "https://v.douyin.com/GiwKX3xWbD4/", "douyin.com"),
    ]

    for name, short_url, expected_domain in short_url_cases:
        try:
            start = time.time()
            resolved = resolve_short_url(short_url)
            elapsed = time.time() - start
            domain_ok = expected_domain in resolved
            print(f"  [{name}] ({elapsed:.1f}s)")
            print(f"    短链: {short_url}")
            print(f"    还原: {resolved[:100]}")
            check(f"{name}: 域名验证 → {expected_domain}", domain_ok,
                  f"解析结果不包含 {expected_domain}")
        except Exception as e:
            print(f"  [{name}] 还原失败: {e}")
            check(f"{name}: 短链还原", False, str(e)[:80])


async def test_13_platform_parser_response_structure():
    print("\n" + "=" * 60)
    print("13. 解析结果结构验证 (ContentResponse)")
    print("=" * 60)

    from app.services.parsers.bilibili import BilibiliParser
    parser = BilibiliParser()

    test_url = "https://www.bilibili.com/video/BV1aTp1zRENj"

    try:
        start = time.time()
        result = await parser.parse(test_url)
        elapsed = time.time() - start
        print(f"  解析耗时: {elapsed:.1f}s")

        checks = [
            ("title 非空", bool(result.title)),
            ("source 正确", result.source == "B站"),
            ("url 非空", bool(result.url)),
            ("author 存在", isinstance(result.author, str)),
            ("content 存在", isinstance(result.content, str)),
            ("tags 为列表", isinstance(result.tags, list)),
            ("knowledge_points 为列表", isinstance(result.knowledge_points, list)),
            ("create_time 格式", "-" in result.create_time or bool(result.create_time)),
            ("update 格式", "-" in result.update or bool(result.update)),
            ("short_summary 存在", isinstance(result.short_summary, str)),
            ("long_summary 存在", isinstance(result.long_summary, str)),
        ]

        for name, ok in checks:
            check(f"字段验证: {name}", ok)

        print(f"\n  完整结果预览:")
        print(f"    title: {result.title}")
        print(f"    author: {result.author}")
        print(f"    source: {result.source}")
        print(f"    url: {result.url}")
        print(f"    tags ({len(result.tags)}): {result.tags}")
        print(f"    knowledge_points ({len(result.knowledge_points)}): {result.knowledge_points}")
        print(f"    short_summary ({len(result.short_summary)}字): {result.short_summary[:80]}...")
        print(f"    long_summary ({len(result.long_summary)}字): {result.long_summary[:80]}...")

    except Exception as e:
        print(f"  ❌ 解析失败: {type(e).__name__}: {str(e)[:150]}")
        check("结构验证: 解析成功", False, str(e)[:80])


async def test_14_concurrent_parsing():
    print("\n" + "=" * 60)
    print("14. 并发解析测试")
    print("=" * 60)

    urls = [
        "https://www.bilibili.com/video/BV1aTp1zRENj",
        "https://zhuanlan.zhihu.com/p/731785401",
        "https://mp.weixin.qq.com/s/Bwmr8vmAgsBz4g5S8SWX7g",
    ]

    parser = PlatformParser()

    start = time.time()
    tasks = [parser.parse(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    elapsed = time.time() - start

    print(f"  并发解析 {len(urls)} 个链接，总耗时: {elapsed:.1f}s")

    success_count = 0
    for i, (url, result) in enumerate(zip(urls, results)):
        if isinstance(result, Exception):
            print(f"  ❌ #{i+1} {url[:60]}: {type(result).__name__}: {str(result)[:60]}")
            check(f"并发 #{i+1}", False, str(result)[:60])
        else:
            print(f"  ✅ #{i+1} [{result.source}] {result.title[:40]}")
            success_count += 1
            check(f"并发 #{i+1}: {result.title[:30]}", True)

    if success_count >= 2:
        check(f"并发成功率: {success_count}/{len(urls)}", True)


async def main():
    print("=" * 60)
    print("  Collectly 平台解析器专项测试")
    print(f"  开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    stats.start()

    await test_1_url_extraction()
    await test_2_url_cleaning()
    await test_3_process_url_integration()
    await test_4_platform_detection()
    await test_5_parse_url_validation()
    await test_12_short_url_resolution()

    print("\n" + "─" * 60)
    print("  📡 以下测试需要 TikHub API 连接")
    print("─" * 60)

    await test_6_douyin_parser()
    await test_7_xiaohongshu_parser()
    await test_8_bilibili_parser()
    await test_9_weixin_parser()
    await test_10_zhihu_parser()
    await test_11_csdn_parser()
    await test_13_platform_parser_response_structure()
    await test_14_concurrent_parsing()

    print(stats.summary())


if __name__ == "__main__":
    asyncio.run(main())
