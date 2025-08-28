"""Knowledge base and dialog models."""
from __future__ import annotations

from django.db import models


class Section(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name


class Entry(models.Model):
    section = models.ForeignKey(Section, related_name="entries", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)

    def __str__(self) -> str:  # pragma: no cover
        return self.title


class Chunk(models.Model):
    entry = models.ForeignKey(Entry, related_name="chunks", on_delete=models.CASCADE)
    index = models.PositiveIntegerField()
    text = models.TextField()


class Attachment(models.Model):
    entry = models.ForeignKey(Entry, related_name="attachments", on_delete=models.CASCADE)
    file = models.FileField(upload_to="kb/")


class DialogSession(models.Model):
    external_id = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class DialogMessage(models.Model):
    session = models.ForeignKey(DialogSession, related_name="messages", on_delete=models.CASCADE)
    role = models.CharField(max_length=10)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
