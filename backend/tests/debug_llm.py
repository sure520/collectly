import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import os
import json
from datetime import datetime
from http import HTTPStatus
from app.utils.config import get_settings

settings = get_settings()

def debug_llm_service():
    """调试 LLM 服务配置和请求"""
    
    import dashscope
    from dashscope import Generation
    from dashscope.api_entities.dashscope_response import Role
    
    log_file = Path(__file__).parent / "llm_debug_log.txt"
    
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("=== LLM 服务调试日志 ===\n")
        f.write(f"生成时间: {datetime.now()}\n")
        f.write("=" * 80 + "\n\n")
        
        # 1. 检查配置
        f.write("【1. 配置检查】\n")
        f.write(f"DASHSCOPE_API_KEY: {settings.DASHSCOPE_API_KEY[:10]}... (长度: {len(settings.DASHSCOPE_API_KEY)})\n")
        f.write(f"LLM_MODEL_NAME: qwen3.5-35b-a3b\n")
        f.write(f"环境变量 DASHSCOPE_API_KEY: {os.getenv('DASHSCOPE_API_KEY', '未设置')[:10]}...\n")
        
        api_key_val = getattr(dashscope, 'api_key', None)
        if api_key_val:
            f.write(f"dashscope.api_key: {api_key_val[:10]}...\n")
        else:
            f.write("dashscope.api_key: 未设置\n")
        f.write("\n")
        
        # 2. 测试 API Key 是否有效
        f.write("【2. API Key 有效性检查】\n")
        if not settings.DASHSCOPE_API_KEY:
            f.write("✗ DASHSCOPE_API_KEY 未配置\n")
            f.write("解决方案：在 .env 文件中添加 DASHSCOPE_API_KEY=your_api_key\n")
            print(f"调试日志已保存到: {log_file}")
            return
        else:
            f.write("✓ DASHSCOPE_API_KEY 已配置\n")
        f.write("\n")
        
        # 3. 测试不同模型名称
        f.write("【3. 模型名称测试】\n")
        
        test_models = [
            "qwen3.5-35b-a3b",
            "qwen-turbo",
            "qwen-plus",
            "qwen-max",
            "qwen-long",
        ]
        
        test_content = "请简要介绍人工智能。"
        messages = [
            {"role": Role.USER, "content": test_content}
        ]
        
        for model_name in test_models:
            f.write(f"\n测试模型: {model_name}\n")
            f.write(f"请求内容: {test_content}\n")
            
            try:
                response = Generation.call(
                    model=model_name,
                    messages=messages,
                    result_format='message',
                    temperature=0.7,
                    max_tokens=100
                )
                
                f.write(f"响应状态码: {response.status_code}\n")
                f.write(f"响应 code: {response.code}\n")
                f.write(f"响应 message: {response.message}\n")
                
                if response.status_code == HTTPStatus.OK:
                    f.write(f"✓ 模型 {model_name} 调用成功\n")
                    output_text = response.output.get('text', '') if response.output else ''
                    f.write(f"响应内容: {output_text[:200]}\n")
                    f.write(f"\n*** 推荐使用此模型 ***\n")
                else:
                    f.write(f"✗ 模型 {model_name} 调用失败\n")
                    response_dict = {
                        'status_code': response.status_code,
                        'code': response.code,
                        'message': response.message,
                        'request_id': getattr(response, 'request_id', 'N/A')
                    }
                    f.write(f"完整响应: {json.dumps(response_dict, ensure_ascii=False, indent=2)}\n")
                    
            except Exception as e:
                f.write(f"✗ 模型 {model_name} 请求异常: {str(e)}\n")
                import traceback
                f.write(f"异常堆栈:\n{traceback.format_exc()}\n")
        
        # 4. 检查 DashScope SDK 版本
        f.write("\n【4. DashScope SDK 信息】\n")
        try:
            import dashscope as ds
            f.write(f"DashScope 版本: {ds.__version__ if hasattr(ds, '__version__') else '未知'}\n")
        except Exception as e:
            f.write(f"获取 SDK 版本失败: {str(e)}\n")
        
        # 5. 检查网络连通性
        f.write("\n【5. 网络连通性检查】\n")
        try:
            import requests
            response = requests.get("https://dashscope.aliyuncs.com", timeout=10)
            f.write(f"DashScope API 端点可达: {response.status_code}\n")
        except Exception as e:
            f.write(f"DashScope API 端点不可达: {str(e)}\n")
    
    print(f"调试日志已保存到: {log_file}")
    print(f"请查看日志文件了解详细的 LLM 服务配置问题")

if __name__ == "__main__":
    debug_llm_service()
