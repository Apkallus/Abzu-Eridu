## 任务项

自启动
- 任务计划程序 
    `%windir%\system32\taskschd.msc`
    - 设置任务项（开机自启项为任务项子类）
        - 设置启动延迟 
            `触发器 - 高级设置 延迟任务时间`

- 注册表 
    `regedit`
    - 用户注册表                
        `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
    - 系统注册表          
        `HKLM\Software\Microsoft\Windows\CurrentVersion\Run`
- 服务
    `services.msc`
    - 设置服务启动类型

复制注册表的程序路径与参数到任务计划中，并删除注册表项，以精确控制启动时延

延后同步/备份程序