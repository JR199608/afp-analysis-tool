# 甲胎蛋白数据分析工具

这是一个用于分析甲胎蛋白（AFP）测定数据的 Python 工具。

## 环境要求

- Python 3.6 或更高版本
- pip（Python 包管理器）

## 安装步骤

1. 克隆或下载此项目到本地
2. 打开命令行，进入项目目录
3. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

1. 准备数据：
   - 将您的 Excel 数据文件放在项目目录中
   - 确保数据格式与示例文件相同

2. 运行分析：
   ```bash
   python diagnosis_analyzer.py
   ```

3. 查看示例：
   ```bash
   python example_usage.py
   ```

## 文件说明

- `diagnosis_analyzer.py`: 主程序文件，包含数据分析的核心功能
- `requirements.txt`: 项目依赖文件
- `example_usage.py`: 使用示例文件

## 注意事项

- 请确保输入数据格式正确
- 分析结果将保存在新的 Excel 文件中 