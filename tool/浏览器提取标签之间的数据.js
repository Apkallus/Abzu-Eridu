// 从选定的起始与结尾元素之间提取数据，即 [start, end] 包含首尾


function insert_mark(selector_start, selector_end, start_mark, end_mark) {
    // 传入起始元素、结束元素的 css 选择器字符串
    /// 在起始元素前、结束元素尾插入注释标记
    const element_start = document.querySelector(selector_start);
    const element_end = document.querySelector(selector_end);

    element_start.before(start_mark);
    element_end.after(end_mark);
    return ;
}

function extract_between_mark(start_mark, end_mark) {
    // 传入作为标记的开头、结尾评论
    /// 在开头结尾之间创建范围元素，得到类文档结构
    const range = document.createRange();
    range.setStartAfter(start_mark);  
    range.setEndBefore(end_mark);    

    /// 类文档结构不包含字符串型方法，于是创建临时元素
    //// 将类文档结构的克隆设置为临时元素的子元素以转为文档后，使用文档以提取 HTML
    const temp_element = document.createElement('temp_element');
    temp_element.appendChild(range.cloneContents());
    const html = temp_element.innerHTML;

    return html;

}

// 分别选中起始与结束元素，浏览器右键复制 CSS 选择器
let selector_start = '';
let selector_end = '';

// 传入 css 选择器
function do_extract(selector_start, selector_end){
  // 创建注释
  let start_mark = document.createComment('START_canary');
  let end_mark = document.createComment('END_canary');

  // 插入标记
  insert_mark(selector_start, selector_end, start_mark, end_mark);
  // 提取标记之间文本
  let res_string = extract_between_mark(start_mark, end_mark);

  // 控制台信息
  console.log(res_string);
  console.log('click web page once');

  // 由于浏览器粘贴板写入需用户交互，此处设置一次性的点击事件监听器，点击任意位置即复制到粘贴板
  document.addEventListener(
      'click', 
      (event) => {
          console.log('get click');
          navigator.clipboard.writeText(res_string);
          // 移除标记节点
          start_mark.remove();
          end_mark.remove();
          event.preventDefault();
      },
      { 
          once: true 
      }
  );
}

// 控制台调用函数 


do_extract(
  'body > h2:nth-child(41)', 
  'body > h2:nth-child(43)'
)



/*
- 或修改为在底部显示一个按钮，点击后复制内容并移除按钮
- 常用功能，设置为函数后加载到油猴扩展
- 或增加功能到页面 css 选择而无需在开发者工具栏中复制后，到 console 粘贴，构想：
  1. console 输入函数名
  2. 提示点击开头元素
  3. 点击开头元素后
    - 显示选中元素
    - 询问是否确认
      - yes：继续
      - no：再次选择开头元素
  4. 点击并选择末尾元素
  5. 在终端打印并复制到粘贴板
*/