import os
import copy
from parsivar import DataHelper
import pandas as pd

DATA_HELPER = DataHelper()

# PATHS
DIR_PATH = os.path.dirname(os.path.realpath(__file__)) + "/"
BIGRAM_LM_PATH = "/resource/mybigram_lm.pckl"
ONEGRAM_LM_PATH = "/resource/onegram.pckl"
PERSIAN_DICT_PATH = "src/group5/logic/confs/resource/updated_persian_dic3.xlsx"

# OBJECTS
HOMONYM_CHARS = [{'ا', 'آ', 'ع'},
                 {'ت', 'ط'},
                 {'ث', 'س', 'ص'},
                 {'ح', 'ه'},
                 {'ذ', 'ز', 'ض', 'ظ'},
                 {'ق', 'غ'}]
ALPHABET = ['ا', 'آ', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ',
            'د', 'ذ', 'ر', 'ز', 'ژ', 'س', 'ش', 'ص', 'ض', 'ط',
            'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل', 'م', 'ن',
            'و', 'ه', 'ی', '‌']

# BASIC OPS
SPELL = "spell"
MERGE = "merge"
SPLIT = "split"
NOTHING = "nothing"
DELETION = "deletion"
INSERTION = "insertion"
SUBSTITUTION = "substitution"
TRANSPOSITION = "transposition"


def get_bigram_lm():
    return DATA_HELPER.load_var(DIR_PATH + BIGRAM_LM_PATH)


def get_onegram_lm():
    return DATA_HELPER.load_var(DIR_PATH + ONEGRAM_LM_PATH)


def get_homonym_chars():
    return copy.deepcopy(HOMONYM_CHARS)


def get_alphabet():
    return copy.deepcopy(ALPHABET)


def get_persian_dictionary(file_path: str):
    persian_dict = {}
    try:
        data = pd.read_excel(file_path)
        for _, row in data.iterrows():
            words = [word.strip() for word in str(row.iloc[0]).split('،')]  # Handle multiple spellings
            for word in words:
                persian_dict[word] = ""
        return persian_dict
    except Exception as e:
        print("An error occurred:", e)
