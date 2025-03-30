import random
from typing import List, Dict, Union
from .utils import format_number


class DoubleColorBall:
    """
    中国福利彩票双色球生成器

    规则:
    - 红球: 从1-33中选6个不重复数字
    - 蓝球: 从1-16中选1个数字
    """

    RED_RANGE = (1, 33)
    RED_COUNT = 6
    BLUE_RANGE = (1, 16)
    BLUE_COUNT = 1

    @classmethod
    def generate(cls) -> Dict[str, List[int]]:
        """生成一注双色球"""
        red = sorted(random.sample(range(*cls.RED_RANGE), cls.RED_COUNT))
        blue = random.randint(*cls.BLUE_RANGE)
        return {"red": red, "blue": blue}

    @classmethod
    def generate_batch(cls, n: int = 5) -> List[Dict[str, Union[List[int], int]]]:
        """生成多注双色球"""
        if n <= 0:
            raise ValueError("注数必须大于0")
        return [cls.generate() for _ in range(n)]

    @classmethod
    def pretty_print(cls, result: Dict[str, Union[List[int], int]]) -> str:
        """美化输出单注结果"""
        red = " ".join(format_number(num) for num in result["red"])
        blue = format_number(result["blue"])
        return f"红球: {red} | 蓝球: {blue}"

    @classmethod
    def validate(cls, red: List[int], blue: int) -> bool:
        """验证号码是否有效"""
        if len(red) != cls.RED_COUNT or len(set(red)) != cls.RED_COUNT:
            return False
        if any(not (cls.RED_RANGE[0] <= num <= cls.RED_RANGE[1]) for num in red):
            return False
        if not (cls.BLUE_RANGE[0] <= blue <= cls.BLUE_RANGE[1]):
            return False
        return True
