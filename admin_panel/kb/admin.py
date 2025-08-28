"""Django admin registrations for knowledge base."""
from django.contrib import admin
from .models import Section, Article

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "section", "is_published", "updated_at")
    list_filter = ("section", "is_published")
    search_fields = ("title", "content")
    readonly_fields = ("created_at", "updated_at")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {"fields": ("section", "title", "slug", "is_published")}),
        ("Содержимое", {"fields": ("content", "source_doc", "cover")}),
        ("Служебное", {"fields": ("created_at", "updated_at")}),
    )
