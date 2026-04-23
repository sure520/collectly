import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
from http import HTTPStatus
import dashscope
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role
from app.utils.config import get_settings

settings = get_settings()

def test_response_format():
    """测试 DashScope API 响应格式"""
    
    dashscope.api_key = settings.DASHSCOPE_API_KEY
    
    messages = [
        {"role": Role.USER, "content": "请简要介绍人工智能。"}
    ]
    
    print("调用 DashScope API...")
    response = Generation.call(
        model="qwen-plus",
        messages=messages,
        result_format='message',
        temperature=0.7,
        max_tokens=100
    )
    
    print(f"\n状态码: {response.status_code}")
    print(f"Code: {response.code}")
    print(f"Message: {response.message}")
    print(f"\n完整 response 对象属性:")
    print(f"  output: {response.output}")
    print(f"  output 类型: {type(response.output)}")
    
    if response.output:
        print(f"\noutput 的所有键: {response.output.keys() if hasattr(response.output, 'keys') else 'N/A'}")
        print(f"\noutput 内容:")
        print(json.dumps(dict(response.output), ensure_ascii=False, indent=2, default=str))
    
    print(f"\nusage: {response.usage}")
    print(f"request_id: {getattr(response, 'request_id', 'N/A')}")

if __name__ == "__main__":
    test_response_format()
