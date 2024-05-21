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
    created = models.DateTimeField(
        verbose_name="Created",
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        verbose_name="Updated",
        auto_now=True,
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    person = models.ForeignKey(
        Person,
        verbose_name="Person",
        blank=False,
        on_delete=models.CASCADE,
    )
    details = models.TextField(
        verbose_name="Details",
        blank=False,
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name="Rate (1-5)",
        blank=False,
    )
    created = models.DateTimeField(
        verbose_name="Created",
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        verbose_name="Updated",
        auto_now=True,
    )

    def __str__(self):
        return "{name} - {rating}".format(
            name = self.person.name,
            rating=self.rating,
        )

