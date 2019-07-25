from uuid import uuid4

from django.db import models


class Note(models.Model):
    uuid = models.UUIDField(
        default=uuid4, editable=False, db_index=True, unique=True
    )
    author = models.CharField(max_length=32)
    title = models.CharField(max_length=32)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
