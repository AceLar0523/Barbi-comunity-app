from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Barbie
from .chroma_client import add_barbie_to_index

@receiver(post_save, sender=Barbie)
def index_barbie_in_chroma(sender, instance, created, **kwargs):
    """
    When a Barbie is saved (created or updated), automatically add or update it in ChromaDB.
    """
    try:
        add_barbie_to_index(instance)
    except Exception as e:
        print(f"Error indexing Barbie {instance.id} in ChromaDB: {e}")
