import json
from django.core.management.base import BaseCommand
from group7.models import Word, Synonym

class Command(BaseCommand):
    help = "Import words and synonyms from JSON file into the database."

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="Path to the JSON file containing word data.")

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)


        for entry in data:
            word_text = entry.get('word')

            synonyms = entry.get('synonyms', [])

            word_obj, created = Word.objects.get_or_create(word=word_text)
            for synonym in synonyms:
                Synonym.objects.get_or_create(word=word_obj, synonym=synonym)

        self.stdout.write(self.style.SUCCESS("Data imported successfully!"))
