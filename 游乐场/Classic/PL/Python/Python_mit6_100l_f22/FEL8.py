def same_chars(s1, s2):
    """
    s1 and s2 are strings
    Returns boolean True is a character in s1 is also in s2, and vice 
    versa. If a character only exists in one of s1 or s2, returns False.
    s1 和 s2 是字符串
    如果 s1 中的某个字符也存在于 s2 中，或者反之，则返回布尔值 True。
    如果某个字符仅存在于 s1 或 s2 中的一个，则返回 False。
    """
    # Your code here
    for ch in s1:
        if ch not in s2:
            return False
    for ch in s2:
        if ch not in s1:
            return False
    return True
# Examples:
print(same_chars("abc", "cab"))     # prints True
print(same_chars("abccc", "caaab")) # prints True
print(same_chars("abcd", "cabaa"))  # prints False
print(same_chars("abcabc", "cabz")) # prints False