import os
import pathlib

from .base import BaseServiceAdapter


class PythonServiceAdapter(BaseServiceAdapter):
    """适配 Python 及其生态工具（uv、poetry）"""

    @staticmethod
    def match(command):
        """匹配 Python 相关命令"""
        first_word = command.split()[0]
        return first_word in {"python", "uv", "poetry"} or command.endswith(".py")

    def get_script_content(self):
        """获取脚本内容，支持虚拟环境"""
        env_path = os.environ.get("VIRTUAL_ENV", "")
        if env_path:
            template_path = (
                pathlib.Path(__file__).parent.parent
                / "templates"
                / "python_script.template"
            )
            with open(template_path, "r") as f:
                template = f.read()

            return template.format(
                working_dir=self.cwd, venv_path=env_path, command=self.command
            )
        return super().get_script_content()
