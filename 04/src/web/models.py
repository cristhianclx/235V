from django.core.validators import FileExtensionValidator
from django.db import models

class Document(models.Model):
    cv = models.FileField(
        upload_to="cv",
        blank=False,
        validators=[FileExtensionValidator(allowed_extensions=["pdf", "docx"])]
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class DocumentMatch(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
    )
    position = models.CharField(
        max_length=255,
        blank=False,
    )
    url = models.URLField(
        blank=True,
    )
    ranking = models.DecimalField(
        max_digits=30,
        decimal_places=25,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
