from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class MainMenu(models.Model):
    item = models.CharField(max_length=200, unique=True)
    link = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.item


class BookRating(models.Model):
    rating = models.DecimalField(decimal_places=1, max_digits=2,
                                 validators=[MinValueValidator(1.0), MaxValueValidator(5.0)], default=5)

    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.rating) + str(self.id)


class Book(models.Model):
    name = models.CharField(max_length=200)
    web = models.URLField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    publishdate = models.DateField(auto_now=True)
    picture = models.FileField(upload_to='bookEx/static/uploads')
    pic_path = models.CharField(max_length=300, editable=False, blank=True)
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    total_rating = models.DecimalField(decimal_places=1, max_digits=65, default=5)
    # rating = models.ManyToManyField(Readers)

    def __str__(self):
        return str(self.id)

class BookRating(models.Model):
    rating = models.DecimalField(decimal_places=1, max_digits=2,
                                 validators=[MinValueValidator(1.0), MaxValueValidator(5.0)], default=5)

    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, blank=True, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.rating) + str(self.username)


