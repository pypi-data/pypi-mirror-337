# MyStats - 统计计算工具包

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

一个用于统计假设检验的Python工具包，支持秩和检验、t检验等常用统计方法。

## 安装

```bash
pip install -e .
```

## 功能列表

### 核心模块
1. **秩和检验 (RankSumTest)**
   - 自动处理小样本（查表法）和大样本（正态近似）
   - 支持自定义显著性水平
2. **t检验 (t_tests)**
   - 独立样本t检验实现
   - 支持双尾检验

### 数据预处理
- `merge_groups()`: 合并实验组/对照组数据
- `assign_ranks()`: 自动分配平均秩

## 快速开始

```python example.py
from mystats import RankSumTest, t_tests

# 秩和检验示例
test = RankSumTest()
result = test.execute([10,12,15], [8,9,11])
print(result)

# t检验示例
t_result = t_tests([20,22,24], [18,19,21])
print(t_result)
```


## 依赖项
- Python 3.8+
- 标准库依赖：
  - `json`
  - `pathlib`
  - `os`

## 贡献指南
1. 提交Issue描述问题
2. Fork仓库并创建特性分支
3. 提交Pull Request

## 作者
zzh <zhaochenxian@outlookk.com>

## 许可证
[MIT License](LICENSE)