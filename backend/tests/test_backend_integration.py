#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Collectly 后端完整测试脚本
执行向量搜索、链接解析、API功能测试
"""

import asyncio
import aiohttp
import time
import json
import os
from typing import List, Dict, Any
from datetime import datetime

class CollectlyTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_base = f"{base_url}/api"
        self.test_results = {
            "test_start_time": datetime.now().isoformat(),
            "platform_tests": {},
            "search_tests": {},
            "vector_stats": {},
            "errors": [],
            "summary": {}
        }
        
    async def test_health(self) -> Dict[str, Any]:
        """测试健康检查端点"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/health") as response:
                    if response.status == 200:
                        result = await response.json()
                        return {"success": True, "status": "healthy", "response": result}
                    else:
                        return {"success": False, "status": "unhealthy", "error": f"HTTP {response.status}"}
        except Exception as e:
            return {"success": False, "status": "error", "error": str(e)}
    
    async def test_parse_single_link(self, url: str, platform_name: str) -> Dict[str, Any]:
        """测试单个链接解析"""
        start_time = time.time()
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
                async with session.post(
                    f"{self.api_base}/parse-link",
                    json={"url": url},
                    headers={"Content-Type": "application/json"}
                ) as response:
                    elapsed_time = time.time() - start_time
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "success": True,
                            "platform": platform_name,
                            "url": url,
                            "status_code": response.status,
                            "response_time": round(elapsed_time, 3),
                            "title": result.get("title", ""),
                            "author": result.get("author", ""),
                            "has_summary": bool(result.get("summary")),
                            "has_tags": bool(result.get("tags")),
                            "has_knowledge_points": bool(result.get("knowledge_points")),
                            "tags_count": len(result.get("tags", [])),
                            "knowledge_points_count": len(result.get("knowledge_points", []))
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "platform": platform_name,
                            "url": url,
                            "status_code": response.status,
                            "response_time": round(elapsed_time, 3),
                            "error": error_text
                        }
        except Exception as e:
            elapsed_time = time.time() - start_time
            return {
                "success": False,
                "platform": platform_name,
                "url": url,
                "response_time": round(elapsed_time, 3),
                "error": str(e)
            }
    
    async def test_search(self, query: str, use_semantic: bool = True, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """测试搜索功能"""
        start_time = time.time()
        try:
            search_payload = {
                "text": query,
                "use_semantic": use_semantic
            }
            if filters:
                search_payload.update(filters)
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
                async with session.post(
                    f"{self.api_base}/search",
                    json=search_payload,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    elapsed_time = time.time() - start_time
                    if response.status == 200:
                        results = await response.json()
                        return {
                            "success": True,
                            "query": query,
                            "use_semantic": use_semantic,
                            "status_code": response.status,
                            "response_time": round(elapsed_time, 3),
                            "results_count": len(results),
                            "avg_relevance_score": round(sum(r.get("relevance_score", 0) for r in results) / len(results) if results else 0, 4)
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "query": query,
                            "use_semantic": use_semantic,
                            "status_code": response.status,
                            "response_time": round(elapsed_time, 3),
                            "error": error_text
                        }
        except Exception as e:
            elapsed_time = time.time() - start_time
            return {
                "success": False,
                "query": query,
                "use_semantic": use_semantic,
                "response_time": round(elapsed_time, 3),
                "error": str(e)
            }
    
    async def test_vector_stats(self) -> Dict[str, Any]:
        """测试向量统计端点"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_base}/vector-stats") as response:
                    if response.status == 200:
                        result = await response.json()
                        return {"success": True, "data": result}
                    else:
                        return {"success": False, "status_code": response.status}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def test_learning_stats(self) -> Dict[str, Any]:
        """测试学习统计端点"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_base}/learning-stats") as response:
                    if response.status == 200:
                        result = await response.json()
                        return {"success": True, "data": result}
                    else:
                        return {"success": False, "status_code": response.status}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def extract_clean_url(self, url_candidate: str) -> str:
        """从混合文本中提取干净的URL"""
        import re
        # 匹配URL模式
        url_pattern = r'https?://[^\s]+'
        matches = re.findall(url_pattern, url_candidate)
        if matches:
            return matches[0]
        return url_candidate
    
    async def run_full_test_suite(self):
        """运行完整测试套件"""
        print("="*70)
        print("Collectly 后端完整测试套件")
        print("="*70)
        
        # 1. 健康检查
        print("\n[1/5] 健康检查测试...")
        health_result = await self.test_health()
        print(f"  健康状态: {'✓' if health_result['success'] else '✗'}")
        if not health_result['success']:
            print(f"  错误: {health_result.get('error', '未知错误')}")
            self.test_results['errors'].append(f"健康检查失败: {health_result.get('error')}")
            return
        
        # 2. 向量统计
        print("\n[2/5] 向量数据库状态检查...")
        vector_stats = await self.test_vector_stats()
        self.test_results['vector_stats'] = vector_stats
        if vector_stats['success']:
            print(f"  ✓ 向量数据库正常")
            print(f"    向量集合大小: {vector_stats.get('data', {}).get('collection_size', 0)}")
        else:
            print(f"  ✗ 向量数据库异常: {vector_stats.get('error')}")
        
        # 3. 学习统计
        print("\n[3/5] 学习统计检查...")
        learning_stats = await self.test_learning_stats()
        if learning_stats['success']:
            print(f"  ✓ 学习统计API正常")
            stats_data = learning_stats.get('data', {})
            if stats_data:
                print(f"    内容总数: {stats_data.get('total_count', 0)}")
                print(f"    未读内容: {stats_data.get('status_counts', {}).get('未读', 0)}")
                print(f"    已读内容: {stats_data.get('status_counts', {}).get('已读', 0)}")
        else:
            print(f"  ✗ 学习统计API异常")
        
        # 4. 加载测试URL并解析
        print("\n[4/5] 平台链接解析测试...")
        test_urls_file = r"d:\python\code\myself\collectly\tests\test_url.txt"
        platform_urls = self.parse_test_urls(test_urls_file)
        
        platform_results = {}
        for platform, urls in platform_urls.items():
            if urls:
                print(f"\n  测试平台: {platform} ({len(urls)}个链接)")
                platform_results[platform] = []
                for idx, url in enumerate(urls, 1):
                    print(f"    链接 {idx}/{len(urls)}: {url[:60]}...")
                    result = await self.test_parse_single_link(url, platform)
                    platform_results[platform].append(result)
                    status = "✓" if result['success'] else "✗"
                    response_time = result.get('response_time', 0)
                    print(f"      结果: {status} 响应时间: {response_time}s")
        
        self.test_results['platform_tests'] = platform_results
        
        # 5. 搜索功能测试
        print("\n[5/5] 搜索功能测试...")
        search_queries = [
            ("AI Agent", True),
            ("RAG 优化", True),
            ("大模型 训练", False),
            ("向量数据库", True),
            ("Python 代码", False)
        ]
        
        search_results = []
        for query, use_semantic in search_queries:
            mode = "语义搜索" if use_semantic else "关键词搜索"
            print(f"\n  测试 {mode}: {query}")
            result = await self.test_search(query, use_semantic)
            search_results.append(result)
            status = "✓" if result['success'] else "✗"
            if result['success']:
                print(f"    结果: {status} 返回 {result['results_count']} 条记录")
                print(f"    平均相关度: {result['avg_relevance_score']}")
            else:
                print(f"    结果: {status} 错误: {result.get('error', '未知')}")
        
        self.test_results['search_tests'] = search_results
        
        # 生成报告
        self.generate_report()
    
    def parse_test_urls(self, file_path: str) -> Dict[str, List[str]]:
        """解析测试URL文件"""
        platform_urls = {
            "微信公众号": [],
            "抖音": [],
            "B站": [],
            "知乎": [],
            "小红书": [],
            "CSDN": []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            current_platform = None
            for line in lines:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                
                if "微信" in line and ("链接" in line or "测试" in line):
                    current_platform = "微信公众号"
                    continue
                elif "抖音" in line and ("链接" in line or "测试" in line):
                    current_platform = "抖音"
                    continue
                elif "bilibili" in line.lower() or "B站" in line:
                    current_platform = "B站"
                    continue
                elif "知乎" in line and ("链接" in line or "测试" in line):
                    current_platform = "知乎"
                    continue
                elif "小红书" in line:
                    current_platform = "小红书"
                    continue
                elif "CSDN" in line:
                    current_platform = "CSDN"
                    continue
                
                if current_platform and (line.startswith("http") or "http" in line):
                    clean_url = self.extract_clean_url(line)
                    platform_urls[current_platform].append(clean_url)
        except Exception as e:
            print(f"  警告: 解析测试URL文件失败: {e}")
        
        return platform_urls
    
    def generate_report(self):
        """生成测试报告"""
        print("\n" + "="*70)
        print("测试报告")
        print("="*70)
        
        # 平台解析统计
        print("\n1. 平台链接解析测试结果:")
        print("-"*70)
        
        platform_tests = self.test_results.get('platform_tests', {})
        total_platform_tests = 0
        successful_platform_tests = 0
        
        for platform, results in platform_tests.items():
            if not results:
                continue
            total = len(results)
            successful = sum(1 for r in results if r['success'])
            avg_time = sum(r.get('response_time', 0) for r in results) / total
            total_platform_tests += total
            successful_platform_tests += successful
            
            print(f"\n{platform}:")
            print(f"  总数: {total}")
            print(f"  成功: {successful}")
            print(f"  失败: {total - successful}")
            print(f"  平均响应时间: {round(avg_time, 3)}s")
        
        # 搜索测试统计
        print("\n2. 搜索功能测试结果:")
        print("-"*70)
        
        search_tests = self.test_results.get('search_tests', [])
        for idx, result in enumerate(search_tests, 1):
            mode = "语义搜索" if result.get('use_semantic') else "关键词搜索"
            status = "成功" if result['success'] else "失败"
            print(f"\n测试 {idx}: {mode} - '{result.get('query')}'")
            print(f"  状态: {status}")
            print(f"  响应时间: {result.get('response_time', 0)}s")
            if result['success']:
                print(f"  返回结果数: {result.get('results_count', 0)}")
                print(f"  平均相关度: {result.get('avg_relevance_score', 0)}")
        
        # 总结
        print("\n3. 总体总结:")
        print("-"*70)
        
        platform_success_rate = (successful_platform_tests / total_platform_tests * 100) if total_platform_tests > 0 else 0
        search_success_rate = (sum(1 for s in search_tests if s['success']) / len(search_tests) * 100) if search_tests else 0
        
        print(f"平台链接解析成功率: {round(platform_success_rate, 1)}%")
        print(f"搜索功能成功率: {round(search_success_rate, 1)}%")
        
        errors = self.test_results.get('errors', [])
        if errors:
            print(f"\n发现 {len(errors)} 个错误:")
            for idx, error in enumerate(errors[:5], 1):
                print(f"  {idx}. {error}")
            if len(errors) > 5:
                print(f"  ... 还有 {len(errors) - 5} 个错误")
        
        # 保存报告
        self.save_report()
    
    def save_report(self):
        """保存测试报告"""
        report_file = r"d:\python\code\myself\collectly\tests\test_report.json"
        try:
            os.makedirs(os.path.dirname(report_file), exist_ok=True)
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(self.test_results, f, ensure_ascii=False, indent=2)
            print(f"\n测试报告已保存到: {report_file}")
        except Exception as e:
            print(f"保存测试报告失败: {e}")

async def main():
    tester = CollectlyTester()
    await tester.run_full_test_suite()

if __name__ == "__main__":
    asyncio.run(main())
