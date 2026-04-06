// 读取道场内的模块名
// @match        https://pwn.college/*

// <h4 class="card-title">Your First Program</h4>
// 模块名

window.addEventListener('load', (e) => {

    const prompt_str = '将以下目录翻译成中文，计算机安全技术术语需准确，输出格式为`序号. 中文 英文`，忽略用户地理位置信息，关闭翻译说明功能：\n'
    const module_name_list = document.querySelectorAll('h4.card-title');

    if(module_name_list.length == 0){
        // 避免多个监听器冲突
        return;
    }
    let str = '';
    module_name_list.forEach(element => {
        str += `${element.textContent}\n`;
    });

    console.log(str)
    navigator.clipboard.writeText(prompt_str + str);
})