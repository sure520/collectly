from datetime import datetime
from typing import Union


def timestamp_to_date(timestamp: Union[str, int]) -> str:
    """
    将时间戳转换为年月日格式的字符串
    
    Args:
        timestamp: 时间戳，可以是字符串或整数（秒级）
        
    Returns:
        str: 格式化的年月日字符串，如 "2026-04-19"
    """
    # 如果输入是字符串，转换为整数
    if isinstance(timestamp, str):
        timestamp = int(timestamp)
    
    # 将秒级时间戳转换为datetime对象
    dt = datetime.fromtimestamp(timestamp)
    
    # 格式化为年月日格式
    return dt.strftime("%Y-%m-%d")


def timestamp_to_datetime(timestamp: Union[str, int]) -> datetime:
    """
    将时间戳转换为datetime对象
    
    Args:
        timestamp: 时间戳，可以是字符串或整数（秒级）
        
    Returns:
        datetime: 对应的datetime对象
    """
    if isinstance(timestamp, str):
        timestamp = int(timestamp)
    
    return datetime.fromtimestamp(timestamp)


def timestamp_to_chinese_date(timestamp: Union[str, int]) -> str:
    """
    将时间戳转换为中文格式的日期字符串
    
    Args:
        timestamp: 时间戳，可以是字符串或整数（秒级）
        
    Returns:
        str: 格式化的中文日期字符串，如 "2026年04月19日"
    """
    if isinstance(timestamp, str):
        timestamp = int(timestamp)
    
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y年%m月%d日")


# 使用示例
if __name__ == "__main__":
    # 测试数据
    test_timestamp_str = "1776576399"
    test_timestamp_int = 1776576399
    
    print("字符串时间戳转换:")
    print(f"原始时间戳: {test_timestamp_str}")
    print(f"标准格式: {timestamp_to_date(test_timestamp_str)}")
    print(f"中文格式: {timestamp_to_chinese_date(test_timestamp_str)}")
    
    print("\n整数时间戳转换:")
    print(f"原始时间戳: {test_timestamp_int}")
    print(f"标准格式: {timestamp_to_date(test_timestamp_int)}")
    print(f"中文格式: {timestamp_to_chinese_date(test_timestamp_int)}")
    
    # 测试datetime对象
    dt_obj = timestamp_to_datetime(test_timestamp_str)
    print(f"\nDatetime对象: {dt_obj}")
    print(f"对象类型: {type(dt_obj)}")