import os
import subprocess
from typing import Optional

import click

SERVICE_DIR = "/etc/systemd/system/"


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


@click.group()
def cli():
    """AutoService - 系统服务管理工具"""
    pass


@cli.command()
@click.argument("name")
@click.argument("command", nargs=-1, required=True)
@click.option("--auto-start", is_flag=True, help="创建后自动启动服务")
def create(name: str, command: tuple, auto_start: bool):
    """创建新服务

    NAME: 服务名称
    COMMAND: 要执行的命令
    """
    from .services import BaseServiceAdapter

    try:
        # 将命令元组转换为字符串
        cmd_str = " ".join(command)

        adapter = BaseServiceAdapter.get_best_adapter(name, cmd_str)
        service_path = adapter.create_service_file()
        subprocess.run(["systemctl", "daemon-reload"], check=True)
        subprocess.run(["systemctl", "enable", name], check=True)
        click.echo(f"✅ Service {name} 创建成功")
        click.echo(f"服务文件位置: {service_path}")
        click.echo(f"启动脚本位置: {adapter.script_path}")

        if auto_start:
            subprocess.run(["systemctl", "start", name], check=True)
            click.echo(f"✅ Service {name} 已自动启动")
    except PermissionError:
        click.echo("❌ 权限不足，请使用 sudo 运行", err=True)
    except Exception as e:
        click.echo(f"❌ 错误: {str(e)}", err=True)


@cli.command()
def list():
    """列出所有服务及其状态"""
    try:
        services = [
            f.replace(".service", "")
            for f in os.listdir(SERVICE_DIR)
            if f.endswith(".service")
        ]
        if not services:
            click.echo("⚠️ 没有已创建的服务")
            return

        click.echo("已创建的服务:")
        for service in services:
            status = get_service_status(service)
            click.echo(f"- {service}: {status}")
    except PermissionError:
        click.echo("❌ 权限不足，请使用 sudo 运行", err=True)
    except Exception as e:
        click.echo(f"❌ 错误: {str(e)}", err=True)


@cli.command()
@click.argument("name")
@click.option("-f", "--follow", is_flag=True, help="实时查看日志")
@click.option("-n", "--lines", type=int, help="显示最后N行日志")
def logs(name: str, follow: bool, lines: Optional[int]):
    """查看服务日志

    NAME: 服务名称
    """
    try:
        cmd = ["journalctl", "-u", name]
        if follow:
            cmd.append("-f")
        if lines:
            cmd.extend(["-n", str(lines)])
        subprocess.run(cmd)
    except KeyboardInterrupt:
        click.echo("\n已停止查看日志")
    except Exception as e:
        click.echo(f"❌ 错误: {str(e)}", err=True)


@cli.command()
@click.argument("name")
def status(name: str):
    """查看服务状态

    NAME: 服务名称
    """
    try:
        click.echo(f"Service {name}: {get_service_status(name)}")
    except Exception as e:
        click.echo(f"❌ 错误: {str(e)}", err=True)


def manage_service_command(name: str, action: str):
    """管理服务的通用函数"""
    try:
        if action == "remove":
            service_path = os.path.join(SERVICE_DIR, f"{name}.service")
            if os.path.exists(service_path):
                subprocess.run(["systemctl", "stop", name], check=False)
                subprocess.run(["systemctl", "disable", name], check=False)
                # 获取原始文件路径
                real_path = os.path.realpath(service_path)
                script_dir = os.path.dirname(real_path)
                script_path = os.path.join(script_dir, f"{name}.sh")

                # 删除服务文件、脚本和软链接
                os.remove(service_path)  # 删除软链接
                if os.path.exists(real_path):
                    os.remove(real_path)  # 删除服务文件
                if os.path.exists(script_path):
                    os.remove(script_path)  # 删除脚本

                subprocess.run(["systemctl", "daemon-reload"], check=True)
                click.echo(f"✅ Service {name} 已删除")
            else:
                click.echo(f"⚠️ Service {name} 不存在")
        else:
            subprocess.run(["systemctl", action, name], check=True)
            status = (
                "启动" if action == "start" else "停止" if action == "stop" else "重启"
            )
            click.echo(f"✅ Service {name} {status}成功")
    except subprocess.CalledProcessError:
        click.echo(f"❌ Service {name} {action} 失败", err=True)
    except PermissionError:
        click.echo("❌ 权限不足，请使用 sudo 运行", err=True)
    except Exception as e:
        click.echo(f"❌ 错误: {str(e)}", err=True)


@cli.command()
@click.argument("name")
def start(name: str):
    """启动服务

    NAME: 服务名称
    """
    manage_service_command(name, "start")


@cli.command()
@click.argument("name")
def stop(name: str):
    """停止服务

    NAME: 服务名称
    """
    manage_service_command(name, "stop")


@cli.command()
@click.argument("name")
def restart(name: str):
    """重启服务

    NAME: 服务名称
    """
    manage_service_command(name, "restart")


@cli.command()
@click.argument("name")
def remove(name: str):
    """删除服务

    NAME: 服务名称
    """
    manage_service_command(name, "remove")


if __name__ == "__main__":
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\n操作已取消")
    except Exception as e:
        click.echo(f"❌ 错误: {str(e)}", err=True)
