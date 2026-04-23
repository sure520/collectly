from openai import AsyncOpenAI
import os


class Summarizer:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key="sk-c7624bc850eb446ebab68fc13aded1a2",
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        self.model = "qwen-turbo"
    
    async def summarize(self, content: str, max_length: int = 500) -> str:
        if not content or len(content) < 100:
            return content
        
        # 截断过长的内容
        truncated_content = content[:3000] if len(content) > 3000 else content
        
        prompt = f"""请对以下文章内容进行摘要总结，要求：
1. 提取核心观点和关键信息
2. 保持客观准确，不添加原文没有的内容
3. 摘要控制在200字以内
4. 使用中文输出

文章内容：
{truncated_content}

请输出摘要："""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的内容摘要助手，擅长提取文章核心要点。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            summary = response.choices[0].message.content.strip()
            return summary
            
        except Exception as e:
            # 如果API调用失败，返回简单的文本截断作为摘要
            return content[:max_length] + "..." if len(content) > max_length else content