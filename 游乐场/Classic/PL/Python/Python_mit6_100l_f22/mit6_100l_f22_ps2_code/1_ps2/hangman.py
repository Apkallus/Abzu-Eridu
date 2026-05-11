# Problem Set 2, hangman.py
# Name:
# Collaborators:
# Time spent:

import random
import string

# -----------------------------------
# HELPER CODE
# -----------------------------------

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    returns: list, a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print(" ", len(wordlist), "words loaded.")
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    returns: a word from wordlist at random
    """
    return random.choice(wordlist)

# -----------------------------------
# END OF HELPER CODE
# -----------------------------------


# Load the list of words to be accessed from anywhere in the program
wordlist = load_words()

def has_player_won(secret_word, letters_guessed):
    """
    secret_word: string, the lowercase word the user is guessing
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: boolean, True if all the letters of secret_word are in letters_guessed,
        False otherwise
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    # 检查 secret_word 的所有字符是否存在于 letters_guessed 中
    for ch in secret_word:
        if ch not in letters_guessed:
            return False
    return True


def get_word_progress(secret_word, letters_guessed):
    """
    secret_word: string, the lowercase word the user is guessing
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: string, comprised of letters and asterisks (*) that represents
        which letters in secret_word have not been guessed so far
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    # 返回值: 字符串，由字母和星号（*）组成，表示secret_word中哪些字母尚未被猜到
    res_str = ''
    for ch in secret_word:
        if ch not in letters_guessed:
            res_str += '*'
        else:
            res_str += ch
    return res_str  

def get_available_letters(letters_guessed):
    """
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: string, comprised of letters that represents which
      letters have not yet been guessed. The letters should be returned in
      alphabetical order
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    # 返回除letters_guessed的字符外，字母表中剩余的字符
    res_str = ''
    for ch in string.ascii_lowercase:
        if ch not in letters_guessed:
            res_str += ch
    return res_str



def hangman(secret_word, with_help):
    """
    secret_word: string, the secret word to guess.
    with_help: boolean, this enables help functionality if true.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses they start with.

    * The user should start with 10 guesses.

    * Before each round, you should display to the user how many guesses
      they have left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a single letter (or help character '!'
      for with_help functionality)

    * If the user inputs an incorrect consonant, then the user loses ONE guess,
      while if the user inputs an incorrect vowel (a, e, i, o, u),
      then the user loses TWO guesses.

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    -----------------------------------
    with_help functionality
    -----------------------------------
    * If the guess is the symbol !, you should reveal to the user one of the
      letters missing from the word at the cost of 3 guesses. If the user does
      not have 3 guesses remaining, print a warning message. Otherwise, add
      this letter to their guessed word and continue playing normally.

    Follows the other limitations detailed in the problem write-up.
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    dashes_str = '--------------'
    get_str = "Good guess: "
    not_get_str = "Oops! That letter is not in my word: "

    user_won = False
    gs_time = 10
    letters_guessed = ''
    letters_already_currect_guess = 0

    print("Welcome to Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")

    # 耗尽猜测次数前持续循环
    while gs_time > 0:
        # 输出头部
        print_header_str(dashes_str, gs_time, letters_guessed)
        # 得到有效输入字符
        one_letter_guessed = get_guess_letter(secret_word, letters_guessed, dashes_str, gs_time, with_help)
        # 如果为帮助字符
        if with_help and one_letter_guessed == '!':
            # 使用帮助字符，花费3次获得一个秘密字符,剩余次数不足的情况在get_guess_letter中处理
            gs_time -= 3
            letter_revealed = helper(secret_word, letters_guessed)
            # 将揭示字符添加到猜测猜测字符串中
            letters_guessed += letter_revealed
            print(f"Letter revealed: {letter_revealed}")
            print(f"{get_word_progress(secret_word, letters_guessed)}")
        # 如果为猜测字符
        else:
            # 更新猜测字符串
            letters_guessed += one_letter_guessed
            # 查看进度
            progress_str = get_word_progress(secret_word, letters_guessed)
            # 查看猜测后的正确字符数量
            after_guess_currect_letters = how_many_letters(progress_str)

            # 如果本次猜测正确
            if after_guess_currect_letters > letters_already_currect_guess:
                # 更新当前正确字符数量
                letters_already_currect_guess = after_guess_currect_letters
                # 使用猜测正确的显示字符串
                is_get_str = get_str
                
            # 如果猜测错误
            else:
                # 使用猜测错误的显示字符串
                is_get_str = not_get_str
                # 错误时，元音失去2次，辅音失去1次
                if is_vowels(one_letter_guessed):
                    gs_time -= 2
                else:
                    gs_time -= 1
            print(f"{is_get_str}{progress_str}")
        
        # 每次猜测后查看玩家是否获胜
        if has_player_won(secret_word, letters_guessed):
            user_won = True
            break
        
    # 输出结束信息
    print(dashes_str)
    if user_won:
        # 计算玩家点数
        total_score = get_score(gs_time, secret_word)
        print("Congratulations, you won!")
        print(f"Your total score for this game is: {total_score}")
    else:
        print(f"Sorry, you ran out of guesses. The word was {secret_word}.")

# 返回猜测点数
def get_score(gs_time, secret_word):
    number_of_unique_letters = how_many_unique_letters(secret_word)
    total_score = gs_time + 4*number_of_unique_letters + 3*len(secret_word)
    return total_score

def how_many_unique_letters(secret_word):
    exist_str = ''
    for ch in secret_word:
        if ch not in exist_str:
            exist_str += ch
    return len(exist_str)    
# 返回帮助字符所揭示的秘密字符
def helper(secret_word, letters_guessed):
    choose_from = ''

    # 使用剩余的秘密字符构建剩余字符串
    for ch in secret_word:
        if ch not in letters_guessed:
            choose_from += ch

    # 随机从剩余字符串中选择返回字符
    new = random.randint(0, len(choose_from)-1)
    revealed_letter = choose_from[new]
    return revealed_letter

# 查看是否为元音字符
def is_vowels(one_letter_guessed):
    return one_letter_guessed in "aeiou"

# 得到有效猜测字符
def get_guess_letter(secret_word, letters_guessed, dashes_str, gs_time, with_help):
    
    not_vaild_str = 'Oops! That is not a valid letter. Please input a letter from the alphabet: '
    guessed_str = "Oops! You've already guessed that letter: "
    not_enough_times_str = "Oops! Not enough guesses left: "

    # 获得输入并转为小写
    one_letter_guessed = str.lower(input("Please guess a letter: "))
    # 是否多于一个字符
    is_more_then_one = len(one_letter_guessed) != 1
    # 创造有效输入的字符串 字母表与 如果使用help模式时的!字符
    alpha_plus_help = string.ascii_lowercase + ('!' if with_help else '')
    # 是否为有效字符
    is_not_vaild_char = one_letter_guessed not in alpha_plus_help
    # 得到当前的进度字符串，在输入无效时print
    progress_str = get_word_progress(secret_word, letters_guessed)
    # 是否为已经猜过的字母,且不为!
    # 如果缺乏处理，则!将被归到已经猜过，由于之前的有效字符串已经处理!,如果按顺序则此处无需再次判断help模式
    # 翻译： 如果在帮助模式下且本次输入符号为!则为false，否则作为字母检查是否已猜测
    is_guessed = one_letter_guessed in letters_guessed and not (one_letter_guessed == '!' and with_help)
    # 剩余次数是否足够使用帮助字符,如果没有启用帮助模式则为false
    is_not_enough_times = (gs_time < 3) if with_help else False

    # 多于一个字符/非有效字符/已猜过/次数不足 持续循环
    while is_more_then_one or is_not_vaild_char or is_guessed or is_not_enough_times:
        # 多于一个字符/非有效字符 对应无效字符串
        if is_more_then_one or is_not_vaild_char:
            appear_str = not_vaild_str
        # 启用帮助模式且输入为!，但次数不足
        elif with_help and one_letter_guessed == '!' and is_not_enough_times:
            appear_str = not_enough_times_str
        # 已猜过 对应已猜过字符串
        else:
            appear_str = guessed_str
            
        # 输出对应字符串与当前进度
        print(f"{appear_str}{progress_str}")

        # 输出头部，以及获得下一轮输入
        print_header_str(dashes_str, gs_time, letters_guessed)
        one_letter_guessed = str.lower(input("Please guess a letter: "))
        is_more_then_one = len(one_letter_guessed) != 1
        is_not_vaild_char = one_letter_guessed not in alpha_plus_help
        progress_str = get_word_progress(secret_word, letters_guessed)
        is_guessed = one_letter_guessed in letters_guessed and not (one_letter_guessed == '!' and with_help)
        is_not_enough_times = (gs_time < 3) if with_help else False

    # 如果字符有效则返回
    return one_letter_guessed

def print_header_str(dashes_str, gs_time, letters_guessed):
    print(dashes_str)
    print(f"You have {gs_time} guesses left.")
    print(f"Available letters: {get_available_letters(letters_guessed)}")  

def how_many_letters(progress_str):
    count = 0
    for ch in progress_str:
        if ch in string.ascii_lowercase:
            count += 1
    return count
# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the lines to test

if __name__ == "__main__":
    # To test your game, uncomment the following three lines.

    # secret_word = choose_word(wordlist)
    secret_word = 'tact'
    with_help = True
    hangman(secret_word, with_help)

    # After you complete with_help functionality, change with_help to True
    # and try entering "!" as a guess!

    ###############

    # SUBMISSION INSTRUCTIONS
    # -----------------------
    # It doesn't matter if the lines above are commented in or not
    # when you submit your pset. However, please run ps2_student_tester.py
    # one more time before submitting to make sure all the tests pass.
    pass

