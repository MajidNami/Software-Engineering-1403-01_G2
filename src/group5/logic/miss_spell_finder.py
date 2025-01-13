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
