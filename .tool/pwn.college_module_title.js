// 在道场的模块页面加载后，选择模块名与挑战名，并添加md标题符号。
// 使用浏览器控制台命令 copy 复制标题字符串到粘贴板 -> 改为设置事件监听器触发粘贴板api

//<h4 class="accordion-item-name" data-challenge-index="1" data-challenge-id="chown" data-challenge-name="Changing File Ownership" id="challenges-header-1">
//    <i class="challenge-icon pr-3 fas fa-flag challenge-solved "></i>
//    <span class="pr-2">Changing File Ownership</span>
//</h4>

window.addEventListener('load', (e) => {

    const prompt_str = '将以下目录翻译成中文，计算机安全技术术语需准确，内容保留原 Markdown 结构，完整输出应包裹在一个可复制的 Markdown 代码块中，忽略用户地理位置信息，关闭翻译说明功能：\n'
    const module_name = document.querySelector('h1');
    // const challenges = document.querySelectorAll('.pr-2');
    // 文本段读取修改为属性读取，同时仅限挑战标题而排除讲座标题
    const challenges = document.querySelectorAll('h4[data-challenge-name]');

    let str = `# ${module_name.textContent}\n\n\n`;
    str += `## Challenge\n\n\n`;

    challenges.forEach(element => {
        // str += `### ${element.textContent}\n\n\n`;
        // 从属性读取属性值
        str += `### ${element.getAttribute('data-challenge-name')}\n\n\n`;
    });

    console.log(str)
    // copy(prompt_str + str);
    // copy 仅限控制台
    navigator.clipboard.writeText(prompt_str + str);
})

