import pathlib

from .base import BaseServiceAdapter


class NpmServiceAdapter(BaseServiceAdapter):
    """适配 Node.js 及 npm 相关命令"""

    @staticmethod
    def match(command):
        """匹配 Node.js 相关命令"""
        first_word = command.split()[0]
        return first_word in {"node", "npm", "yarn", "pnpm"} or command.endswith(".js")

    def get_script_content(self):
        """获取脚本内容，支持 nvm 环境"""
        template_path = (
            pathlib.Path(__file__).parent.parent / "templates" / "npm_script.template"
        )
        with open(template_path, "r") as f:
            template = f.read()

        return template.format(working_dir=self.cwd, command=self.command)
