from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('postbook', views.postbook, name='postbook'),
    path('displaybooks',views.displaybooks, name='displaybooks'),
    path('aboutus',views.aboutus, name='aboutus'),
    path('book_detail/<int:book_id>',views.book_detail, name='book_detail'),
    path('mybooks', views.mybooks, name='mybooks'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    path('book_detail/rating_delete/<int:book_id>', views.rating_delete, name='rating_delete'),
    path('search', views.search, name='search'),
    path('book_message', views.book_message, name='book_message'),
    path('book_imessage', views.book_imessage, name='book_imessage'),
    path('messagebox', views.messagebox, name='messagebox'),
]