from django.db import models


class Person(models.Model):
    fullname = models.CharField(max_length=200, null=False)
    dni = models.PositiveIntegerField(unique=True, null=False)

    def __str__(self):
        return self.fullname
