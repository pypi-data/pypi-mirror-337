from .base import BaseServiceAdapter


class ShellServiceAdapter(BaseServiceAdapter):
    """默认适配器，适用于所有 Shell 命令"""

    @staticmethod
    def match(command):
        """所有命令都可以使用 Shell 适配器"""
        return True  # 兜底适配
