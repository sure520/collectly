"""
LLM 服务使用示例

展示如何使用 DashScope SDK 集成的内容处理功能
"""
from app.services.llm_service import LLMService, LLMServiceError
from app.services.platform_parser import PlatformParser


def example_basic_usage():
    """基础使用示例"""
    print("=== 基础使用示例 ===\n")
    
    # 创建 LLM 服务实例
    llm = LLMService()
    
    # 示例内容
    content = """
    大语言模型（LLM）是人工智能领域的重要突破。
    RAG 技术结合了检索和生成的优势，Agent 技术让模型能够自主规划。
    多模态模型能够同时处理文本、图像、音频等多种模态的数据。
    """
    
    # 1. 生成摘要
    summary = llm.generate_summary(content)
    print(f"摘要：{summary}\n")
    
    # 2. 生成标签
    tags = llm.generate_tags(content)
    print(f"标签：{tags}\n")
    
    # 3. 提取知识点
    points = llm.extract_knowledge_points(content)
    print(f"知识点：{points}\n")


def example_speech_to_text():
    """语音转文字示例"""
    print("=== 语音转文字示例 ===\n")
    
    llm = LLMService()
    
    # 示例音频 URL（需要替换为真实的音频 URL）
    audio_url = "https://example.com/audio.wav"
    
    try:
        text = llm.speech_to_text(audio_url, language="zh")
        print(f"识别结果：{text}")
    except LLMServiceError as e:
        print(f"语音识别失败：{e.message}")


def example_error_handling():
    """错误处理示例"""
    print("=== 错误处理示例 ===\n")
    
    llm = LLMService()
    
    # 测试空输入
    try:
        llm.generate_summary("")
    except LLMServiceError as e:
        print(f"捕获错误：{e.message}")
        print(f"错误码：{e.error_code}\n")
    
    # 带重试的调用（自动处理）
    content = "测试内容" * 100
    try:
        result = llm.generate_summary(content, timeout=30)
        print(f"成功：{result[:50]}...")
    except LLMServiceError as e:
        print(f"API 调用失败：{e.message}")


def example_platform_parser():
    """PlatformParser 集成示例"""
    print("=== PlatformParser 集成示例 ===\n")
    
    # 注意：这个示例需要有效的抖音分享链接
    # 实际使用时请替换为真实的链接
    test_url = "https://v.douyin.com/example"  # 示例链接
    
    parser = PlatformParser()
    
    try:
        # 解析链接并自动使用 LLM 处理内容
        result = parser.parse(test_url)
        
        print(f"标题：{result.title}")
        print(f"摘要：{result.summary}")
        print(f"标签：{result.tags}")
        print(f"知识点：{result.knowledge_points}")
    except Exception as e:
        print(f"解析失败（预期）：{e}")
        print("注：需要有效的分享链接才能成功解析")


def example_custom_timeout():
    """自定义超时设置示例"""
    print("=== 自定义超时设置示例 ===\n")
    
    llm = LLMService()
    content = "短内容"
    
    # 设置较短的超时时间
    try:
        summary = llm.generate_summary(content, timeout=10)
        print(f"快速响应：{summary}")
    except LLMServiceError as e:
        if e.error_code == "TIMEOUT":
            print("请求超时，建议使用默认超时时间（60 秒）")
        else:
            print(f"其他错误：{e.message}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("LLM 服务使用示例")
    print("=" * 60)
    print()
    
    # 运行各个示例
    example_basic_usage()
    example_speech_to_text()
    example_error_handling()
    example_platform_parser()
    example_custom_timeout()
    
    print("\n" + "=" * 60)
    print("示例执行完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
