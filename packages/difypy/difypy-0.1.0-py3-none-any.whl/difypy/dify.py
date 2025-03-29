import requests
import json
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
from enum import Enum


class ResponseMode(Enum):
    STREAMING = "streaming"
    BLOCKING = "blocking"

@dataclass
class FileUploadResponse:
    id: str
    name: str
    size: int
    extension: str
    mime_type: str
    created_by: str
    created_at: int

@dataclass
class WorkflowResponse:
    workflow_run_id: str
    task_id: str
    data: Dict[str, Any]

class Dify:
    def __init__(self, api_key: str, base_url: str ):
        """
        初始化 Dify 客户端
        
        Args:
            api_key: API密钥
            base_url: API基础URL
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def _handle_response(self, response: requests.Response) -> Dict:
        """
        处理API响应
        
        Args:
            response: requests响应对象
            
        Returns:
            Dict: 响应数据
            
        Raises:
            DifyError: API错误
        """
        if response.status_code >= 400:
            error_data = response.json()
            raise DifyError(
                message=error_data.get("message", "Unknown error"),
                status_code=response.status_code
            )
        return response.json()

    def run_workflow(
        self,
        inputs: Dict[str, Any],
        user: str,
        response_mode: ResponseMode = ResponseMode.STREAMING,
        files: Optional[List[Dict]] = None
    ) -> Union[WorkflowResponse, Any]:
        """
        执行工作流
        
        Args:
            inputs: 输入参数
            user: 用户标识
            response_mode: 响应模式
            files: 文件列表
            
        Returns:
            WorkflowResponse: 工作流响应
        """
        url = f"{self.base_url}/workflows/run"
        
        payload = {
            "inputs": inputs,
            "response_mode": response_mode.value,
            "user": user
        }
        
        if files:
            payload["files"] = files
            
        response = self.session.post(url, json=payload)
        data = self._handle_response(response)
        
        if response_mode == ResponseMode.BLOCKING:
            return WorkflowResponse(**data)
        return data  # 流式响应直接返回数据

    def get_workflow_status(self, workflow_id: str) -> Dict:
        """
        获取工作流执行状态
        
        Args:
            workflow_id: 工作流ID
            
        Returns:
            Dict: 工作流状态信息
        """
        url = f"{self.base_url}/workflows/run/{workflow_id}"
        response = self.session.get(url)
        return self._handle_response(response)

    def stop_workflow(self, task_id: str, user: str) -> Dict:
        """
        停止工作流执行
        
        Args:
            task_id: 任务ID
            user: 用户标识
            
        Returns:
            Dict: 停止结果
        """
        url = f"{self.base_url}/workflows/tasks/{task_id}/stop"
        payload = {"user": user}
        response = self.session.post(url, json=payload)
        return self._handle_response(response)

    def upload_file(
        self,
        file_path: str,
        user: str,
        file_type: str = "document"
    ) -> FileUploadResponse:
        """
        上传文件
        
        Args:
            file_path: 文件路径
            user: 用户标识
            file_type: 文件类型
            
        Returns:
            FileUploadResponse: 文件上传响应
        """
        url = f"{self.base_url}/files/upload"
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {
                'user': user,
                'type': file_type
            }
            response = self.session.post(url, files=files, data=data)
            data = self._handle_response(response)
            return FileUploadResponse(**data)

    def get_workflow_logs(
        self,
        keyword: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        limit: int = 20
    ) -> Dict:
        """
        获取工作流日志
        
        Args:
            keyword: 搜索关键字
            status: 状态过滤
            page: 页码
            limit: 每页数量
            
        Returns:
            Dict: 日志数据
        """
        url = f"{self.base_url}/workflows/logs"
        params = {
            "page": page,
            "limit": limit
        }
        
        if keyword:
            params["keyword"] = keyword
        if status:
            params["status"] = status
            
        response = self.session.get(url, params=params)
        return self._handle_response(response)

    def get_app_info(self) -> Dict:
        """
        获取应用信息
        
        Returns:
            Dict: 应用信息
        """
        url = f"{self.base_url}/info"
        response = self.session.get(url)
        return self._handle_response(response)

    def get_app_parameters(self) -> Dict:
        """
        获取应用参数
        
        Returns:
            Dict: 应用参数
        """
        url = f"{self.base_url}/parameters"
        response = self.session.get(url)
        return self._handle_response(response)
    
    
    def get_workflow_config(self) -> Dict:
        """
        获取工作流配置信息，包括：
        - 输入参数配置
        - 文件上传配置
        - 系统参数限制
        
        Returns:
            Dict: 工作流配置信息
        """
        url = f"{self.base_url}/parameters"
        response = self.session.get(url)
        data = self._handle_response(response)
        
        return {
            "user_input_form": data.get("user_input_form", []),  # 用户输入表单配置
            "file_upload": data.get("file_upload", {}),  # 文件上传配置
            "system_parameters": data.get("system_parameters", {})  # 系统参数
        }

    def get_workflow_input_schema(self) -> List[Dict]:
        """
        获取工作流输入参数的结构定义
        
        Returns:
            List[Dict]: 输入参数结构列表
        """
        config = self.get_workflow_config()
        return config.get("user_input_form", [])

    def get_file_upload_config(self) -> Dict:
        """
        获取文件上传配置信息
        
        Returns:
            Dict: 文件上传配置
        """
        config = self.get_workflow_config()
        return config.get("file_upload", {})

    def get_system_parameters(self) -> Dict:
        """
        获取系统参数限制
        
        Returns:
            Dict: 系统参数配置
        """
        config = self.get_workflow_config()
        return config.get("system_parameters", {})

class DifyError(Exception):
    """Dify API 错误"""
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(f"Dify API Error: {message} (Status: {status_code})")