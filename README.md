# 四叶草

### 已完成功能
- 自动世界树
- 每日矿场
- 自动登录
- 遗迹探索
### 接下来的
- 自动高级素材
### 已知问题
- 自动探索采用穷举寻找下一节点（日后会优化的，大概。。。

### 遇到报错
```
uiautomator2.exceptions.JsonRpcError: -32001 Jsonrpc error: <java.lang.SecurityException> data: java.lang.Secu rityException: Injecting to another application requires INJECT_EVENTS permission
```
解决方法：
```angular2html
开启模拟器中的开发者模式->开启usb调试
```