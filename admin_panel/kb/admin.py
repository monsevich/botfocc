"""Django admin registrations for knowledge base."""
from __future__ import annotations

import requests
from django.conf import settings
from django.contrib import admin, messages

from .models import Attachment, Chunk, DialogMessage, DialogSession, Entry, Section


class ChunkInline(admin.TabularInline):
    model = Chunk
    extra = 0
    readonly_fields = ("index", "text")


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("title", "section", "is_published")
    list_filter = ("section", "is_published")
    search_fields = ("title", "content")
    inlines = [ChunkInline, AttachmentInline]
    actions = ["publish", "unpublish", "reindex"]

    def publish(self, request, queryset):
        queryset.update(is_published=True)

    def unpublish(self, request, queryset):
        queryset.update(is_published=False)

    def reindex(self, request, queryset):
        url = getattr(settings, "BOT_API_URL", "http://bot_api:8000") + "/kb/reindex"
        requests.post(url, timeout=5)
        messages.success(request, "Reindex triggered")


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(DialogSession)
class DialogSessionAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at",)
    search_fields = ("external_id",)


@admin.register(DialogMessage)
class DialogMessageAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at",)
    list_filter = ("role",)
    search_fields = ("text",)
    raw_id_fields = ("session",)
