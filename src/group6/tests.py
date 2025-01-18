from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
import json

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    @patch("views.generator")
    def test_suggest_word(self, mock_generator):
        mock_generator.return_value = [
            {"generated_text": "test word suggestion one"},
            {"generated_text": "test word suggestion two"},
            {"generated_text": "test word suggestion three"},
        ]

        response = self.client.get(reverse("suggest_word"), {"text": "test"})

        self.assertEqual(response.status_code, 200)

    @patch("views.load_feedback")
    @patch("views.save_feedback")
    def test_system_feedback(self, mock_save_feedback, mock_load_feedback):
        mock_load_feedback.return_value = {"ratings": [4, 5], "average": 4.5}

        response = self.client.get(reverse("system_feedback"), {"rating": 3})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "\u0628\u0627\u0632\u062e\u0648\u0631\u062f \u0634\u0645\u0627 \u0628\u0627 \u0645\u0648\u0641\u0642\u06cc\u062a \u062b\u0628\u062a \u0634\u062f.")
        self.assertGreater(data["average_rating"], 0)

        mock_save_feedback.assert_called_once()

    def test_download_text(self):
        response = self.client.get(reverse("download_text"), {"text": "Sample generated text."})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain;charset=utf-8")
        self.assertIn("attachment; filename=\"generated_text.txt\"", response["Content-Disposition"])
        self.assertEqual(response.content.decode("utf-8"), "Sample generated text.")

    def test_download_text_empty(self):
        response = self.client.get(reverse("download_text"), {"text": ""})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "\u0645\u062a\u0646 \u062e\u0627\u0644\u06cc \u0627\u0633\u062a.")

    def test_home_view(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
