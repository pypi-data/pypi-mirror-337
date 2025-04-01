import os
import pathlib
import stat


class BaseServiceAdapter:
    """所有适配器的基类"""

    registered_adapters = []
    SYSTEMD_DIR = "/etc/systemd/system"

    def __init__(self, service_name, command, cwd=None):
        self.service_name = service_name
        self.command = command
        self.cwd = cwd or os.getcwd()
        # 将脚本和服务文件放在当前工作目录的 scripts 文件夹下
        self.script_dir = os.path.join(self.cwd, "scripts")
        self.script_path = os.path.join(self.script_dir, f"{service_name}.sh")
        self.service_path = os.path.join(self.script_dir, f"{service_name}.service")

    def create_script(self):
        """创建启动脚本"""
        os.makedirs(self.script_dir, exist_ok=True)
        script_content = self.get_script_content()

        with open(self.script_path, "w") as f:
            f.write(script_content)

        # 添加执行权限
        st = os.stat(self.script_path)
        os.chmod(self.script_path, st.st_mode | stat.S_IEXEC)

        return self.script_path

    def create_service_file(self):
        """创建服务文件"""
        os.makedirs(self.script_dir, exist_ok=True)
        service_content = self.generate_service_content()

        with open(self.service_path, "w") as f:
            f.write(service_content)

        # 创建软链接到 systemd 目录
        systemd_link = os.path.join(self.SYSTEMD_DIR, f"{self.service_name}.service")
        if os.path.exists(systemd_link):
            os.remove(systemd_link)
        os.symlink(self.service_path, systemd_link)

        return self.service_path

    def get_script_content(self):
        """获取脚本内容"""
        template_path = (
            pathlib.Path(__file__).parent.parent / "templates" / "script.template"
        )
        with open(template_path, "r") as f:
            template = f.read()

        return template.format(working_dir=self.cwd, command=self.command)

    def generate_service_content(self):
        """生成 systemd 服务文件内容"""
        script_path = self.create_script()
        template_path = (
            pathlib.Path(__file__).parent.parent / "templates" / "service.template"
        )

        with open(template_path, "r") as f:
            template = f.read()

        return template.format(
            service_name=self.service_name,
            exec_command=script_path,
            working_dir=self.cwd,
            user=os.getenv("USER", "root"),
        )

    @classmethod
    def register_adapter(cls, adapter):
        """注册适配器"""
        cls.registered_adapters.append(adapter)

    @classmethod
    def get_best_adapter(cls, service_name, command):
        """遍历所有适配器，找到最匹配的"""
        for adapter in cls.registered_adapters:
            if adapter.match(command):
                return adapter(service_name, command)
        from .shell import ShellServiceAdapter

        return ShellServiceAdapter(service_name, command)  # 默认 Shell 适配
