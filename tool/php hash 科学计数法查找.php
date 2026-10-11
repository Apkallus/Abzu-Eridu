<?php

# 输入字符集字符串，使用随机数组作为字符串索引，返回随机字符串
function get_random_string(
    int $length = 0, 
    string $charset = CHARSET
    ): string {

    # 进行 length 轮循环
    $random_string = '';
    # 最大索引为长度 -1
    $charset_max_index = strlen($charset) - 1;
    for ($i = 0; $i < $length; $i++) {
        # 使用 random_int 获得随机索引，拼接字符串
        $random_string .= $charset[random_int(0, $charset_max_index)];
    }
    return $random_string;
}

# 寻找 hash 为有效科学计数法的字符串，若提供前后缀则搜索拼接后的字符串
function get_hash_0e(
    string $hash_method = "fnv164",
    string $head = "", 
    string $tail = "", 
    int $length = 6, 
    string $charset = CHARSET
    ) {

    // 正则表达式模式，使用 `0e` 开头、并且剩余均为数字
    $regex = '#^0e[\d]+$#';
    while (1) {
        $random_string = get_random_string($length, $charset);
        $test_str = $head . $random_string . $tail;
        $test_hash = hash($hash_method, $test_str);
        // 得到有效科学计数法字符串后返回
        if (preg_match($regex, $test_hash)){
            break;
        };
    }

    echo "cur test: \n\ttest_str: {$test_str} \n\ttest_hash: {$test_hash} \n";
    return [$test_hash, $test_str];
}

# 将字符集使用 define 定义为全局变量
## 普通格式：使用普通字母数字字符集，或使用所有可见字符
## 编码格式：扩展为所有编码字符（输出时以编码格式）
// define("CHARSET", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789");
define("CHARSET", implode('', range(chr(32), chr(126))));

# 测试
$random_string = get_random_string(10);
echo "test random_string: {$random_string} \n";

# php 的其中一种多函数返回值方式为列表型 `[a, b]`
## 传递命名参数时使用 `name: value`
$host_name = "adeb8ee52f49";
$salt_len = 6;
$password_len = strlen($host_name) + $salt_len;

[$test_hash_a, $test_str_a] = get_hash_0e(
    hash_method: "fnv164", head: $host_name, length: $salt_len
    );

[$test_hash_b, $test_str_b] = get_hash_0e(length: $password_len);

echo ($test_hash_a == $test_hash_b ? "eq" : "not eq") . "\n"

# 改进
## 使用随机字符串长度：例如长度a运行1000次后转为长度b
## 扩展字符集：使用 URL 编码的不可打印字符

# 各种 hash 的示例
## https://github.com/spaze/hashes/tree/master
?>