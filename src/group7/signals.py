from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from meilisearch import Client
from .models import Word, Synonym, UserProfile
import logging

logger = logging.getLogger(__name__)

# Initialize Meilisearch client
client = Client('http://127.0.0.1:7700')
index_name = 'words'

try:
    # Ensure index exists
    indexes = client.get_indexes()

    # Handle response structure
    existing_indexes = [
        index['uid'] if isinstance(index, dict) else index
        for index in indexes.get('results', indexes)
    ]

    if index_name not in existing_indexes:
        client.create_index(uid=index_name)
        logger.info(f"Index '{index_name}' created successfully.")

    index = client.index(index_name)
except Exception as e:
    logger.error(f"Error initializing Meilisearch index '{index_name}': {e}")
    index = None


@receiver(post_save, sender=Word)
def index_word(sender, instance, **kwargs):
    if not index:
        logger.warning("Meilisearch index is not initialized.")
        return

    try:
        synonyms = Synonym.objects.filter(word_id=instance.id).values_list('synonym', flat=True)
        document = {
            "id": instance.id,
            "word": instance.word,
            "synonyms": list(synonyms),
        }
        index.add_documents([document])
        logger.info(f"Word (ID: {instance.id}) indexed successfully.")
    except Exception as e:
        logger.error(f"Error indexing Word (ID: {instance.id}): {e}")


@receiver(post_delete, sender=Word)
def delete_word(sender, instance, **kwargs):
    if not index:
        logger.warning("Meilisearch index is not initialized.")
        return

    try:
        index.delete_document(str(instance.id))
        logger.info(f"Word (ID: {instance.id}) deleted from index successfully.")
    except Exception as e:
        logger.error(f"Error deleting Word (ID: {instance.id}) from index: {e}")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
            email=instance.email or "default@example.com",
            first_name=instance.first_name or "بدون نام",
            last_name=instance.last_name or "بدون نام",
            profile_image="uploads/profiles/default-profile.png",  # تصویر پیش‌فرض
            bio="...",
            additional_info="..."
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()