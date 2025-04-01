# AutoService

一个简单高效的 systemd 服务管理工具。

## 痛点

- systemd 服务创建流程繁琐，需要手动编写配置文件
- 不同类型程序（Python、Shell等）的服务配置方式不同
- 服务管理命令分散，使用不便

## 解决方案

- 自动生成标准化的服务配置文件
- 智能识别命令类型，自动适配不同运行环境
- 统一的命令行接口管理全部服务

## 使用效果

```bash
# 创建服务（自动处理配置文件）
sudo autoservice create my-app "python app.py"

# 支持 Python 虚拟环境
sudo autoservice create venv-app "poetry run python app.py"

# 查看服务状态
sudo autoservice list
my-app: 🟢 运行中
venv-app: ⚫ 已停止

# 实时查看日志
sudo autoservice logs my-app -f

# 服务管理
sudo autoservice start my-app
sudo autoservice stop my-app
sudo autoservice restart my-app
sudo autoservice remove my-app
```

## 安装

```bash
sudo pip install autoservice
```

## 功能特点

- 支持创建、启动、停止、重启和删除 systemd 服务
- 自动适配不同类型的命令（Python、Shell 等）
- 自动检测 Python 虚拟环境
- 简单易用的命令行界面

## 使用方法

### 创建服务

```bash
sudo autoservice create <服务名> <命令>
```