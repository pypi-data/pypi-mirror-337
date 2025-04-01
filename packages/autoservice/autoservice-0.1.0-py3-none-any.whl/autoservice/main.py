import argparse
import os
import subprocess

from .commands import Command, registry
from .services import BaseServiceAdapter

SERVICE_DIR = "/etc/systemd/system/"


def create_service_handler(args):
    """创建服务处理函数"""
    try:
        # 将命令列表组合成字符串
        command = " ".join(args.command)
        adapter = BaseServiceAdapter.get_best_adapter(args.name, command)
        service_path = adapter.create_service_file()
        subprocess.run(["systemctl", "daemon-reload"], check=True)
        subprocess.run(["systemctl", "enable", args.name], check=True)
        print(f"✅ Service {args.name} 创建成功")
        print(f"服务文件位置: {service_path}")
        print(f"启动脚本位置: {adapter.script_path}")

        if args.auto_start:
            subprocess.run(["systemctl", "start", args.name], check=True)
            print(f"✅ Service {args.name} 已自动启动")
    except PermissionError:
        print("❌ 权限不足，请使用 sudo 运行")


def list_services_handler(args):
    """列出服务处理函数"""
    try:
        services = [
            f.replace(".service", "")
            for f in os.listdir(SERVICE_DIR)
            if f.endswith(".service")
        ]
        if not services:
            print("⚠️ 没有已创建的服务")
            return

        print("已创建的服务:")
        for service in services:
            status = get_service_status(service)
            print(f"- {service}: {status}")
    except PermissionError:
        print("❌ 权限不足，请使用 sudo 运行")


def get_service_status(service_name: str) -> str:
    """获取服务状态"""
    try:
        result = subprocess.run(
            ["systemctl", "is-active", service_name], capture_output=True, text=True
        )
        status = result.stdout.strip()
        if status == "active":
            return "🟢 运行中"
        elif status == "inactive":
            return "⚫ 已停止"
        else:
            return "🔴 异常"
    except Exception:
        return "❓ 未知"


def view_logs_handler(args):
    """查看日志处理函数"""
    try:
        cmd = ["journalctl", "-u", args.name]
        if args.follow:
            cmd.append("-f")
        if args.lines:
            cmd.extend(["-n", str(args.lines)])
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n已停止查看日志")


def status_handler(args):
    """查看状态处理函数"""
    status = get_service_status(args.name)
    print(f"Service {args.name}: {status}")


def manage_service_handler(args):
    """管理服务处理函数"""
    try:
        if args.command == "remove":
            service_path = os.path.join(SERVICE_DIR, f"{args.name}.service")
            if os.path.exists(service_path):
                subprocess.run(["systemctl", "stop", args.name], check=False)
                subprocess.run(["systemctl", "disable", args.name], check=False)
                # 获取原始文件路径
                real_path = os.path.realpath(service_path)
                script_dir = os.path.dirname(real_path)
                script_path = os.path.join(script_dir, f"{args.name}.sh")

                # 删除服务文件、脚本和软链接
                os.remove(service_path)  # 删除软链接
                if os.path.exists(real_path):
                    os.remove(real_path)  # 删除服务文件
                if os.path.exists(script_path):
                    os.remove(script_path)  # 删除脚本

                subprocess.run(["systemctl", "daemon-reload"], check=True)
                print(f"✅ Service {args.name} 已删除")
            else:
                print(f"⚠️ Service {args.name} 不存在")
        else:
            subprocess.run(["systemctl", args.command, args.name], check=True)
            status = (
                "启动"
                if args.command == "start"
                else "停止"
                if args.command == "stop"
                else "重启"
            )
            print(f"✅ Service {args.name} {status}成功")
    except subprocess.CalledProcessError:
        print(f"❌ Service {args.name} {args.command} 失败")
    except PermissionError:
        print("❌ 权限不足，请使用 sudo 运行")


# 注册命令
def register_commands():
    """注册所有命令"""
    # create 命令
    registry.register(
        Command(
            name="create",
            help="创建新服务",
            handler=create_service_handler,
            arguments=[
                {
                    "flags": ["name"],
                    "help": "服务名称",
                    "metavar": "服务名",
                },
                {
                    "flags": ["command"],
                    "help": "要执行的命令",
                    "nargs": argparse.REMAINDER,  # 收集剩余的所有参数
                    "metavar": "命令",
                },
                {
                    "flags": ["--auto-start"],
                    "help": "创建后自动启动服务",
                    "action": "store_true",
                    "default": False,
                },
            ],
        )
    )

    # list 命令
    registry.register(
        Command(
            name="list",
            help="列出所有服务及其状态",
            handler=list_services_handler,
            arguments=[],
        )
    )

    # logs 命令
    registry.register(
        Command(
            name="logs",
            help="查看服务日志",
            handler=view_logs_handler,
            arguments=[
                {"flags": ["name"], "help": "服务名称", "metavar": "服务名"},
                {
                    "flags": ["-f", "--follow"],
                    "help": "实时查看日志",
                    "action": "store_true",
                    "default": False,
                },
                {
                    "flags": ["-n", "--lines"],
                    "help": "显示最后N行日志",
                    "type": int,
                    "metavar": "N",
                    "default": None,
                },
            ],
        )
    )

    # status 命令
    registry.register(
        Command(
            name="status",
            help="查看服务状态",
            handler=status_handler,
            arguments=[{"flags": ["name"], "help": "服务名称", "metavar": "服务名"}],
        )
    )

    # 服务管理命令
    for cmd, desc in [
        ("start", "启动服务"),
        ("stop", "停止服务"),
        ("restart", "重启服务"),
        ("remove", "删除服务"),
    ]:
        registry.register(
            Command(
                name=cmd,
                help=desc,
                handler=manage_service_handler,
                arguments=[
                    {"flags": ["name"], "help": "服务名称", "metavar": "服务名"},
                    {
                        "flags": ["--command"],
                        "help": argparse.SUPPRESS,
                        "default": cmd,
                    },
                ],
            )
        )


def main():
    register_commands()
    registry.execute()


if __name__ == "__main__":
    main()
