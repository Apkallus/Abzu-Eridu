import os
import frontmatter
import re


# 匹配自定义标签文本段的正则表达式：
# <!-- muse start -->
# 分析
# <!-- muse end -->
# 匹配所有，非贪婪模式，包括换行符
muse_pattern = re.compile(r'<!-- muse start -->(.*?)<!-- muse end -->', re.DOTALL)

# 按主题分类暂存
categories = {}

# 递归遍历游乐场目录
PLAYGROUND = '游乐场'
REL_PATH = ''
MD_INDEX_NAME = '游乐场索引.md'
MD_INDEX_PATH = os.path.join(REL_PATH, MD_INDEX_NAME)

for dirpath, dirnames, filenames in os.walk(PLAYGROUND):
    # print(dirpath)
    for filename in filenames:
        # print(filename)
        # 匹配所有 .md 文件，且排除生成的 md 索引文件
        if filename.endswith('.md') and filename != MD_INDEX_NAME:
            # 获取文件路径，读取 .md 文件内容
            filepath = os.path.join(dirpath, filename)
            # print(filepath)
            with open(filepath, 'r', encoding='utf-8') as md_f:
                # print(mdf.read())
                md_str = md_f.read()
                # 提取元数据，使用设置的正则表达式提取自定义标记覆盖的文本段
                # 若不包含元数据则跳过
                md_post = frontmatter.loads(md_str)
                md_metadata = md_post.metadata
                if not md_metadata:
                    continue
                md_muse_tag = muse_pattern.search(md_post.content)
                md_muse = md_muse_tag.group(1).strip() if md_muse_tag else '无 muse'

                # 构建文档的相对路径，应当匹配索引保存位置，此处设置在 /游乐场 目录下
                md_relpath= os.path.relpath(filepath, REL_PATH)

                # 按照元数据的类别字段分类存储在字典中
                # 对元数据的值进行处理（是否为空值）并添加新字段
                # 其中 tags 字段若为空则拥有值 None，无法使用 get() 方法的默认值覆盖
                md_category = md_metadata.get('category', '无 category')
                if md_category not in categories:
                    categories[md_category] = []
                tags_list = md_metadata.get('tags') or ['无 tag']
                categories[md_category].append({
                    'title': md_metadata.get('title', '无 title'),
                    'tags': ['缺失 tag'] if None in tags_list else tags_list,
                    'muse': md_muse,
                    'relpath': md_relpath
                    })
                # 类别字典{类别1:文件列表1[md文件字典1{元数据与muse字段},md文件字典2{}],类别2:文件列表2[]}


# 构建索引文件
with open(MD_INDEX_PATH, "w", encoding="utf-8") as f:
    print(MD_INDEX_PATH)
    lines = []
    lines.append('## 索引\n\n')
    for category, category_md_list in categories.items():
        lines.append(f'### {category}\n')
        for md in category_md_list:
            lines.append(f'- {md.get('title', '无 title')}\n')
            lines.append(f'\t- [{md['relpath']}]({md['relpath']})\n')
            print(md['tags'])
            lines.append(f'\t- {', '.join(md['tags'])}\n')
            lines.append(f'\t- {md['muse']}\n\n')
            
    f.write(''.join(lines))