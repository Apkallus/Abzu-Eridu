# Problem Set 4C
# Name:
# Collaborators:

import json
import ps4b # Importing your work from Part B

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    文件名（字符串）：包含待加载单词列表的文件名称

    返回值：一个由有效单词组成的列表。单词均为小写字母组成的字符串。

    根据单词列表的大小，此函数可能需要一些时间才能完成。
    '''
    # inFile: file
    with open(file_name, 'r') as inFile:
        # wordlist: list of strings
        wordlist = []
        for line in inFile:
            wordlist.extend([word.lower() for word in line.split(' ')])
        return wordlist


def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    判断单词是否为有效单词，忽略大小写和标点符号

    word_list（列表）：字典中的单词列表。
    word（字符串）：一个可能的单词。

    返回值：如果单词在word_list中，返回True；否则返回False

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"").lower()
    return word in word_list


def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story[:-1]

# json.load() 将文件对象中的 JSON 数据解析为 Python 对象（通常是字典或列表）
def get_story_pads():
    with open('pads.txt') as json_file:
        return json.load(json_file)


WORDLIST_FILENAME = 'words.txt'
### END HELPER CODE ###


def decrypt_message_try_pads(ciphertext, pads):
    '''
    Given a string ciphertext and a list of possible pads
    used to create it find the pad used to create the ciphertext

    We will consider the pad used to create it the pad which
    when used to decrypt ciphertext results in a plaintext
    with the most valid English words. In the event of ties return
    the last pad that results in the maximum number of valid English words.

    ciphertext (EncryptedMessage): The ciphertext
    pads (list of lists of ints): A list of pads which might have been used
        to encrypt the ciphertext

    Returns: (PlaintextMessage) A message with the decrypted ciphertext and the best pad

    给定一个密文字符串和一组可能用于生成该密文的填充列表，找出用于生成该密文的填充。

    我们将认为用于生成密文的填充是：当使用该填充解密密文时，能够产生包含最多有效英文单词的明文。
    如果出现平局，则返回最后一个能够产生最大数量有效英文单词的填充。

    **参数**:
    - ciphertext (EncryptedMessage): 密文
    - pads (list of lists of ints): 可能用于加密密文的填充列表

    **返回**: (PlaintextMessage) 包含解密后的密文和最佳填充的消息
    '''
    # 使用密码本解密后，统计有效单词
    # 加载word列表

    wordlist = load_words(WORDLIST_FILENAME)
    
    # 对加密信息EncryptedMessage，使用其中一个pad进行解密，得到解密后的文本对象PlaintextMessage
    max_words_pt = ciphertext.decrypt_message(pads[0])
    cur_wordlist = [is_word(wordlist ,word) for word in max_words_pt.get_text().split(' ')]
    max_wordnum = cur_wordlist.count(True)

    for loop_pad in pads[1:]:
        cur_words_pt = ciphertext.decrypt_message(loop_pad)
        cur_wordlist = [is_word(wordlist, word) for word in cur_words_pt.get_text().split(' ')]
        cur_wordnum = cur_wordlist.count(True)

        if cur_wordnum >= max_wordnum:
            max_words_pt = cur_words_pt
            max_wordnum = cur_wordlist.count(True)
    
    return max_words_pt
        


def decode_story():
    '''
    Write your code here to decode Bob's story using a list of possible pads
    Hint: use the helper functions get_story_string and get_story_pads and your EncryptedMessage class.

    Returns: (string) the decoded story
    
    在此处编写代码，使用可能的密钥列表来解码鲍勃的故事
    提示：使用辅助函数 get_story_string 和 get_story_pads 以及你的 EncryptedMessage 类。

    返回：(字符串) 解码后的故事
    '''
    # 加载story到加密对象
    ecm_obj = ps4b.EncryptedMessage(get_story_string())
    story_pads = get_story_pads()
    return decrypt_message_try_pads(ecm_obj, story_pads).get_text()



if __name__ == '__main__':
    # # Uncomment these lines to try running decode_story()
    story = decode_story()
    print("Decoded story: ", story)
    pass