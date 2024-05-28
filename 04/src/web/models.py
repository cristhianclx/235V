from django.db import models


class Document(models.Model):
    cv = models.FileField(
        upload_to="cv",
        blank=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )