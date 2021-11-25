from django import forms
from django.forms import ModelForm
from .models import Book
from .models import BookRating
from .models import Messages
from .models import IndivMessages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


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
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control'})
        }


class IndivMessageForm(ModelForm):
    class Meta:
        model = IndivMessages
        fields = [
            'receiver',
            'message',
        ]
        widgets = {
            'receiver': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'})
        }

