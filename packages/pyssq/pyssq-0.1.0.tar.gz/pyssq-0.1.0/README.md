# PySSQ - 中国双色球随机生成器

[![PyPI version](https://img.shields.io/pypi/v/pyssq.svg)](https://pypi.org/project/pyssq/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个简单的中国福利彩票双色球随机号码生成器。

## 安装(测试阶段使用 uv)

```bash
# 正式发布后
pip install pyssq

# 测试发布时
uv add --default-index  https://test.pypi.org/simple/ pyssq
```

## 使用示例

```python
from pyssq import DoubleColorBall

# 生成一注
ticket = DoubleColorBall.generate()
print(DoubleColorBall.pretty_print(ticket))

# 生成5注
for i, ticket in enumerate(DoubleColorBall.generate_batch(5), 1):
    print(f"第{i}注: {DoubleColorBall.pretty_print(ticket)}")

# 验证号码
print(DoubleColorBall.validate([1,2,3,4,5,6], 7))  # True
print(DoubleColorBall.validate([1,1,2,3,4,5], 7))  # False
```

## 功能

- 随机生成符合规则的双色球号码
- 批量生成多注号码
- 号码验证功能
- 美化输出格式

## 贡献

欢迎提交 issue 或 pull request。

## 许可证

MIT
