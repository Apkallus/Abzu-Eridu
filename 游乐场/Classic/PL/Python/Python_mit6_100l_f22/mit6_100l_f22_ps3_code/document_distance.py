# 6.100A Fall 2022
# Problem Set 3
# Written by: sylvant, muneezap, charz, anabell, nhung, wang19k, asinelni, shahul, jcsands

# Problem Set 3
# Name:
# Collaborators:

# Purpose: Check for similarity between two texts by comparing different kinds of word statistics.
# 目的：通过比较不同种类的词汇统计特征来检测两段文本之间的相似度。

import string
import math

# python -u test_ps3_student.py
# python -u document_distance.py

# string.punctuation 标点符号的字符串
# 遍历小集合再从大集合中删除所有匹配项似乎更高效
### DO NOT MODIFY THIS FUNCTION
def load_file(filename):
    """
    Args:
        filename: string, name of file to read
    Returns:
        string, contains file contents
    """
    # print("Loading file %s" % filename)
    inFile = open(filename, 'r')
    line = inFile.read().strip()
    for char in string.punctuation:
        line = line.replace(char, "")
    inFile.close()
    return line.lower()


### Problem 0: Prep Data ###
def text_to_list(input_text):
    """
    Args:
        input_text: string representation of text from file.
                    assume the string is made of lowercase characters
    Returns:
        list representation of input_text, where each word is a different element in the list
    参数:
        input_text: 文件中文本的字符串表示。
                    假设该字符串由小写字符组成
    返回:
        input_text 的列表表示，其中每个单词都是列表中的一个不同元素
    """
    # 使用无参数的split，以空格与换行等空白符号从字符串中分离单词
    return input_text.split()


### Problem 1: Get Frequency ###
def get_frequencies(input_iterable):
    """
    Args:
        input_iterable: a string or a list of strings, all are made of lowercase characters
    Returns:
        dictionary that maps string:int where each string
        is a letter or word in input_iterable and the corresponding int
        is the frequency of the letter or word in input_iterable
    Note: 
        You can assume that the only kinds of white space in the text documents we provide will be new lines or space(s) between words (i.e. there are no tabs)
    参数：
        input_iterable: 一个字符串或字符串列表，均由小写字符组成
    返回：
        一个字典，映射形式为字符串:整数，其中每个字符串是input_iterable中的字母或单词，对应的整数是该字母或单词在input_iterable中出现的频率
    注意：
        您可以假设我们提供的文本文档中唯一的空白字符是换行符或单词之间的空格（即没有制表符）
        """
    # 空字典与字典的key视图
    res_dict = {}

    # # 遍历序列，字典的key视图来将元素添加或更新到字典
    # # 直接遍历字典时，遍历的是key
    # for e in input_iterable:
    #     if e in res_dict:
    #         res_dict[e] += 1
    #     else:# 初始为1
    #         res_dict[e] = 1

    # 使用get函数, 若存在则返回value，不存在则返回设置的默认值
    # 设置默认值为0,在+1后正好是1
    for e in input_iterable:
        res_dict[e] = res_dict.get(e, 0) + 1

    return res_dict


### Problem 2: Letter Frequencies ###
def get_letter_frequencies(word):
    """
    Args:
        word: word as a string
    Returns:
        dictionary that maps string:int where each string
        is a letter in word and the corresponding int
        is the frequency of the letter in word
    """
    # 直接调用get_frequencies
    return  get_frequencies(word)


### Problem 3: Similarity ###
def calculate_similarity_score(freq_dict1, freq_dict2):
    """
    The keys of dict1 and dict2 are all lowercase,
    you will NOT need to worry about case sensitivity.

    Args:
        freq_dict1: frequency dictionary of letters of word1 or words of text1
        freq_dict2: frequency dictionary of letters of word2 or words of text2
    Returns:
        float, a number between 0 and 1, inclusive
        representing how similar the words/texts are to each other

        The difference in words/text frequencies = DIFF sums words
        from these three scenarios:
        * If an element occurs in dict1 and dict2 then
          get the difference in frequencies
        * If an element occurs only in dict1 then take the
          frequency from dict1
        * If an element occurs only in dict2 then take the
          frequency from dict2
         The total frequencies = ALL is calculated by summing
         all frequencies in both dict1 and dict2.
        Return 1-(DIFF/ALL) rounded to 2 decimal places

        dict1 和 dict2 的键均为小写字母，
    因此您无需担心大小写敏感性问题。

    参数:
        freq_dict1: 单词1或文本1中字母或单词的频率字典
        freq_dict2: 单词2或文本2中字母或单词的频率字典
    返回:
        float, 一个介于0和1之间（包括0和1）的数字，
        表示单词/文本之间的相似程度

        单词/文本频率的差异 = DIFF，通过以下三种情况求和：
        * 如果某个元素同时出现在dict1和dict2中，
          则计算其频率的差值
        * 如果某个元素仅出现在dict1中，
          则取dict1中的频率
        * 如果某个元素仅出现在dict2中，
          则取dict2中的频率
        总频率 = ALL，通过将dict1和dict2中的所有频率相加计算得出。
        返回 1-(DIFF/ALL)，结果四舍五入至小数点后两位
    """
    #  1 - |a - b| / (a + b) 衡量差异占比

    # 创建合并字典得到独特key集合,使用此序列遍历，在两个字典中查找
    key_set = freq_dict1 | freq_dict2
    add, diff_abs = 0, 0
    for k in key_set:
        # 得到独特单词的频率，若未出现则设置为0
        dict1_value = freq_dict1.get(k, 0)
        dict2_value = freq_dict2.get(k, 0)
        # 计算并累积差的绝对值与和
        diff_abs += abs(dict1_value - dict2_value)
        add += dict1_value + dict2_value
    
    # 最终计算以及舍入
    res = 1 - diff_abs/add
    res = round(res, 2)
    return res

### Problem 4: Most Frequent Word(s) ###
def get_most_frequent_words(freq_dict1, freq_dict2):
    """
    The keys of dict1 and dict2 are all lowercase,
    you will NOT need to worry about case sensitivity.

    Args:
        freq_dict1: frequency dictionary for one text
        freq_dict2: frequency dictionary for another text
    Returns:
        list of the most frequent word(s) in the input dictionaries

    The most frequent word:
        * is based on the combined word frequencies across both dictionaries.
          If a word occurs in both dictionaries, consider the sum the
          freqencies as the combined word frequency.
        * need not be in both dictionaries, i.e it can be exclusively in
          dict1, dict2, or shared by dict1 and dict2.
    If multiple words are tied (i.e. share the same highest frequency),
    return an alphabetically ordered list of all these words.
    字典 `dict1` 和 `dict2` 的键均为小写字母，因此您无需担心大小写敏感性问题。

    **参数：**  
    - `freq_dict1`: 一个文本的频率字典  
    - `freq_dict2`: 另一个文本的频率字典  

    **返回值：**  
    输入字典中出现频率最高的单词列表  

    **最频繁单词的定义：**  
    - 基于两个字典中单词频率的总和。如果一个单词同时出现在两个字典中，则将其频率相加作为该单词的总频率。  
    - 该单词不必同时出现在两个字典中，即它可以仅存在于 `dict1`、`dict2` 或同时存在于两者中。  

    如果多个单词的频率相同（即共享相同的最高频率），则返回这些单词按字母顺序排列的列表。
    """
    # 创建合并字典得到独特key集合,使用此序列遍历，在两个字典中查找
    key_set = freq_dict1 | freq_dict2

    # 遍历key_set的key并使用两个字典更新value
    for k in key_set:
        key_set[k] = freq_dict1.get(k, 0) + freq_dict2.get(k, 0)
    
    # 使用item得到字典的k，v对元组，并转为列表
    # 此处可找到最大value值，并将此作为列表推导条件，只保存最大值对应的key
    res = list(key_set.items())
    # 按照元组的顺序 频率降序，字母升序
    res.sort(key = lambda x: (-x[1], x[0]))
    # 得到最大次数，并提取元组中的key
    max_num = res[0][1]
    res = [e[0] for e in res if e[1] == max_num]
    return res

### Problem 5: Finding TF-IDF ###
def get_tf(file_path):
    """
    Args:
        file_path: name of file in the form of a string
    Returns:
        a dictionary mapping each word to its TF

    * TF is calculatd as TF(i) = (number times word *i* appears
        in the document) / (total number of words in the document)
    * Think about how we can use get_frequencies from earlier
    参数:
        file_path: 文件名称，以字符串形式给出
    返回:
        一个字典，将每个单词映射到其词频（TF）

    * 词频（TF）的计算公式为：TF(i) = (单词 *i* 在文档中出现的次数) / (文档中的总单词数)
    * 思考如何利用之前定义的 get_frequencies 函数来实现此功能
    """
    # load_file() text_to_list() get_frequencies()
    # 使用之前的函数得到文件字符串，单词字符串列表，频率
    file_str = load_file(file_path)
    words_str = text_to_list(file_str)
    words_freq_dict = get_frequencies(words_str)

    # 使用单词频率/总单词数 得到新字典或更新words_freq_dict字典
    total_words = len(words_str)
    res_dict = {k:v/total_words for k,v in words_freq_dict.items()}
    return res_dict

def get_idf(file_paths):
    """
    Args:
        file_paths: list of names of files, where each file name is a string
    Returns:
       a dictionary mapping each word to its IDF

    * IDF is calculated as IDF(i) = log_10(total number of documents / number of
    documents with word *i* in it), where log_10 is log base 10 and can be called
    with math.log10()
    参数:
        file_paths: 文件名列表，其中每个文件名均为字符串
    返回:
       一个字典，将每个单词映射到其IDF值

    * IDF的计算公式为：IDF(i) = log_10(文档总数 / 包含单词 *i* 的文档数)，
    其中log_10表示以10为底的对数，可通过math.log10()调用。

    """
    all_file_words_dict = {}

    # 遍历所有文档，创建单词与包含单词的文档数量字典
    for file_path in file_paths: 
        file_str = load_file(file_path)
        words_str = text_to_list(file_str)
        words_freq_dict = get_frequencies(words_str)
        for k in words_freq_dict:
            all_file_words_dict[k] = all_file_words_dict.get(k, 0) + 1

    # 使用文档总数/包含单词的文档数量 得到新字典
    file_num = len(file_paths)
    res_dict = {k:math.log10(file_num / v) for k,v in all_file_words_dict.items()}
    return res_dict

def get_tfidf(tf_file_path, idf_file_paths):
    """
        Args:
            tf_file_path: name of file in the form of a string (used to calculate TF)
            idf_file_paths: list of names of files, where each file name is a string
            (used to calculate IDF)
        Returns:
           a sorted list of tuples (in increasing TF-IDF score), where each tuple is
           of the form (word, TF-IDF). In case of words with the same TF-IDF, the
           words should be sorted in increasing alphabetical order.

        * TF-IDF(i) = TF(i) * IDF(i)
        参数：
            tf_file_path: 文件名称，以字符串形式表示（用于计算词频TF）
            idf_file_paths: 文件名称列表，其中每个文件名称均为字符串
            （用于计算逆文档频率IDF）
        返回：
           一个按TF-IDF分数递增排序的元组列表，其中每个元组的形式为
           (单词, TF-IDF)。若单词的TF-IDF分数相同，则按字母顺序递增排序。

        * TF-IDF(i) = TF(i) * IDF(i)
        """
    # 计算单词点数
    tf_dict = get_tf(tf_file_path)
    idf_dict = get_idf(idf_file_paths)
    res_dict = {k:v*idf_dict.get(k, 0) for k,v in tf_dict.items()}
    # 字典转列表元组
    res_dict = list(res_dict.items())
    # 排序
    res_dict.sort(key=lambda x:(x[1], x[0]))
    return res_dict

if __name__ == "__main__":
    pass
    ###############################################################
    ## Uncomment the following lines to test your implementation ##
    ###############################################################

    # python -u test_ps3_student.py
    # python -u document_distance.py

    # Tests Problem 0: Prep Data
    # test_directory = "tests/student_tests/"
    # hello_world, hello_friend = load_file(test_directory + 'hello_world.txt'), load_file(test_directory + 'hello_friends.txt')
    # world, friend = text_to_list(hello_world), text_to_list(hello_friend)
    # print(world)      # should print ['hello', 'world', 'hello']
    # print(friend)     # should print ['hello', 'friends']

    # Tests Problem 1: Get Frequencies
    # test_directory = "tests/student_tests/"
    # hello_world, hello_friend = load_file(test_directory + 'hello_world.txt'), load_file(test_directory + 'hello_friends.txt')
    # world, friend = text_to_list(hello_world), text_to_list(hello_friend)
    # world_word_freq = get_frequencies(world)
    # friend_word_freq = get_frequencies(friend)
    # print(world_word_freq)    # should print {'hello': 2, 'world': 1}
    # print(friend_word_freq)   # should print {'hello': 1, 'friends': 1}

    # # Tests Problem 2: Get Letter Frequencies
    # freq1 = get_letter_frequencies('hello')
    # freq2 = get_letter_frequencies('that')
    # print(freq1)      #  should print {'h': 1, 'e': 1, 'l': 2, 'o': 1}
    # print(freq2)      #  should print {'t': 2, 'h': 1, 'a': 1}

    # # Tests Problem 3: Similarity
    # test_directory = "tests/student_tests/"
    # hello_world, hello_friend = load_file(test_directory + 'hello_world.txt'), load_file(test_directory + 'hello_friends.txt')
    # world, friend = text_to_list(hello_world), text_to_list(hello_friend)
    # world_word_freq = get_frequencies(world)
    # friend_word_freq = get_frequencies(friend)
    # word1_freq = get_letter_frequencies('toes')
    # word2_freq = get_letter_frequencies('that')
    # word3_freq = get_frequencies('nah')
    # word_similarity1 = calculate_similarity_score(word1_freq, word1_freq)
    # word_similarity2 = calculate_similarity_score(word1_freq, word2_freq)
    # word_similarity3 = calculate_similarity_score(word1_freq, word3_freq)
    # word_similarity4 = calculate_similarity_score(world_word_freq, friend_word_freq)
    # print(word_similarity1)       # should print 1.0
    # print(word_similarity2)       # should print 0.25u
    # print(word_similarity3)       # should print 0.0
    # print(word_similarity4)       # should print 0.4

    # # Tests Problem 4: Most Frequent Word(s)
    # freq_dict1, freq_dict2 = {"hello": 5, "world": 1}, {"hello": 1, "world": 5}
    # most_frequent = get_most_frequent_words(freq_dict1, freq_dict2)
    # print(most_frequent)      # should print ["hello", "world"]

    # Tests Problem 5: Find TF-IDF
    tf_text_file = 'tests/student_tests/hello_world.txt'
    idf_text_files = ['tests/student_tests/hello_world.txt', 'tests/student_tests/hello_friends.txt']
    tf = get_tf(tf_text_file)
    idf = get_idf(idf_text_files)
    tf_idf = get_tfidf(tf_text_file, idf_text_files)
    print(tf)     # should print {'hello': 0.6666666666666666, 'world': 0.3333333333333333}
    print(idf)    # should print {'hello': 0.0, 'world': 0.3010299956639812, 'friends': 0.3010299956639812}
    print(tf_idf) # should print [('hello', 0.0), ('world', 0.10034333188799373)]