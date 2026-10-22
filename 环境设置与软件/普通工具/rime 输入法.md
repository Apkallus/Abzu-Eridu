# rime 输入法

[rime](https://rime.im/)

- 输入方案
    - 简化字，之后使用雾凇拼音配置包覆盖
- 配色
    - 暗堂
- 快捷键
    - 切换输入方案
        - `F4` 或 ``Ctrl + ` ``
    - 候选全角/半角符号时，再次输入同一符号既切换。例如 `1.` 再次输入则为 `1。`
        - 来自 `default.yaml` 的 `punctuator/digit_separators` 项
        
## 配置包

[雾凇拼音](https://github.com/iDvel/rime-ice)
- 清空用户目录后，复制配置文件
- 符号配置 `./symbols_v.yaml`
    ```yaml
    # 使用 `v` 模式，调出 emoji/符号字典

    # 设置 `vvv` 为自定义 emoji
    'vvv': []
    ```
    - 不直接修改配置文件，而是使用自定义补丁配置，更新时不会被覆盖
- 词语到 emoji 映射 `./opencc/emoji.txt`
- 自定义短语 `./custom_phrase.txt`，配置 `custom_phrase/user_dict`

## 自定义补丁配置

[rime wiki](https://github.com/rime/home/wiki/CustomizationGuide)
- 设置补丁文件后，重新部署以生效
- 查看 `default.yaml` 获取设定项名

```yaml
# `patch` 自定义配置头（补丁）
patch:
    "一級設定項/二級設定項/三級設定項": 新的設定值
    "另一個設定項": 新的設定值
```

在用户目录设置默认补丁文件 `./default.custom.yaml`

```yaml
# default.custom.yaml
patch:
    # 候选词个数
    menu/page_size: 7
    
    # 切换方案与快捷键
    # 仅保留雾凇拼音而设置空快捷键
    switcher:
        caption: 「切换方案」
        hotkeys:
            # - F4

```

在用户目录设置雾凇拼音的补丁文件 `./rime_ice.custom.yaml`

```yaml
# rime_ice.custom.yaml
patch:
    # 自定义 emoji
    punctuator/symbols:
        vvv: [ §, 🎯, 🖇️, ⚔️, 🛠️, 🥷, 🌟, ♾️, 📌, 📅, 🔍, ❓, ⏸️ ]

    # 加载自定义短语文件，对应 `./custom_phrase_my.txt`
    custom_phrase/user_dict: "custom_phrase_my"

```

设置自定义短语文件 `./custom_phrase_my.txt`
- 格式，以 Tab 分割：`显示词汇<Tab>输入编码<Tab>排序权重`（输入法的短语 `tab` 即可获得制表符）
- 用来跨配置保存 emoji 

```txt
🛠️	gj	99
🛠️	gongju	99

```

样式文件 `./weasel.yaml` 的自定义样式覆盖文件 

```yaml
# weasel.custom.yaml
patch:
    # 切换中英文时通知图标显示的时长，默认 1200ms。缩短
    show_notifications_time: 500
    
```