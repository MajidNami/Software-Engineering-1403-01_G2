import pytest
from src.group5.logic.miss_spell_finder import WordsEvaluation


class TestWordsEvaluation:
    def setup_method(self, method):
        self.words_eva = WordsEvaluation([], 0)

    @pytest.mark.parametrize("word, output", [("سلام", True), ("قارپوز", False)])
    def test_isword(self, word, output):
        assert self.words_eva.isword(word) == output

    @pytest.mark.parametrize("current_word, candidate_word, output", [("سلام", "صلام", True), ("علی", "علا", False)])
    def test_is_homonym(self, current_word, candidate_word, output):
        assert self.words_eva.is_homonym(current_word, candidate_word) == output

    @pytest.mark.parametrize("words, index, output", [(["سلام"], 0, (
            ['سلامت', 'اسلام', 'سلاح', 'سالم', 'سهام', 'سیام', 'کلام', 'سلام', 'سل-ام', 'سلامی', 'س-لام', 'سلیم',
             'غلام',
             'آلام', 'سام', 'سلامه', 'سجام', 'سلام'],
            ['insertion', 'insertion', 'substitution', 'transposition', 'substitution', 'substitution', 'substitution',
             'substitution', 'split', 'insertion', 'split', 'substitution', 'substitution', 'substitution', 'deletion',
             'insertion', 'substitution', 'nothing'])), (["نجات"], 0, (
            ['نجات', 'نکات', 'نشات', 'ن-جات', 'جات', 'نیات', 'نجار', 'نجاتی', 'نجابت', 'نبات', 'ونجات', 'نجا-ت', 'نات',
             'نجاتش', 'نجاح', 'نظات', 'نجاست', 'نجات'],
            ['substitution', 'substitution', 'substitution', 'split', 'deletion', 'substitution', 'substitution',
             'insertion',
             'insertion', 'substitution', 'insertion', 'split', 'deletion', 'insertion', 'substitution', 'substitution',
             'insertion', 'nothing']))])
    def test_filter_possible_words(self, words, index, output):
        assert self.words_eva.filter_possible_words(words, index) == output

