from parsivar import Normalizer
from parsivar import Tokenizer
from confs.consts import get_bigram_lm
from confs.consts import get_onegram_lm
from confs.consts import get_alphabet
from confs.consts import get_homonym_chars
from confs.consts import get_persian_dictionary
from confs.consts import PERSIAN_DICT_PATH
from confs.consts import SPELL
from confs.consts import MERGE
from confs.consts import SPLIT
from confs.consts import NOTHING
from confs.consts import DELETION
from confs.consts import INSERTION
from confs.consts import SUBSTITUTION
from confs.consts import TRANSPOSITION
import math

NORMALIZER = Normalizer()
TOKENIZER = Tokenizer()
BIGRAM_LM = get_bigram_lm()
ONEGRAM_LM = get_onegram_lm()
HOMONYM_CHARS = get_homonym_chars()
ALPHABET = get_alphabet()
PERSIAN_DICT = get_persian_dictionary(PERSIAN_DICT_PATH)


# Basic Operations
class BasicOperations:
    def __init__(self, words, index):
        self.words = words
        self.index = index

    def deletion(self, word):
        temp_list = []
        for i in range(len(word)):
            if word[i] == '-' or word[i] == '#':  # we do not want to remove merge and split char
                continue
            first = word[:i]
            second = word[i + 1:]
            tmp_string = first + second
            temp_list.append(tmp_string)
        return temp_list

    def insertion(self, word):
        temp_list = []
        for i in range(len(word) + 1):
            for char in ALPHABET:
                first = word[:i]
                second = word[i:]
                tmp_string = first + char + second
                temp_list.append(tmp_string)
        return temp_list

    def substitution(self, word):
        temp_list = []
        for i, char in enumerate(word):
            # we do not want to substitute merge and split signs
            if char == '-' or char == '#':
                continue
            for c in ALPHABET:
                first = word[:i]
                second = word[i + 1:]
                tmp_string = first + c + second  # replacing
                temp_list.append(tmp_string)
        return temp_list

    def transposition(self, word):
        temp_list = []
        word = list(word)
        word_array = word[:]
        for i in range(len(word)):
            j = i + 1
            if j == len(word):
                break
            temp = word_array[i]
            word_array[i] = word_array[j]
            word_array[j] = temp
            temp_string = "".join(word_array)
            temp_list.append(temp_string)
            word_array = word[:]
        return temp_list

    def splitting(self, word):
        temp_list = set([])  # avoiding duplicate words
        sep = '-'  # indicate that this word is split
        for i, char in enumerate(word):
            first = word[:i].strip('\u200c')
            second = word[i:].strip('\u200c')
            tmp_string = first + sep + second
            temp_list.add(tmp_string)
        return list(temp_list)

    def generate_words_with_basic_ops(self, words, index, wi, operation):
        new_sim_words = []
        ops = []
        if operation == SPELL:
            temp = self.deletion(wi)
            for i in temp:
                new_sim_words.append(i)
                ops.append(DELETION)
            temp = self.insertion(wi)
            for i in temp:
                new_sim_words.append(i)
                ops.append(INSERTION)
            temp = self.substitution(wi)
            for i in temp:
                new_sim_words.append(i)
                ops.append(SUBSTITUTION)
            temp = self.transposition(wi)
            for i in temp:
                new_sim_words.append(i)
                ops.append(TRANSPOSITION)

        elif operation == SPLIT:
            temp = self.splitting(wi)
            for i in temp:
                new_sim_words.append(i)
                ops.append(SPLIT)

        elif operation == MERGE:
            if index < len(words) - 1:
                temp = wi + '#' + words[index + 1]
                new_sim_words.append(temp)
                ops.append(MERGE)

        return new_sim_words, ops



class WordsEvaluation:
    def __init__(self, words, index):
        self.basic_ops = BasicOperations(words, index)

    # Evaluation Utils:
    def bigram_probability(self, w1, w2):
        bigram_counts, total_count = BIGRAM_LM
        tmp = (w1, w2)
        if tmp in bigram_counts.keys():
            x = bigram_counts[tmp]
            x = float(x) / total_count
            x = math.log2(x)
            return x
        else:
            return -28

    def onegram_probability(self, word):
        p_dict = ONEGRAM_LM[0]
        total_words = ONEGRAM_LM[1]

        if word in p_dict:
            count = p_dict[word]
            logprob = math.log2(float(count) / total_words)
            return logprob
        else:
            return -50.0

    def isword(self, word):
        if abs(word.find('#') - word.find('-')) == 1:
            return False
        # checking divided word
        dash_idx = word.find('-')
        if dash_idx != -1:
            first_part = word[:dash_idx]
            second_part = word[dash_idx + 1:]
            if self.onegram_probability(first_part) < -49:
                return False
            elif self.onegram_probability(second_part) < -49:
                return False
            else:
                return True
        # checking merged word
        sharp_idx = word.find('#')
        if sharp_idx != -1:
            first = word[:sharp_idx]
            second = word[sharp_idx + 1:]
            # Merge:
            temp_str = first + second
            if self.onegram_probability(temp_str) < -49:
                return False
            else:
                return True
        # checking other words
        else:
            if self.onegram_probability(word) < -49:
                return False
            else:
                return True

    def is_homonym(self, current_word, candidate_word):
        current_word = list(current_word)
        candidate_word = list(candidate_word)
        is_homonym = False
        for i, c in enumerate(current_word):
            if c == candidate_word[i]:
                continue
            else:
                is_homonym = False
                for l in HOMONYM_CHARS:
                    if c in l and candidate_word[i] in l:
                        is_homonym = True
                        break
                break
        return is_homonym
