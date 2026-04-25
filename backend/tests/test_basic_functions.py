#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Collectly 基础功能测试 - 不依赖外部API
测试向量服务、内容管理、搜索功能
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import asyncio
import json
import time
from datetime import datetime

# 设置UTF-8编码
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

class SimpleTester:
    def __init__(self):
        self.results = {
            "test_time": datetime.now().isoformat(),
            "tests": [],
            "summary": {}
        }
    
    async def test_vector_service(self):
        """测试向量服务"""
        print("\n[测试1/3] 向量数据库服务...")
        try:
            from app.services.vector_service import VectorService
            
            vs = VectorService(persist_directory="./test_chroma_db")
            print("  ✓ 向量服务初始化成功")
            
            # 测试添加向量
            test_content = {
                "title": "测试文章标题",
                "content": "这是一篇关于AI Agent和RAG技术的测试文章，内容涉及向量数据库、语义搜索等技术点。",
                "summary": "AI技术测试文章"
            }
            
            embedding_text = f"{test_content['title']}\n{test_content['summary']}\n{test_content['content']}"
            success = vs.add_embedding(
                content_id="test_001",
                text=embedding_text,
                metadata={"source": "测试", "title": test_content["title"]}
            )
            print(f"  ✓ 向量添加: {'成功' if success else '失败'}")
            
            # 测试搜索
            search_results = vs.search("RAG 向量数据库", n_results=5)
            print(f"  ✓ 语义搜索: 返回 {len(search_results)} 条结果")
            
            # 测试统计
            count = vs.get_collection_size()
            print(f"  ✓ 向量集合大小: {count}")
            
            self.results["tests"].append({
                "name": "向量服务",
                "success": True,
                "vector_count": count
            })
            return True
            
        except Exception as e:
            print(f"  ✗ 向量服务测试失败: {e}")
            import traceback
            traceback.print_exc()
            self.results["tests"].append({
                "name": "向量服务",
                "success": False,
                "error": str(e)
            })
            return False
    
    async def test_content_manager(self):
        """测试内容管理"""
        print("\n[测试2/3] 内容管理服务...")
        try:
            from app.services.content_manager import ContentManager
            from app.models.schemas import ContentResponse
            
            cm = ContentManager()
            print("  ✓ 内容管理器初始化成功")
            
            # 测试保存内容
            test_content = ContentResponse(
                title="AI Agent 开发入门指南",
                content="本文详细介绍了AI Agent的开发技术，包括记忆系统、工具调用、多Agent协作等关键模块。同时涉及RAG技术实现和向量数据库应用。",
                author="测试作者",
                update="2026-04-25",
                create_time="2026-04-25",
                url="https://example.com/test-article",
                source="测试平台",
                tags=["AI", "Agent", "RAG", "向量数据库", "入门"],
                knowledge_points=["AI Agent架构", "RAG技术原理", "向量数据库应用"],
                summary="AI Agent开发入门指南"
            )
            
            content_id = await cm.save(test_content)
            print(f"  ✓ 内容保存成功: ID={content_id}")
            
            # 测试获取内容
            retrieved = await cm.get(content_id)
            print(f"  ✓ 内容读取成功: {retrieved.title}")
            
            # 测试获取所有内容
            all_content = await cm.get_all()
            print(f"  ✓ 内容列表: 共 {len(all_content)} 条")
            
            self.results["tests"].append({
                "name": "内容管理",
                "success": True,
                "content_count": len(all_content)
            })
            return True
            
        except Exception as e:
            print(f"  ✗ 内容管理测试失败: {e}")
            import traceback
            traceback.print_exc()
            self.results["tests"].append({
                "name": "内容管理",
                "success": False,
                "error": str(e)
            })
            return False
    
    async def test_search_engine(self):
        """测试搜索引擎"""
        print("\n[测试3/3] 搜索与检索功能...")
        try:
            from app.services.search_engine import SearchEngine
            
            se = SearchEngine()
            print("  ✓ 搜索引擎初始化成功")
            
            # 测试关键词搜索
            keyword_results = await se.search(
                "AI Agent",
                use_semantic=False
            )
            print(f"  ✓ 关键词搜索: 返回 {len(keyword_results)} 条结果")
            
            # 测试语义搜索
            semantic_results = await se.search(
                "RAG 向量数据库",
                use_semantic=True
            )
            print(f"  ✓ 语义搜索: 返回 {len(semantic_results)} 条结果")
            
            # 测试多维度筛选
            filtered_results = await se.search(
                "",
                domains=["AI"],
                learning_status="未读"
            )
            print(f"  ✓ 筛选搜索: 返回 {len(filtered_results)} 条结果")
            
            # 展示搜索结果质量
            if semantic_results:
                print(f"    最高相关度: {semantic_results[0].relevance_score}")
            
            self.results["tests"].append({
                "name": "搜索引擎",
                "success": True,
                "keyword_count": len(keyword_results),
                "semantic_count": len(semantic_results)
            })
            return True
            
        except Exception as e:
            print(f"  ✗ 搜索功能测试失败: {e}")
            import traceback
            traceback.print_exc()
            self.results["tests"].append({
                "name": "搜索引擎",
                "success": False,
                "error": str(e)
            })
            return False
    
    async def run_all_tests(self):
        """运行所有测试"""
        print("="*70)
        print("Collectly 后端基础功能测试")
        print("="*70)
        
        tests_passed = 0
        tests_total = 0
        
        # 运行各个测试
        if await self.test_vector_service():
            tests_passed += 1
        tests_total += 1
        
        if await self.test_content_manager():
            tests_passed += 1
        tests_total += 1
        
        if await self.test_search_engine():
            tests_passed += 1
        tests_total += 1
        
        # 生成总结
        print("\n" + "="*70)
        print("测试总结")
        print("="*70)
        print(f"\n总测试数: {tests_total}")
        print(f"通过: {tests_passed}")
        print(f"失败: {tests_total - tests_passed}")
        print(f"通过率: {tests_passed/tests_total*100:.1f}%\n")
        
        for test in self.results["tests"]:
            status = "✓ PASS" if test["success"] else "✗ FAIL"
            print(f"{status}: {test['name']}")
        
        self.results["summary"] = {
            "total": tests_total,
            "passed": tests_passed,
            "failed": tests_total - tests_passed,
            "pass_rate": round(tests_passed/tests_total*100, 1)
        }
        
        # 保存结果
        self.save_report()
        
        return tests_passed == tests_total
    
    def save_report(self):
        """保存测试报告"""
        report_file = os.path.join(
            os.path.dirname(__file__),
            "basic_test_report.json"
        )
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            print(f"\n测试报告已保存: {report_file}")
        except Exception as e:
            print(f"\n保存测试报告失败: {e}")

async def main():
    # 切换到backend目录
    backend_dir = os.path.dirname(__file__)
    os.chdir(backend_dir)
    
    tester = SimpleTester()
    success = await tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
