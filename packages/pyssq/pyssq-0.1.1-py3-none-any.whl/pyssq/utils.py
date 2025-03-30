from typing import Union


def format_number(num: Union[int, str], digits: int = 2) -> str:
    """格式化数字为指定位数，前面补零"""
    try:
        num = int(num)
        return f"{num:0{digits}d}"
    except (ValueError, TypeError):
        raise ValueError("输入必须是数字")
