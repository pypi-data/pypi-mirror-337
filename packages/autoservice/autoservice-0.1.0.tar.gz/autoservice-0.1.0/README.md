# AutoService

AutoService 是一个命令行工具，用于轻松管理 systemd 服务。它支持通过命令创建、启动、停止、重启和删除服务，并且可以适配多种命令行工具。

## 功能特点

- 支持创建、启动、停止、重启和删除 systemd 服务
- 自动适配不同类型的命令（Python、Shell 等）
- 自动检测 Python 虚拟环境
- 简单易用的命令行界面

## 安装

使用 uv 安装：

```bash
sudo uv tool install
```

## 使用方法

### 创建服务

```bash
sudo autoservice create <服务名> <命令>
```

例如：
```bash
sudo autoservice create my-python-app "python /path/to/app.py"
```

### 列出服务

```bash
sudo autoservice list
```

### 管理服务

启动服务：
```bash
sudo autoservice start <服务名>
```

停止服务：
```bash
sudo autoservice stop <服务名>
```

重启服务：
```bash
sudo autoservice restart <服务名>
```

删除服务：
```bash
sudo autoservice remove <服务名>
```

## 注意事项

- 需要 root 权限来管理 systemd 服务
- 确保命令路径是绝对路径
- Python 服务会自动检测并使用虚拟环境

## 许可证

MIT
