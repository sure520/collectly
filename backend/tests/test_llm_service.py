"""
LLM 服务测试模块

测试 DashScope SDK 集成的内容处理功能
"""
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.llm_service import LLMService, LLMServiceError, LLMServiceValidationError
from app.utils.logger import get_logger

logger = get_logger("test_llm_service")


def test_generate_summary():
    """测试摘要生成功能"""
    print("\n=== 测试摘要生成 ===")
    
    test_content = """
    大语言模型（Large Language Model, LLM）是人工智能领域的重要突破。
    基于 Transformer 架构，这些模型能够理解和生成自然语言文本。
    RAG（检索增强生成）技术结合了检索和生成的优势，通过从外部知识库检索相关信息，
    增强了模型的回答能力。Agent 技术则让大语言模型能够自主规划、使用工具，
    完成复杂的任务。多模态模型进一步扩展了能力边界，能够同时处理文本、图像、音频等多种模态的数据。
    """
    
    llm = LLMService()
    
    try:
        summary = llm.generate_summary(test_content)
        print(f"✓ 摘要生成成功:")
        print(f"  {summary}")
        return True
    except LLMServiceValidationError as e:
        print(f"✗ 输入校验失败：{e.message}")
        return False
    except LLMServiceError as e:
        print(f"✗ API 调用失败：{e.message} (错误码：{e.error_code})")
        return False
    except Exception as e:
        print(f"✗ 未知错误：{str(e)}")
        return False


def test_generate_tags():
    """测试标签生成功能"""
    print("\n=== 测试标签生成 ===")
    
    test_content = """
    本文介绍如何使用 Python 实现一个完整的 RAG 系统。
    我们将使用 LangChain 框架，结合向量数据库如 FAISS 或 Chroma，
    构建一个能够回答特定领域问题的智能助手。
    内容涵盖：嵌入模型选择、文档分块策略、检索算法优化、Prompt Engineering 技巧等。
    适合有一定 Python 基础的开发者入门学习。
    """
    
    llm = LLMService()
    
    try:
        tags = llm.generate_tags(test_content)
        print(f"✓ 标签生成成功:")
        print(f"  标签列表：{tags}")
        print(f"  标签数量：{len(tags)}")
        return True
    except LLMServiceValidationError as e:
        print(f"✗ 输入校验失败：{e.message}")
        return False
    except LLMServiceError as e:
        print(f"✗ API 调用失败：{e.message} (错误码：{e.error_code})")
        return False
    except Exception as e:
        print(f"✗ 未知错误：{str(e)}")
        return False


def test_extract_knowledge_points():
    """测试知识点提取功能"""
    print("\n=== 测试知识点提取 ===")
    
    test_content = """
    Transformer 模型的核心是自注意力机制（Self-Attention），
    它能够让模型在处理每个词时，同时关注句子中的其他相关词。
    多头注意力（Multi-Head Attention）允许模型在不同的表示子空间中学习注意力模式。
    位置编码（Positional Encoding）为模型提供了词序信息。
    Layer Normalization 和残差连接（Residual Connection）帮助训练更深的网络。
    这些技术共同构成了现代大语言模型的基础架构。
    """
    
    llm = LLMService()
    
    try:
        points = llm.extract_knowledge_points(test_content)
        print(f"✓ 知识点提取成功:")
        for i, point in enumerate(points, 1):
            print(f"  {i}. {point}")
        return True
    except LLMServiceValidationError as e:
        print(f"✗ 输入校验失败：{e.message}")
        return False
    except LLMServiceError as e:
        print(f"✗ API 调用失败：{e.message} (错误码：{e.error_code})")
        return False
    except Exception as e:
        print(f"✗ 未知错误：{str(e)}")
        return False


def test_speech_to_text():
    """测试语音转文字功能"""
    print("\n=== 测试语音转文字 ===")
    
    llm = LLMService()
    
    # 注意：这里需要一个有效的音频 URL
    # 可以使用测试音频 URL 或本地路径
    test_audio_url = "https://example.com/test-audio.wav"  # 示例 URL
    
    try:
        text = llm.speech_to_text(test_audio_url)
        print(f"✓ 语音识别成功:")
        print(f"  {text}")
        return True
    except LLMServiceValidationError as e:
        print(f"✗ 输入校验失败：{e.message}")
        return False
    except LLMServiceError as e:
        print(f"✗ API 调用失败：{e.message} (错误码：{e.error_code})")
        return False
    except Exception as e:
        print(f"✗ 未知错误：{str(e)}")
        return False


def test_error_handling():
    """测试错误处理功能"""
    print("\n=== 测试错误处理 ===")
    
    llm = LLMService()
    
    # 测试空输入
    print("\n测试 1: 空输入校验")
    try:
        llm.generate_summary("")
        print("✗ 应该抛出输入校验异常")
        return False
    except LLMServiceValidationError as e:
        print(f"✓ 正确捕获输入校验异常：{e.message}")
    
    # 测试过长输入
    print("\n测试 2: 超长输入校验")
    try:
        long_content = "测试内容 " * 5000  # 远超 10000 字符限制
        llm.generate_summary(long_content)
        print("✗ 应该抛出输入校验异常")
        return False
    except LLMServiceValidationError as e:
        print(f"✓ 正确捕获输入校验异常：{e.message}")
    
    return True


def test_platform_parser_integration():
    """测试与 PlatformParser 的集成"""
    print("\n=== 测试 PlatformParser 集成 ===")
    
    from app.services.platform_parser import PlatformParser
    
    parser = PlatformParser()
    
    # 测试内容处理（不依赖外部 API）
    test_content = """
    这是一篇关于大模型技术实践的文章。
    文章介绍了 RAG、Agent、多模态等核心技术概念。
    通过实际案例展示了如何构建基于大语言模型的应用系统。
    适合想要入门大模型开发的工程师阅读。
    """
    
    try:
        print("\n测试摘要生成:")
        summary = parser._generate_summary(test_content)
        print(f"✓ 摘要：{summary[:100]}...")
        
        print("\n测试标签生成:")
        tags = parser._generate_tags(test_content)
        print(f"✓ 标签：{tags}")
        
        print("\n测试知识点提取:")
        points = parser._extract_knowledge_points(test_content)
        print(f"✓ 知识点：{points}")
        
        return True
    except Exception as e:
        print(f"✗ 集成测试失败：{str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """运行所有测试"""
    print("=" * 60)
    print("LLM 服务功能测试")
    print("=" * 60)
    
    results = {
        "摘要生成": test_generate_summary(),
        "标签生成": test_generate_tags(),
        "知识点提取": test_extract_knowledge_points(),
        "语音转文字": test_speech_to_text(),
        "错误处理": test_error_handling(),
        "集成测试": test_platform_parser_integration()
    }
    
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")
    
    passed = sum(results.values())
    total = len(results)
    print(f"\n总计：{passed}/{total} 测试通过")
    
    return all(results.values())


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n测试执行异常：{str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
