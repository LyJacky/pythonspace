from django.contrib import admin

# Register your models here.
from .models import MainMenu
from .models import Book
from .models import BookRating
from .models import Messages
from .models import IndivMessages

admin.site.register(MainMenu)
admin.site.register(Book)
admin.site.register(BookRating)
admin.site.register(Messages)
admin.site.register(IndivMessages)
