from django import forms
from django.forms import ModelForm
from .models import Book
from .models import BookRating
from .models import Messages
from .models import IndivMessages


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


class BookMessageForm(ModelForm):
    class Meta:
        model = Messages
        fields = [
            'message',
        ]


class IndivMessageForm(ModelForm):
    class Meta:
        model = IndivMessages
        fields = [
            'receiver',
            'message',
        ]

