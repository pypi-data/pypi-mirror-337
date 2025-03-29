"""
数据清洗模块

此模块提供使用Unstructured分区库从各种源清洗数据的功能。
它支持处理文件、URL和文本内容，并提供用于管理清洗任务的简单API。

组件:
- unstructured_core: 数据清洗核心实现
- task_manager: 任务队列管理
"""

from .task_manager import TaskManager, TaskStatus
from .unstructured_core import DataCleanseCore

__version__ = "0.1.0"
__all__ = [
    "TaskManager",
    "TaskStatus",
    "DataCleanseCore",
] 