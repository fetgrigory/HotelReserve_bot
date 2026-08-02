from asgiref.sync import sync_to_async
from .models import FAQ


# Inserts faq chunks and their embeddings
@sync_to_async
def insert_faq_data(data):
    faq = FAQ(
        question=data["question"],
        answer=data["answer"],
        embedding=data["embedding"],
    )
    faq.save()
