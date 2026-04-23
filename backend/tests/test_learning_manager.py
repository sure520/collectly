import asyncio
from app.services.learning_manager import LearningManager

async def test_learning_manager():
    """测试学习管理功能"""
    learning_manager = LearningManager()
    
    # 测试内容ID
    content_id = "476f318580a8fb30085f928c1cc0dfc8"  # 知乎文章
    
    # 测试更新学习状态
    print("测试更新学习状态...")
    try:
        success = await learning_manager.update_status(content_id, "已读")
        print(f"更新学习状态成功: {success}")
        
        # 验证状态更新
        status = await learning_manager.get_status(content_id)
        print(f"当前学习状态: {status}")
    except Exception as e:
        print(f"更新学习状态失败: {e}")
    
    # 测试更新标签
    print("\n测试更新标签...")
    try:
        new_tags = ["大模型", "Agent", "教程", "进阶"]
        success = await learning_manager.update_tags(content_id, new_tags)
        print(f"更新标签成功: {success}")
    except Exception as e:
        print(f"更新标签失败: {e}")
    
    # 测试更新笔记
    print("\n测试更新笔记...")
    try:
        note = "这是一篇关于Agent模型能力的好文章，值得深入学习。"
        success = await learning_manager.update_note(content_id, note)
        print(f"更新笔记成功: {success}")
        
        # 验证笔记更新
        saved_note = await learning_manager.get_note(content_id)
        print(f"保存的笔记: {saved_note}")
    except Exception as e:
        print(f"更新笔记失败: {e}")
    
    # 测试获取学习统计
    print("\n测试获取学习统计...")
    try:
        stats = await learning_manager.get_stats()
        print("学习统计数据:")
        print(f"  总内容数: {stats['total_count']}")
        print(f"  学习进度: {stats['progress']}%")
        print(f"  各状态内容数: {stats['status_counts']}")
        print(f"  各平台内容数: {stats['source_counts']}")
        print(f"  各领域内容数: {stats['domain_counts']}")
    except Exception as e:
        print(f"获取学习统计失败: {e}")
    
    # 测试根据状态获取内容
    print("\n测试根据状态获取内容...")
    try:
        read_content = await learning_manager.get_content_by_status("已读")
        print(f"已读内容: {len(read_content)} 条")
        for item in read_content:
            print(f"  - {item['title']}")
    except Exception as e:
        print(f"根据状态获取内容失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_learning_manager())