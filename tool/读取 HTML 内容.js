// 使用 eval 动态执行元素选择，获取 HTML 字符串到 LLM 格式化并翻译
// 若提供字典，则在基础元素内查找子孙元素

/*

<h4 class="accordion-item-name" data-challenge-index="1" data-challenge-id="chown" data-challenge-name="Changing File Ownership" id="challenges-header-1">
    <i class="challenge-icon pr-3 fas fa-flag challenge-solved "></i>
    <span class="pr-2">Changing File Ownership</span>
</h4>

*/
// 选择模块标题与描述、挑战标题与描述
const pwn_collenge_mod_content = [
    "document.querySelector('h1').outerHTML",
    "document.querySelector('div.container:nth-child(2) > div:nth-child(1)').outerHTML",
    {
        "base_element": ".accordion-item", 
        "sub_element": [
            "base_element.querySelector('h4')?.outerHTML ?? ''",
            "base_element.querySelector('.embed-responsive')?.outerHTML ?? ''"
        ],
    },
]

/* 模块名 HTML 标签

<h4 class="card-title">Hello Hackers</h4>

*/
/* 预期输出
    
Hello Hackers
Pondering Paths
Comprehending Commands
...

*/
/* 翻译提示语

本次为模块名目录翻译任务，输出格式为 `{递增数字序号}.o {中文翻译} {原英文}.md`
- 此处的 `{}` 仅为占位符边界示意，不包含在输出中
- 数字序号从1开始

*/
const pwn_collenge_mod_title = [
    {
        // 选择所有包含模块名的标签
        "base_element": "h4.card-title", 
        // 提取标签内文本
        "sub_element": [
            "base_element.innerText ?? ''",
        ],
    },
]


/*

若仅提取特定内容，例如属性值或文本内容，而非整个元素。只需添加一小段
"base_element.querySelector('h4').getAttribute('data-challenge-name')",
"base_element.querySelector('.challenge-description').textContent"

半自动化仅限于此，略有提升的可能改进：
- 修改为 JSON，设置固定项目例如 `当前元素，当前提取目标，若提取属性则提供属性名`
    ```
    h4, attribute, data-challenge-name
    .challenge-description, textContent
    ```
*/
function get_content(content_list) {
    let res_str = '';
    content_list.forEach(query => {
        console.log(`cur query: ${query}`)
        
        if (typeof(query) == 'string') {
            // 若为单项，则直接提取
            console.log('is string')
            let cur_str = eval(query);
            console.log(cur_str)
            res_str += cur_str + '\n';

        } else {
            // 若为复合项，则遍历提取
            console.log('not string')
            const base_element_list = document.querySelectorAll(query["base_element"]);
            console.log(base_element_list)
            
            // 遍历每个基础元素
            base_element_list.forEach(base_element => {
                console.log(base_element)
                // 遍历查询项，以 base_element 为基准元素，查询本元素或子孙元素
                query["sub_element"].forEach(sub_element => {
                    console.log(sub_element)
                    let cur_str = eval(sub_element);
                    console.log(res_str);
                    res_str += cur_str + '\n';
                });
            });
        }
    });

    // 由于浏览器粘贴板写入需用户交互，此处设置一次性的点击事件监听器，点击任意位置即复制到粘贴板
    document.addEventListener(
        'click', 
        (event) => {
            console.log('get click');
            navigator.clipboard.writeText(res_str);
            event.preventDefault();
        },
        { 
            once: true 
        }
    );
}

const content_list = pwn_collenge_mod_content
get_content(content_list)
