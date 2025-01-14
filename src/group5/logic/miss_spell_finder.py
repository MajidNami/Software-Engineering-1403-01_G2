from parsivar import Normalizer
from parsivar import Tokenizer
from src.group5.logic.confs.consts import get_bigram_lm
from src.group5.logic.confs.consts import get_onegram_lm
from src.group5.logic.confs.consts import get_alphabet
from src.group5.logic.confs.consts import get_homonym_chars
from src.group5.logic.confs.consts import get_persian_dictionary
from src.group5.logic.confs.consts import PERSIAN_DICT_PATH
from src.group5.logic.confs.consts import SPELL
from src.group5.logic.confs.consts import MERGE
from src.group5.logic.confs.consts import SPLIT
from src.group5.logic.confs.consts import NOTHING
from src.group5.logic.confs.consts import DELETION
from src.group5.logic.confs.consts import INSERTION
from src.group5.logic.confs.consts import SUBSTITUTION
from src.group5.logic.confs.consts import TRANSPOSITION
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

    def filter_possible_words(self, words, index):
        wi = words[index]
        possible_words = []
        possible_ops = []
        possible_words_prob_dict = {}
        possible_ops_dict = {}

        possible_words.append(wi)
        possible_ops.append(NOTHING)

        if len(wi) == 1:
            return possible_words, possible_ops
        built_words, ops = self.basic_ops.generate_words_with_basic_ops(words, index, wi, SPELL)
        for i, word in enumerate(built_words):
            if self.isword(word):
                prob = self.onegram_probability(word)
                if word not in possible_words_prob_dict:
                    possible_words_prob_dict[word] = prob
                    possible_ops_dict[word] = ops[i]

        built_words, ops = self.basic_ops.generate_words_with_basic_ops(words, index, wi, SPLIT)
        for i, word in enumerate(built_words):
            if self.isword(word):
                first = word.split('-')[0]
                second = word.split('-')[1]
                prob = float(self.onegram_probability(first) + self.onegram_probability(second)) / 2
                if word not in possible_words_prob_dict:
                    possible_words_prob_dict[word] = prob
                    possible_ops_dict[word] = ops[i]

        built_words, ops = self.basic_ops.generate_words_with_basic_ops(words, index, wi, MERGE)
        for i, word in enumerate(built_words):
            if self.isword(word):
                temp_word = word.replace("#", "")
                prob = self.onegram_probability(temp_word)
                if word not in possible_words_prob_dict:
                    possible_words_prob_dict[word] = prob
                    possible_ops_dict[word] = ops[i]

        n_best_possible_words = sorted(possible_words_prob_dict, key=possible_words_prob_dict.get, reverse=True)[:17]
        n_best_possible_ops = [possible_ops_dict[key] for key in n_best_possible_words]
        n_best_possible_words.append(wi)
        n_best_possible_ops.append(NOTHING)
        return n_best_possible_words, n_best_possible_ops

    def context_base_filter(self, candidate_list, next_candidates, next_next_candidates, prev_word, current_word):
        word_prob_dict = {}
        word_ops_dict = {}
        next_next_candidate_list = []
        next_next_operation_list = []

        candidate_list, operation_list = candidate_list
        if next_candidates is not None:
            next_candidate_list, next_operation_list = next_candidates
        else:
            next_candidate_list, next_operation_list = [None], NOTHING

        if next_next_candidates is not None:
            next_next_candidate_list, next_next_operation_list = next_next_candidates
        else:
            next_candidate_list, next_operation_list = [None], NOTHING

        for i, candidate in enumerate(candidate_list):
            operation = operation_list[i]

            if operation == SPLIT:
                next_bigram_score = -1000
                first = candidate[:candidate.find('-')]
                second = candidate[candidate.find('-') + 1:]
                candidate = first
                next_word = second

                onegram_score = self.onegram_probability(candidate)
                bigram_score_with_prev = self.bigram_probability(prev_word, candidate)
                tmp_score_next = self.bigram_probability(candidate, next_word)

                for j, next_next_word in enumerate(next_candidate_list):
                    opt = next_operation_list[j]
                    if opt == MERGE:
                        next_next_word = next_next_word.replace("#", "")
                    elif opt == SPLIT:
                        next_next_word = next_next_word.split('-')[0]

                    tmp_score_next_next = self.bigram_probability(next_word, next_next_word)
                    if tmp_score_next_next > next_bigram_score:
                        next_bigram_score = tmp_score_next_next

                next_bigram_score = float(next_bigram_score + tmp_score_next) / 2

            elif operation == MERGE:
                next_bigram_score = -1000
                first = candidate[:candidate.find('#')]
                second = candidate[candidate.find('#') + 1:]
                # Merge:
                candidate = first + second

                onegram_score = self.onegram_probability(candidate)
                bigram_score_with_prev = self.bigram_probability(prev_word, candidate)

                for j, next_next_word in enumerate(next_next_candidate_list):
                    opt = next_next_operation_list[j]
                    if opt == MERGE:
                        next_next_word = next_next_word.replace("#", "")
                    elif opt == SPLIT:
                        next_next_word = next_next_word.split('-')[0]

                    temp_next_bigram_score = self.bigram_probability(candidate, next_next_word)
                    if temp_next_bigram_score > next_bigram_score:
                        next_bigram_score = temp_next_bigram_score

            else:
                onegram_score = self.onegram_probability(candidate)
                bigram_score_with_prev = self.bigram_probability(prev_word, candidate)

                next_bigram_score = -1000
                for j, next_word in enumerate(next_candidate_list):
                    opt = next_operation_list[j]
                    if opt == MERGE:
                        next_word = next_word.replace("#", "")
                    elif opt == SPLIT:
                        next_word = next_word.split('-')[0]

                    temp_next_bigram_score = self.bigram_probability(candidate, next_word)
                    if temp_next_bigram_score > next_bigram_score:
                        next_bigram_score = temp_next_bigram_score

            # adding bounces for different operations
            if operation == SUBSTITUTION:
                if self.is_homonym(current_word, candidate):
                    onegram_score += 20
                else:
                    onegram_score += 10
            elif operation == DELETION or operation == INSERTION:
                onegram_score += 5
                if '\u200c' in candidate and '\u200c' not in current_word:
                    onegram_score += 5
            elif operation == SPLIT or operation == MERGE:
                onegram_score += 7
            elif operation == NOTHING:
                onegram_score += 20

            score = 1 * onegram_score + 0.7 * bigram_score_with_prev + 0.7 * next_bigram_score

            word_prob_dict[candidate_list[i]] = score
            word_ops_dict[candidate_list[i]] = operation

        best_candidates = sorted(word_prob_dict, key=word_prob_dict.get, reverse=True)
        best_operations = [word_ops_dict[key] for key in best_candidates]
        n = len(best_candidates)
        if n >= 3:
            return best_candidates[:5], best_operations[:5]
        return best_candidates, best_operations


class SpellCorrector:
    def __init__(self):
        self.word_ev = None

    def is_in_potential_miss_spells(slef, wi, potential_miss_spells):
        for i, n_best in enumerate(potential_miss_spells):
            if wi in n_best[0]:
                return i
        return -1

    def is_in_persian_dic(self, word: str, persian_dict: dict):
        if word in persian_dict:
            return True
        return False

    def miss_spell_suggestion(self, string):
        words = TOKENIZER.tokenize_words(NORMALIZER.normalize(string))
        prev_word = None
        potential_miss_spells = []
        miss_spells_suggestions = []

        for index, word in enumerate(words):
            self.word_ev = WordsEvaluation(words, index)
            if self.is_in_persian_dic(word, PERSIAN_DICT) or word == "،":
                continue
            n_best = self.word_ev.filter_possible_words(words, index)
            potential_miss_spells.append(n_best)

        merged_before = False
        for i, wi in enumerate(words):
            self.word_ev = WordsEvaluation(words, i)
            if self.is_in_potential_miss_spells(wi, potential_miss_spells) == -1:
                continue

            if merged_before:
                continue

            if (i + 2) < len(words):
                miss_spell_index1 = self.is_in_potential_miss_spells(words[i + 1], potential_miss_spells)
                miss_spell_index2 = self.is_in_potential_miss_spells(words[i + 2], potential_miss_spells)

                if miss_spell_index1 != -1:
                    next_candidates = potential_miss_spells[miss_spell_index1]
                    if miss_spell_index2 != -1:
                        next_next_candidates = potential_miss_spells[miss_spell_index2]
                    else:
                        next_next_candidates = words[i + 2], NOTHING
                else:
                    next_candidates = words[i + 1], NOTHING
                    if miss_spell_index2 != -1:
                        next_next_candidates = potential_miss_spells[miss_spell_index2]
                    else:
                        next_next_candidates = words[i + 2], NOTHING

            elif (i + 1) < len(words):
                miss_spell_index1 = self.is_in_potential_miss_spells(words[i + 1], potential_miss_spells)
                if miss_spell_index1 != -1:
                    next_candidates = potential_miss_spells[miss_spell_index1]
                else:
                    next_candidates = words[i + 1], NOTHING
                next_next_candidates = None
            else:
                next_candidates = None
                next_next_candidates = None
            candidates = potential_miss_spells[self.is_in_potential_miss_spells(wi, potential_miss_spells)]
            best_candidates, best_operations = self.word_ev.context_base_filter(candidates, next_candidates,
                                                                                next_next_candidates, prev_word, wi)

            merged_before = False
            for j in range(len(best_candidates)):
                if best_operations[j] == SPLIT:
                    first = best_candidates[j].split('-')[0]
                    second = best_candidates[j].split('-')[1]
                    best_candidates[j] = first + " " + second
                if best_operations[j] == MERGE:
                    best_candidates[j] = best_candidates[j].replace("#", "")
                    if j == len(best_candidates) - 1:
                        merged_before = True

            miss_spells_suggestions.append({words[i]: best_candidates})
            prev_word = best_candidates[0]

        return miss_spells_suggestions
