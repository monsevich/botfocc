"""Knowledge base and dialog models."""
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError

class Section(models.Model):
    name = models.CharField("Название", max_length=200, unique=True)
    slug = models.SlugField("Слаг", max_length=200, unique=True, blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"

    def __str__(self):
        return self.name

    def clean(self):
        self.slug = self.slug or slugify(self.name)

class Article(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="articles", verbose_name="Раздел")
    title = models.CharField("Заголовок", max_length=255)
    slug = models.SlugField("Слаг", max_length=255, blank=True, unique=True)
    is_published = models.BooleanField("Публиковать", default=True)

    # Основной текст (Markdown)
    content = models.TextField("Содержимое (Markdown)", blank=True)

    # Исходник в .docx (опционально) — при сохранении подтянем текст в content, если он пустой
    source_doc = models.FileField("DOCX-файл", upload_to="kb/docs/", blank=True, null=True)

    # Опциональная обложка/фото
    cover = models.ImageField("Картинка", upload_to="kb/images/", blank=True, null=True)

    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return self.title

    def clean(self):
        self.slug = self.slug or slugify(self.title)
        if not self.section_id:
            raise ValidationError("Укажите раздел.")

    def save(self, *args, **kwargs):
        # Если загружен DOCX и content пуст — сконвертируем в текст
        if self.source_doc and not (self.content and self.content.strip()):
            try:
                from docx import Document
                self.source_doc.open("rb")
                doc = Document(self.source_doc)
                text = "\n\n".join(p.text for p in doc.paragraphs).strip()
                if text:
                    # Простейшая разметка: заголовок как H1, далее текст
                    self.content = f"# {self.title}\n\n{text}"
            except Exception:
                # Не валим сохранение, просто оставим как есть
                pass
            finally:
                try:
                    self.source_doc.close()
                except Exception:
                    pass
        super().save(*args, **kwargs)
