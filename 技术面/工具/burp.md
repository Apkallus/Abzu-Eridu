### burp

安装
- 下载后在浏览器中手动设置代理为 Burp 的监听地址
- [安装Burp CA 证书](https://portswigger.net/burp/documentation/desktop/external-browser-config/certificate)：
    1. 使用浏览器访问拦截代理服务器的地址下载证书
    2. 在浏览器设置中的证书管理器中导入此证书，确保勾选此证书可以标识网站

设置
- User interface 用户界面选项 
    - Display
        - 主题选择 Dark 暗黑模式
        - 界面放大：设置缩放为默认的固定 `1.0` ，尝试调大字体来控制字体清晰度以及界面缩放。若仅调整缩放则光标错位。
            - 字体20
            - 开启配置缩放
                - 光标偏移错位修复
                <https://www.52pojie.cn/thread-1908732-1-1.html>
    - Message editor
        - 更改默认信息显示字体为 Consolas(仅限英文)
        - 下载中英文等宽字体 https://github.com/SpaceTimee/Fusion-JetBrainsMapleMono
- 内置 chrome 浏览器
    - appearance 
        - theme 主题设置 dark
        - 自定义字体大小 18
        - 页面缩放 125%
- Network 网络选项
    - Connections
        - SOCKS proxy 设置 burp 连接到的代理
- 控制面板
    - 设置
        - 扫描详情
            - URL scope 设置 suite scope 以仅解析范围内 URL


使用
- [官网文档](https://portswigger.net/burp/documentation/desktop)
- Scan 爬取或扫描，可配置凭证
- Engagement tools 
    - Discover content 自动化内容发现工具查找隐藏的目录、文件及其他端点
    - Analyze target 目标分析器查看已映射的内容
- Intruder
    - 字符翻转或位翻转，查看令牌的实际有效部分
- BApp 插件：输出在日志或仪表盘中
    - Param Miner 发现潜在的隐藏输入
        - Guess params
    

- 插件
    :warning: 若出现功能异常，检查扩展设置或关闭扩展后重试