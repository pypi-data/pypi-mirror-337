# DifyPy

Python SDK for Dify API - 简单易用的 Dify API 客户端

## 安装

```bash
pip install difypy
```
## 快速开始

```python 
from difypy import Dify, ResponseMode

# 初始化客户端,url填写你们公司自己部署的
client = Dify(api_key="your_api_key", base_url="https://api.dify.ai/v1")

# 运行工作流
response = client.run_workflow(
    inputs={"query": "你好，请介绍一下自己"},
    user="user_123",
    response_mode=ResponseMode.BLOCKING
)

print(response.data)

# 上传文件
file_response = client.upload_file(
    file_path="path/to/file.pdf",
    user="user_123"
)

print(f"文件ID: {file_response.id}")

```

## 功能特性
- 工作流执行（支持流式和阻塞模式）
- 文件上传和管理
- 工作流状态查询
- 应用信息获取
- 错误处理

## 许可证
MIT
