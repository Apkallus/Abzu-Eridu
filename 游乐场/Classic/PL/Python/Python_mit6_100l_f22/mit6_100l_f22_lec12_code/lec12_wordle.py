######## WORDLE ###########
######## ASSUME YOU ARE GIVEN CODE FROM HERE.... ############
import random

words = """abroad
accept
access
across
acting
action
active
actual
advice
advise
affect
afford
afraid
agency
agenda
almost
always
amount
animal
annual
answer
anyone
anyway
appeal
appear
around
arrive
artist
aspect
assess
assist
assume
attack
attend
august
author
avenue
backed
barely
battle
beauty
became
become
before
behalf
behind
belief
belong
berlin
better
beyond
bishop
border
bottle
bottom
bought
branch
breath
bridge
bright
broken
budget
burden
bureau
button
camera
cancer
cannot
carbon
career
castle
casual
caught
center
centre
chance
change
charge
choice
choose
chosen
church
circle
client
closed
closer
coffee
column
combat
coming
common
comply
copper
corner
costly
county
couple
course
covers
create
credit
crisis
custom
damage
danger
dealer
debate
decade
decide
defeat
defend
define
degree
demand
depend
deputy
desert
design
desire
detail
detect
device
differ
dinner
direct
doctor
dollar
domain
double
driven
driver
during
easily
eating
editor
effect
effort
eighth
either
eleven
emerge
empire
employ
enable
ending
energy
engage
engine
enough
ensure
entire
entity
equity
escape
estate
ethnic
exceed
except
excess
expand
expect
expert
export
extend
extent
fabric
facing
factor
failed
fairly
fallen
family
famous
father
fellow
female
figure
filing
finger
finish
fiscal
flight
flying
follow
forced
forest
forget
formal
format
former
foster
fought
fourth
French
friend
future
garden
gather
gender
german
global
golden
ground
growth
guilty
handed
handle
happen
hardly
headed
health
height
hidden
holder
honest
impact
import
income
indeed
injury
inside
intend
intent
invest
island
itself
jersey
joseph
junior
killed
labour
latest
latter
launch
lawyer
leader
league
leaves
legacy
length
lesson
letter
lights
likely
linked
liquid
listen
little
living
losing
lucent
luxury
mainly
making
manage
manner
manual
margin
marine
marked
market
martin
master
matter
mature
medium
member
memory
mental
merely
merger
method
middle
miller
mining
minute
mirror
mobile
modern
modest
module
moment
morris
mostly
mother
motion
moving
murder
museum
mutual
myself
narrow
nation
native
nature
nearby
nearly
nights
nobody
normal
notice
notion
number
object
obtain
office
offset
online
option
orange
origin
output
oxford
packed
palace
parent
partly
patent
people
period
permit
person
phrase
picked
planet
player
please
plenty
pocket
police
policy
prefer
pretty
prince
prison
profit
proper
proven
public
pursue
raised
random
rarely
rather
rating
reader
really
reason
recall
recent
record
reduce
reform
regard
regime
region
relate
relief
remain
remote
remove
repair
repeat
replay
report
rescue
resort
result
retail
retain
return
reveal
review
reward
riding
rising
robust
ruling
safety
salary
sample
saving
saying
scheme
school
screen
search
season
second
secret
sector
secure
seeing
select
seller
senior
series
server
settle
severe
should
singer
signal
signed
silent
silver
simple
simply
single
sister
slight
smooth
social
solely
sought
sounds
source
soviet
speech
spirit
spoken
spread
spring
square
stable
status
steady
stolen
strain
stream
street
stress
strict
strike
string
strong
struck
studio
submit
sudden
suffer
summer
summit
supply
surely
survey
switch
symbol
system
taking
talent
target
taught
tenant
tender
tennis
thanks
theory
thirty
though
threat
thrown
ticket
timely
timing
tissue
toward
travel
treaty
trying
twelve
twenty
unable
unique
united
unless
unlike
update
useful
valley
varied
vendor
versus
victim
vision
visual
volume
walker
wealth
weekly
weight
wholly
window
winner
winter
within
wonder
worker
wright
writer
yellow"""

random.seed(0)
def new_word(words):
    """ words is a multi-line string.
    Returns a 6 letter word as a str. """
    words_list = get_word_list(words)
    return random.choice(words_list)

######## ....ASSUME YOU ARE GIVEN CODE UP TO HERE ############

################################################
######## THE CODE BELOW IS BUGGY #############
################################################
def get_word_list(words_str):
    """ words_str is a multi-line string.
    Returns a list whose elements are lowercase words 
    words_str 是一个多行字符串。
    返回一个元素为小写单词的列表
    """
    # return words.split('\n') #应当使用参数words_str而不是全局名称words
    print("into get_word_list ",type(words_str))
    return words_str.split('\n')

def is_a_real_word(s, word_list):
    """ s is a string
        word_list is a list of words
    Returns True is s is in word_list and False otherwise 
    s 是一个字符串
        word_list 是一个单词列表
    如果 s 在 word_list 中则返回 True，否则返回 False
    """
    return (s in word_list)

def is_correct_len(guess, length):
    """ guess is a str
        length is an int
    Returns True if guess has length number of characters. 
    guess 是一个字符串
        length 是一个整数
    如果 guess 的字符数为 length，则返回 True。
    """
    return (len(guess) == length)

def make_wordle(guess, secret):
    """ guess and secret are 6 letter words
    Returns a result where:
    * a guess' letter in the correct place is capitalized
    * a guess' letter in the secret but not in the correct place is lowercase
    * a guess' letter not in the secret is not shown 
    For example: if guess is "struck" and the secret is "strike" 
    then the return is "ST   k"
    猜测词和秘密词均为6个字母的单词
    返回结果规则如下：
    * 猜测词中位置正确的字母大写显示
    * 猜测词中存在但位置不正确的字母小写显示
    * 猜测词中不存在的字母不显示
    例如：若猜测词为“struck”，秘密词为“strike”
    则返回结果为“ST   k”
    """
    result = ""
    # guessed = [] # guessed无效果
    # 创建一个除位置正确的字母外的剩余待猜测列表
    secreted = [ secret[i] for i in range(len(secret)) if guess[i] != secret[i] ]
    for i in range(len(secret)):
        if guess[i] == secret[i]:
            result += guess[i].upper()
            # guessed.append(guess[i])
        # elif guess[i] in secret:
        # 如果位置不对应但存在于secret的剩余待猜测字母中
        elif guess[i] in secreted:
            result += guess[i]
            secreted.remove(guess[i])
        else:
            result += ' '
    return result

# python -u lec12_wordle.py

def play_game():
    """ Plays the game.
    0) Generates a word_list, a new secret word, and sets up 6 guesses.
    1) Asks the user for a 6 letter word as a guess
    2) Creates a wordle, i.e. the word that the user guessed, but with the
       following replacements: 
       a) guessed letters in the correct position as secret are capitalized
       b) guessed letters in the secret but not in the correct position are lowercase
       c) all other guessed letters are represented as a space
       For example: if guess is "struck" and the secret is "strike" then the
       user is presented with "ST   k".
    3) The user has 6 guesses to guess the secret word. 
    进行游戏。
    0) 生成一个单词列表，一个新的秘密单词，并设置6次猜测机会。
    1) 要求用户输入一个6字母的单词作为猜测。
    2) 创建一个Wordle，即用户猜测的单词，但进行以下替换：
       a) 猜测的字母在秘密单词中的正确位置时，该字母大写显示。
       b) 猜测的字母存在于秘密单词中但位置不正确时，该字母小写显示。
       c) 所有其他猜测的字母用空格表示。
       例如：如果猜测是“struck”，而秘密单词是“strike”，则用户将看到“ST   k”。
    3) 用户有6次机会来猜出秘密单词。"""
    word_list = get_word_list(words)
    # secret = new_word 应当调用函数
    secret = new_word(words)
    print(secret)
    wordle_len = 6
    n_guesses = 6
    win = False
    
    print(f"You have {n_guesses} to guess a 6-letter word.")
    guess = input("Guess: ")
    
    # while guess != secret: 如果第一次猜测正确则不进入循环而显示you lose
    while n_guesses > 0:
        while True: # 增加while循环，直到输入6个字的单词
            if is_a_real_word(guess, word_list) and is_correct_len(guess, wordle_len):
                # result = make_wordle(guess, secret) # 若符合则重复显示
                # print(result)
                n_guesses -= 1
                break
            else:
                print("Not a word or not the correct length.")
                guess = input("Guess: ")

        result = make_wordle(guess, secret)
        print(result)

        if guess == secret: # 调整猜测正确的与剩余次数的条件判断
            print("into guess == secret")
            win = True
            break

        print(f"You have {n_guesses} guesses left.")
        if n_guesses > 0:
            guess = input("Guess: ")
        else:
            print("n_guesses <= 0")
            break
        # if n_guesses > 0:
        #     guess = input("Guess: ")
        # elif guess == secret:
        #     win = True
        #     break
        # else:
        #     break
    if win:
        print('YOU WIN')
    else:
        print('YOU LOSE')

play_game()





################################################
######## FIXES TO THE BUGGY CODE #############
################################################

def get_word_list(words_str):
    """ words_str is a multi-line string.
    Returns a list whose elements are lowercase words """
    return words.split('\n')

def is_a_real_word(s, word_list):
    """ s is a string
        word_list is a list of words
    Returns True is s is in word_list and False otherwise """
    return (s in word_list)

def is_correct_len(guess, length):
    """ guess is a str
        length is an int
    Returns True if guess has length number of characters. """
    return (len(guess) == length)

def make_wordle(guess, secret):
    """ guess and secret are 6 letter words
    Returns a result where:
    * a guess' letter in the correct place is capitalized
    * a guess' letter in the secret but not in the correct place is lowercase
    * a guess' letter not in the secret is not shown 
    For example: if guess is "struck" and the secret is "strike" 
    then the return is "ST   k"
    """
    result = ""
    guessed = []
    for i in range(len(secret)):
        if guess[i] == secret[i]:
            result += guess[i].upper()
            guessed.append(guess[i])
        # 错误在于，如果guess了两个相同字符，但secret只有一个时,
        # 第一次没有猜中将显示为小写而不是空。
        # 直接创建一个剩余secret列表更简单，否则要进行复杂判断:
        # guess[i]在secret中，且对应secret位置的guess不正确，
        # 如果猜测相同字母两次，存在但位置都不对，那么第二个guess应当为空而不是小写
        # 于是直接创建一个剩余secret列表更简单
        elif guess[i] in secret and guess[i] not in guessed:
            result += guess[i]
        else:
            result += ' '
    return result

def play_game():
    """ Plays the game.
    0) Generates a word_list, a new secret word, and sets up 6 guesses.
    1) Asks the user for a 6 letter word as a guess
    2) Creates a wordle, i.e. the word that the user guessed, but with the
       following replacements: 
       a) guessed letters in the correct position as secret are capitalized
       b) guessed letters in the secret but not in the correct position are lowercase
       c) all other guessed letters are represented as a space
       For example: if guess is "struck" and the secret is "strike" then the
       user is presented with "ST   k".
    3) The user has 6 guesses to guess the secret word. """
    word_list = get_word_list(words)
    secret = new_word(words)
    print(secret)
    wordle_len = 6
    n_guesses = 6
    win = False
    
    print(f"You have {n_guesses} to guess a 6-letter word.")
    guess = input("Guess: ")
    
    while guess != secret:
        # if is_a_real_word(guess, word_list) and is_correct_len(guess, wordle_len):
        #     result = make_wordle(guess, secret)
        #     print(result)
        #     n_guesses -= 1
        # else:
        #     print("Not a word or not the correct length.")
        result = make_wordle(guess, secret)
        print(result)
        n_guesses -= 1
        print(f"You have {n_guesses} guesses left.")
        if n_guesses > 0:
            guess = input("Guess: ")
        elif guess == secret:
            win = True
            break
        else:
            break
    if win or guess==secret:
        print('YOU WIN')
    else:
        print('YOU LOSE')
    
# play_game()




