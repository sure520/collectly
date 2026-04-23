import asyncio
from app.services.search_engine import SearchEngine
from datetime import date

async def test_search_engine():
    """测试智能检索和推荐功能"""
    search_engine = SearchEngine()
    
    # 测试搜索功能
    print("测试搜索功能...")
    try:
        results = await search_engine.search(
            text="Agent",
            sources=["知乎", "B站"]
        )
        print(f"搜索成功，找到 {len(results)} 条结果")
        for i, result in enumerate(results[:3]):
            print(f"  {i+1}. {result.title} (相关度: {result.relevance_score:.2f})")
    except Exception as e:
        print(f"搜索失败: {e}")
    
    # 测试相似内容推荐
    print("\n测试相似内容推荐...")
    try:
        # 使用之前存储的内容ID
        content_id = "476f318580a8fb30085f928c1cc0dfc8"  # 知乎文章
        similar_results = await search_engine.get_similar_content(content_id)
        print(f"相似内容推荐成功，找到 {len(similar_results)} 条结果")
        for i, result in enumerate(similar_results):
            print(f"  {i+1}. {result.title} ({result.source})")
    except Exception as e:
        print(f"相似内容推荐失败: {e}")
    
    # 测试个性化推荐
    print("\n测试个性化推荐...")
    try:
        recommendations = await search_engine.get_recommendations()
        print(f"个性化推荐成功，找到 {len(recommendations)} 条结果")
        for i, result in enumerate(recommendations):
            print(f"  {i+1}. {result.title} ({result.source})")
    except Exception as e:
        print(f"个性化推荐失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_search_engine())