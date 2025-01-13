from parsivar import Normalizer
from parsivar import Tokenizer
from confs.consts import get_bigram_lm
from confs.consts import get_onegram_lm
from confs.consts import get_alphabet
from confs.consts import get_homonym_chars
from confs.consts import get_persian_dictionary
from confs.consts import PERSIAN_DICT_PATH
import math

NORMALIZER = Normalizer()
TOKENIZER = Tokenizer()
BIGRAM_LM = get_bigram_lm()
ONEGRAM_LM = get_onegram_lm()
HOMONYM_CHARS = get_homonym_chars()
ALPHABET = get_alphabet()
PERSIAN_DICT = get_persian_dictionary(PERSIAN_DICT_PATH)


# Basic Operations
def deletion(word):
    temp_list = []
    p_dic = ONEGRAM_LM[0]
    for i in range(len(word)):
        if word[i] == '-' or word[i] == '#':  # we do not want to remove merge and split char
            continue
        begin = word[:i]
        end = word[i + 1:]
        tmp_string = begin + end
        if tmp_string in p_dic:
            temp_list.append(tmp_string)
    return temp_list


def insertion(word):
    temp_list = []
    p_dic = ONEGRAM_LM[0]
    for i in range(len(word) + 1):
        for char in ALPHABET:
            begin = word[:i]
            end = word[i:]
            tmp_string = begin + char + end
            if tmp_string in p_dic:
                temp_list.append(tmp_string)
    return temp_list


def substitution(word):
    temp_list = []
    for i, char in enumerate(word):
        if char == '-' or char == '#':
            continue
        for c in ALPHABET:
            begin = word[:i]
            end = word[i + 1:]
            tmp_string = begin + c + end  # replacing
            temp_list.append(tmp_string)
    return temp_list


def transposition(word):
    temp_list = []
    word = list(word)
    word_array = word[:]
    p_dic = ONEGRAM_LM[0]
    for i in range(len(word)):
        j = i + 1
        if j == len(word):
            break
        temp = word_array[i]
        word_array[i] = word_array[j]
        word_array[j] = temp
        temp_string = "".join(word_array)
        if temp_string in p_dic:
            temp_list.append(temp_string)
        word_array = word[:]
    return temp_list


def splitting(word):
    temp_list = set([])  # avoiding duplicate words
    sep = '-'  # indicate that this word is split
    for i, char in enumerate(word):
        begin = word[:i].strip('\u200c')
        end = word[i:].strip('\u200c')
        tmp_string = begin + sep + end
        temp_list.add(tmp_string)
    return list(temp_list)
