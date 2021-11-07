from django import forms
from django.forms import ModelForm
from .models import Book
from .models import BookRating


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'name',
            'web',
            'price',
            'picture',
        ]


class BookRatingForm(ModelForm):
    class Meta:
        model = BookRating
        fields = [
            'rating',
        ]

