// 导入 express 模块，并调用初始化函数
const express = require("express");
const app  = express();

// 中间件添加回调函数，查看响应头部
app.use((req, res, next) => {
    // 设置事件监听器，当响应触发结束事件时：打印状态码 + 状态信息 + 头部
    res.on('finish', () => {
        console.log('Status:', res.statusCode);
        console.log('StatusMessage:', res.statusMessage);
        console.log('Response Headers:', res.getHeaders());
    });
    // 继续传递，而非作为最终端点
    next();
});   

// 导航到根目录的所有请求方法
app.all("/", (req, res) => {
    // 返回字符串
    res.send("Hello World!");
});

// 监听端口
app.listen(9999, () => {
    // 回调函数打印成功信息
    console.log(`CORS Playground running on port 9999`);
});