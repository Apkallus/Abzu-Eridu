def read_or_creat_file(file_path: str):
    """从文件读取内容，若不存在则创建"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        with open(file_path, 'x', encoding='utf-8') as f:
            pass
        print('FileNotFound')
        return ""
    
def write_to_file(file_path: str, data: str|bytes, mod: str):
    # with open(file_path, mod, encoding='utf-8') as f:
    if 'b' in mod:
        with open(file_path, mod) as f:
            f.write(data)
    else:
        with open(file_path, mod, encoding='utf-8') as f:
            f.write(data)        

def url_trans(origin_url: str, replace_list: list[tuple[str, str]]):
    """url_trans(origin_url, replace_list[(old, new)..])"""
    for old, new in replace_list:
        origin_url = origin_url.replace(old, new)
    return origin_url

