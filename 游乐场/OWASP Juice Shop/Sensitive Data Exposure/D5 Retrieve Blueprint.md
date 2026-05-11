---
title: Retrieve Blueprint
description: 分析产品图片的元数据，定位构建蓝图或模型的软件，在可能的路径由可能的文件名与扩展名暴力破解
---

- 描述：通过下载其中一个产品的蓝图，剥夺商店的收入。
- 查看示例解决方案：
    - 查看商品图片与描述，定位可能使用蓝图制造的商品
        ```OWASP Juice Shop Logo (3D-printed)```
    - 下载图片分析元数据，得到
        ```
        照相机制造商：OpenSCAD
        照相机型号：https://imgur.com/a/GeHQP
        ```
    - 搜索 OpenSCAD
        - 此为 3D 模型构建软件
        https://openscad.org/
    
    - 示例解决方案定位到支持的扩展文件名 .stl 后开始爆破
        > 研究相机型号条目 OpenSCAD 揭示，这是一个创建 3D 模型的程序，它使用 .stl 文件工作
        由于没有提供关于蓝图文件名或其他任何提示，你唯一的选择就是幸运猜测或暴力破解攻击
        Download http://localhost:3000/assets/public/images/products/JuiceShop.stl to solve this challenge
    - 然而此软件支持多个文件类型
        > SVG 用于 2D，同时 AutoCAD DXF 文件也可以用作 2D 轮廓的数据交换格式。除了用于挤压的 2D 路径外，还可以从 DXF 文件中读取设计参数。除了 DXF 文件，OpenSCAD 还可以读取和创建 3D 模型，支持开放的 3mf、STL、OFF 以及许多其他文件格式