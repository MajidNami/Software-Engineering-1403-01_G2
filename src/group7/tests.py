# Create your tests here.
from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve

from .models import *
from .views import *


class WordModelTest(TestCase):
    def setUp(self):
        self.word = Word.objects.create(word="سلام")

    def test_word_creation(self):
        self.assertEqual(self.word.word, "سلام")
        self.assertEqual(str(self.word), "سلام")

    def test_unique_word(self):
        with self.assertRaises(Exception):
            Word.objects.create(word="سلام")



class SynonymModelTest(TestCase):
    def setUp(self):
        self.word = Word.objects.create(word="سلام")
        self.synonym = Synonym.objects.create(synonym="درود", word=self.word)

    def test_synonym_creation(self):
        self.assertEqual(self.synonym.synonym, "درود")
        self.assertEqual(self.synonym.word, self.word)

    def test_str_method(self):
        self.assertEqual(str(self.synonym), "درود (for سلام)")









class FavoriteWordModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="hessam", email="hessam@example.com")
        self.word = Word.objects.create(word="سلام")
        self.favorite_word = FavoriteWord.objects.create(user=self.user, word=self.word)

    def test_favorite_word_creation(self):
        self.assertEqual(self.favorite_word.user, self.user)
        self.assertEqual(self.favorite_word.word, self.word)

    def test_unique_together(self):
        with self.assertRaises(Exception):
            FavoriteWord.objects.create(user=self.user, word=self.word)

    def test_str_method(self):
        self.assertEqual(str(self.favorite_word), "سلام")




class StaticViewsTest(TestCase):

    def test_about_view(self):
        response = self.client.get(reverse('group7:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_index_view(self):
        response = self.client.get(reverse('group7:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')





class UserProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='hessam', password='12345')
        self.client.login(username='hessam', password='12345')

    def test_user_profile_with_valid_session(self):
        response = self.client.get(reverse('group7:user_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'hessam')


class EditProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='hessam', password='12345')
        self.client.login(username='hessam', password='12345')

    def test_edit_profile_get(self):
        response = self.client.get(reverse('group7:edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_profile.html')

    def test_edit_profile_post(self):
        response = self.client.post(reverse('group7:edit_profile'), {
            'first_name': 'hessam',
            'last_name': 'hos',
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.first_name, 'hessam')
        self.assertEqual(self.user.profile.last_name, 'hos')
        self.assertRedirects(response, reverse('group7:user_profile'))





class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('group7:home')
        self.assertEqual(resolve(url).func, index)

    def test_about_url_resolves(self):
        url = reverse('group7:about')
        self.assertEqual(resolve(url).func, about)

    def test_search_url_resolves(self):
        url = reverse('group7:exact_search_words')
        self.assertEqual(resolve(url).func, exact_search_words)

    def test_profile_url_resolves(self):
        url = reverse('group7:user_profile')
        self.assertEqual(resolve(url).func, user_profile)

    def test_edit_profile_url_resolves(self):
        url = reverse('group7:edit_profile')
        self.assertEqual(resolve(url).func, edit_profile)

    def test_highlight_words_url_resolves(self):
        url = reverse('group7:highlight_words')
        self.assertEqual(resolve(url).func, highlight_words)

    def test_invalid_url_returns_404(self):
        response = self.client.get('/invalid-path/')
        self.assertEqual(response.status_code, 404)