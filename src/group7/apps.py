from django.apps import AppConfig
from meilisearch import Client
import logging

logger = logging.getLogger(__name__)


class Group7Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'group7'

    def ready(self):
        # Import necessary models and signals
        from group7.models import Word, Synonym
        import group7.signals

        # Initialize Meilisearch client
        client = Client('http://127.0.0.1:7700')

        try:
            # Fetch the list of indexes and ensure 'words' exists
            indexes = client.get_indexes()

            # Handle response structure
            existing_indexes = [
                index['uid'] if isinstance(index, dict) else index
                for index in indexes.get('results', indexes)
            ]

            if 'words' not in existing_indexes:
                client.create_index(uid='words')
                logger.info("Index 'words' created successfully.")

            index = client.index('words')

            # Fetch data from the database
            words = Word.objects.all()
            documents = [
                {
                    "id": word.id,
                    "word": word.word,
                    "synonyms": list(
                        Synonym.objects.filter(word_id=word.id).values_list('synonym', flat=True)
                    ),
                }
                for word in words
            ]

            # Add documents to the index
            if documents:
                index.add_documents(documents)
                logger.info(f"Successfully indexed {len(documents)} documents into 'words'.")
            else:
                logger.info("No documents to index.")

        except Exception as e:
            logger.error(f"Error while setting up Meilisearch index: {e}")
