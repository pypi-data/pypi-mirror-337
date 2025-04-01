import argparse
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable, Dict, List


@dataclass
class Command:
    """命令定义类"""

    name: str
    help: str
    handler: Callable
    arguments: List[Dict[str, Any]]


class CommandRegistry:
    """命令注册中心"""

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="AutoService - 系统服务管理工具",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        self.subparsers = self.parser.add_subparsers(dest="command", required=True)
        self.commands: Dict[str, Command] = {}

    def register(self, command: Command):
        """注册命令"""
        self.commands[command.name] = command
        # 创建子命令解析器
        subparser = self.subparsers.add_parser(command.name, help=command.help)
        # 添加命令参数
        for arg in command.arguments:
            # 创建参数字典的副本
            arg_copy = deepcopy(arg)
            flags = arg_copy.pop("flags")
            subparser.add_argument(*flags, **arg_copy)

    def execute(self, args=None):
        """执行命令"""
        try:
            parsed_args = self.parser.parse_args(args)
            command = self.commands.get(parsed_args.command)
            if command:
                command.handler(parsed_args)
            else:
                self.parser.print_help()
        except Exception as e:
            print(f"❌ 错误: {str(e)}")
            self.parser.print_help()


# 创建全局命令注册中心
registry = CommandRegistry()
