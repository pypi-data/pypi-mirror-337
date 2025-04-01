from .base import BaseServiceAdapter
from .python import PythonServiceAdapter
from .shell import ShellServiceAdapter

# 注册适配器
BaseServiceAdapter.register_adapter(PythonServiceAdapter)
BaseServiceAdapter.register_adapter(ShellServiceAdapter)  # 兜底适配

__all__ = ["BaseServiceAdapter", "ShellServiceAdapter", "PythonServiceAdapter"]
