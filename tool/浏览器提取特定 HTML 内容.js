// 使用 eval 动态执行元素选择，获取 HTML 字符串到 LLM 格式化并翻译
// 若提供字典，则在基础元素内查找子孙元素

/*

<h4 class="accordion-item-name" data-challenge-index="1" data-challenge-id="chown" data-challenge-name="Changing File Ownership" id="challenges-header-1">
    <i class="challenge-icon pr-3 fas fa-flag challenge-solved "></i>
    <span class="pr-2">Changing File Ownership</span>
</h4>

*/

/**  
 * 类属性注解的自定义类型
 * @typedef {Object} Query
 * @property {string} element - 元素 css 选择器
 * @property {string} grep_mod - 提取类型
 * @property {string[] | undefined} [exclude_list] - 排除元素 css 选择器列表
 */    

/**  
 * @typedef {Object} Content
 * @property {string | undefined} base_element
 * @property {Query[]} query_list
 */ 

/** 
 * 选择模块标题与描述，挑战标题与描述
 * @type {Content[]}
 */
const pwn_college_grep_mod_content = [
    {
        base_element: undefined,
        query_list: [
            {
                element: 'h1', 
                grep_mod: "outerHTML"
            },
            {
                element: 'div.container:nth-child(2) > div:nth-child(1)',
                grep_mod: "outerHTML",
                exclude_list: [".github-edit-link"]
            }
        ]
    },
    {
        base_element: ".accordion-item",
        query_list: [
            {
                element: 'h4',
                grep_mod: "outerHTML"
            },
            {
                element: '.embed-responsive',
                grep_mod: "outerHTML",
                exclude_list: [".github-edit-link"]
            }
        ]
    },
]

// ------------

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
const pwn_college_grep_mod_title = [
    {
        // 选择所有包含模块名的标签
        "base_element": "h4.card-title", 
        // 提取标签内文本
        "sub_element": [
            "base_element.innerText ?? ''",
        ],
    },
]


// --------

/*  https://p.ost2.fyi/courses

<h2 class="course-name">
    <span class="course-code">Arch1001_x86-64_Asm</span>
    <span class="course-title">Architecture 1001: x86-64 Assembly</span>
    <span class="course-organization">OpenSecurityTraining2</span>
</h2>
*/

const ost2_course_title = [
    {
        // 选择所有包含课程的标签
        "base_element": "h2.course-name", 
        // 提取课程名称标签内文本
        "sub_element": [
            "base_element.querySelector('.course-title').innerText ?? ''",
        ],
    },
]

// --------
/** 
 * @param {Node} element
 * @param {Query} query 
 */
function clone_exclude_grep(element, query) {  
    // 若存在移除项，在克隆元素中移除。若不存在则传递原始元素
    let target = element;
    if (query.exclude_list != undefined) {
        // 创建克隆元素
        target = element.cloneNode(true);
        // 批量查询，并移除
        const selectors = query.exclude_list.join(',');
        console.log('selectors', selectors);
        target.querySelectorAll(selectors).forEach(el => el.remove());
    } 
    // 提取内容
    const grep_data = target[query.grep_mod];
    if (grep_data == undefined) {
        throw new Error("grep_data undefined", query.grep_mod);
    }
    return grep_data;
}

/** @param {Content[]} content_list */
function do_task(content_list) {
    const res_list = [];
    for (const content of content_list) {

        // 选择基准元素列表：文档或自定义元素。格式统一为列表
        /** @type {Element[] | Document[]} */
        const base_elements = content.base_element != undefined
            ? document.querySelectorAll(content.base_element)
            : [window.document];

        console.log('base_elements: ', base_elements);

        // 基于基准元素，执行查询
        for (const base_element of base_elements) {
            for (const query of content.query_list) {
                // 查询内容包含：选择元素、提取类型、排除项
                console.log('query: ', query);

                // 选取元素列表
                /** @type {NodeList} */
                const elements = base_element.querySelectorAll(query.element);
                console.log('elements: ', elements);
                
                for (const element of elements) {
                    console.log('element: ', element);
                    
                    // 对元素创建克隆。在克隆中移除排除项，返回剩余克隆内容
                    const grep_data = clone_exclude_grep(element, query);
                    console.log('grep_data: ', grep_data);
                    res_list.push(grep_data);
                }
            }
        }
    }
    return res_list;
}

/** @param {Content[]} content_list */
function task_main(content_list) {

    const res_list = do_task(content_list);
    const res_str = res_list.join('\n');

    console.log('点击页面任意位置以复制');
    // 由于浏览器粘贴板写入需用户交互，此处设置一次性的点击事件监听器，点击任意位置即复制到粘贴板
    document.addEventListener('click', (event) => {
            console.log('得到点击');
            navigator.clipboard.writeText(res_str)
                .then(() => console.log("成功复制到剪贴板"))
                .catch((error) => console.log("复制失败", error));
            event.preventDefault();
        },
        { once: true }
    );
}

const content_list = pwn_college_grep_mod_content;
// const content_list = pwn_college_grep_mod_title;
// const content_list = ost2_course_title;
task_main(content_list);
