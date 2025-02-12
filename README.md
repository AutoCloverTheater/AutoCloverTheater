<div style="text-align: center">

# 四叶草小助手

</div>

![License](https://img.shields.io/github/license/AutoCloverTheater/AutoCloverTheater)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-blueviolet)
![GitHub commit activity](https://img.shields.io/github/commit-activity/y/AutoCloverTheater/AutoCloverTheater)
![Version](https://img.shields.io/badge/Version-0.1.0-blue)

### 项目概述
本项目是一个自动化脚本集合，旨在实现游戏内的多种自动化任务，如自动世界树、每日矿场、自动登录等。项目使用Python编写，并依赖于uiautomator2库与模拟器进行交互。

### 目录说明
```
.
├── README.md                         # 项目简介及使用指南
├── LICENSE                           # 许可证
├── env.yaml.example                  # 环境变量配置
├── mac                               # macOS平台下模拟器控制脚本
│   └── emulator                      # 模拟器接口实现
├── facades                           # 各类功能模块封装
│   ├── App                           # 应用层接口
│   ├── Configs                       # 配置管理
│   ├── Constant                      # 常量定义
│   ├── Detect                        # 图像识别与检测
│   │   ├── Common                    # 常用检测逻辑
│   │   ├── Items                     # 物品检测
│   │   ├── Refinery                  # 神秘矿厂相关检测
│   │   ├── Relic                     # 遗迹相关检测
│   │   └── WorldTree                 # 世界树相关检测
│   ├── Emulator                      # 模拟器驱动程序
│   ├── Env                           # 环境变量管理
│   ├── Img                           # 图像处理工具
│   ├── Logx                          # 日志记录工具
│   ├── Ocr                           # OCR文字识别
│   ├── Runner                        # 任务执行器
│   │   └── core                      # 暂时没用到的函数
│   │   └── layout                    # 可通用的任务执行器
│   └── tool                          # 辅助工具（主要是截取世界树卡组的图片）
├── win                               # Windows平台下模拟器控制脚本
│   └── emulator                      # 模拟器接口实现
└── app                               # 应用服务端代码
    ├── api                           # API接口
    └── webui                         # Web界面
```
### 使用指引
在运行本项目之前，请确保已安装以下依赖项：
- python 3.10
- git
- pip（Python 包管理工具）

1. 克隆本仓库：
```
git clone https://github.com/AutoCloverTheater/AutoCloverTheater.git
```
2. 复制 `env.yaml.example` 文件并重命名为 `env.yaml`：
```
cd /yourpath/AutoCloverTheater
cp env.yaml.example env.yaml
```
3.安装 依赖项：
```
$ pip install -r requirements.txt
```

4.修改env.yaml中的参数
```
// 你的账号（可选），因为你游换设备登录会把旧设备踢下线，我经常换设备所以保留了输入账号密码。
ACCOUNT:'your_account'
// 你的密码（可选）
PASSWORD:'your_password'
// 模拟器路径类似
EMULATORPATH:'/Applications/MuMuPlayer.app/Contents/MacOS'
// 模拟器类型:mumu（目前仅在mumu上测试过
EMULATORTYPE:'mumu'
// 模拟器地址
ADDR: '127.0.0.1'
// 模拟器端口
SERIAL: 5555
```


### 已完成功能
- 自动世界树
- 每日矿场
- 每日高难度素材
- 遗迹探索
- - 工会每日

### 接下来要做的
- 删除用不到的静态资源

### 遇到报错
```
uiautomator2.exceptions.JsonRpcError: -32001 Jsonrpc error: <java.lang.SecurityException> data: java.lang.Secu rityException: Injecting to another application requires INJECT_EVENTS permission
```
解决方法：
- 开启模拟器中的开发者模式->开启usb调试

### 已知问题
- uiautomator2在操作模拟器的时候人工操作模拟器可能导致断连