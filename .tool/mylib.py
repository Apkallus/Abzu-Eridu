def read_or_creat_file(md_input_file_path: str):
    # 从文件读取内容，若不存在则创建
    try:
        with open(md_input_file_path, 'r+', encoding='utf-8') as f:
            md_text = f.read()
    except FileNotFoundError:
        with open(md_input_file_path, 'x', encoding='utf-8') as f:
            pass
    return md_text

def write_to_file(md_output_file_path: str, text: str):
    with open(md_output_file_path, 'w', encoding='utf-8') as f:
        f.write(text)

def url_trans(origin_url: str, replace_list: list[tuple[str, str]]):
    """url_trans(origin_url, replace_list[(old, new)..])"""
    for old, new in replace_list:
        origin_url = origin_url.replace(old, new)
    return origin_url

