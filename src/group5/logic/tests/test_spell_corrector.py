import pytest
from src.group5.logic.miss_spell_finder import SpellCorrector


class TestSpellCorrector:
    def setup_method(self, method):
        self.spell_corrector = SpellCorrector()

    @pytest.mark.parametrize("string, output", [("صلام این یک مطن آذمایشی هست", [{'صلام': ['سلام', 'صلاح', 'غلام', 'کلام', 'صدام']}, {'مطن': ['متن', 'من', 'مان', 'وطن', 'مین']}, {'آذمایشی': ['آزمایشی', 'آمایشی', 'آذمایشی']}]), ("بنزر شما فارصی زیان ظیبایی اسط ؟ !", [{'بنزر': ['بنظر', 'بندر', 'بن زر', 'بنز ر', 'بنزن']}, {'فارصی': ['فارسی', 'فارغی', 'فارلی', 'فار صی', 'فارشی']}, {'ظیبایی': ['زیبایی', 'دیبایی', 'لیبایی', 'ظی بایی', 'ظیبایی']}, {'اسط': ['است', 'اسب', 'اسد', 'اسم', 'وسط']}])])
    def test_spell_corrector(self, string, output):
        assert self.spell_corrector.miss_spell_suggestion(string) == output
