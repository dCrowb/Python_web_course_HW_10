from django.db import models


# Create your models here.
class Author(models.Model):
    fullname = models.CharField(max_length=64, null=False)
    born_date = models.CharField(max_length=32, null=False)
    born_location = models.CharField(max_length=128, null=False)
    description = models.TextField()

    def __str__(self):
        return f"{self.fullname}"


class Tag(models.Model):
    name = models.CharField(max_length=64, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Quote(models.Model):
    quote = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=False)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.name}"
