from django.db import models


class Person(models.Model):
    name = models.CharField(
        verbose_name="Name (name of a person)",
        max_length=100,
        blank=False,
    )
    age = models.PositiveSmallIntegerField(
        verbose_name="Age",
        blank=False,
    )
    description = models.TextField(
        verbose_name="Description",
        blank=False,
    )