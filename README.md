<h1 align="center">四叶草小助手</h1>

<div align="center">

[![License](https://img.shields.io/badge/License-MIT%202.0-blue.svg)](https://opensource.org/licenses/MIT-2.0)
![Windows](https://img.shields.io/badge/-Windows%20x64-0078D6?logo=microsoft)
![macOS](https://img.shields.io/badge/-macOS%20Arm64-000000?logo=apple)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/AutoCloverTheater/AutoCloverTheater)
[![Version](https://img.shields.io/github/v/release/AutoCloverTheater/AutoCloverTheater?color=blue&label=Version)](https://github.com/AutoCloverTheater/AutoCloverTheater/releases)

[//]: # ( ![Platform]&#40;https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-blueviolet&#41;)


</div>

### 项目概述
本项目是一个自动化脚本集合，旨在实现游戏内的多种自动化任务，如自动世界树、每日矿场、自动登录等。项目使用Python编写，并依赖于uiautomator2库与模拟器进行交互。


### 使用指引
## 1. docker
- 使用docker-compose运行docker镜像

**docker-compose**：
```bash
   docker-compose up -d
```
#### 或者

1. 克隆本仓库：
```bash
  git clone https://github.com/AutoCloverTheater/AutoCloverTheater.git
```
2. 复制 `env.yaml.example` 文件并重命名为 `env.yaml`：
```bash
  cd /yourpath/AutoCloverTheater/etc
  cp env.yaml.example env.yaml
```
3. 安装 依赖项：
```bash
  pip install -e .
  pip install -r requirements.txt
```
4. 运行
```
python  main.py
```
5. 浏览器访问
```angular2html
http://127.0.0.1:8233/
```
### 已完成功能
- 自动世界树
- 每日矿场
- 每日高难度素材
- 遗迹探索
- 工会每日

### 接下来要做的
- 每日素材本
- 每日商店免费资源
- 删除用不到的静态资源
### 遇到报错
```
uiautomator2.exceptions.JsonRpcError: -32001 Jsonrpc error: <java.lang.SecurityException> data: java.lang.Secu rityException: Injecting to another application requires INJECT_EVENTS permission
```
### 解决方法
- 开启模拟器中的开发者模式->开启usb调试

### 已知问题
- uiautomator2在操作模拟器的时候人工操作模拟器可能导致断连