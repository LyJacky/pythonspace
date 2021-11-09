from django.contrib.auth import get_user_model
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from .models import MainMenu
from .forms import BookForm, BookRatingForm
from .models import Book, BookRating
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required

class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)


@login_required(login_url=reverse_lazy('login'))
def index(request):
    # return HttpResponse('Hello')
    # return render(request,'base.html')
    # return render(request,'bookMng/displaybooks.html')
    return render(request,
                  'bookMng/index.html',
                  {
                    'item_list': MainMenu.objects.all()

                  })
@login_required(login_url=reverse_lazy('login'))
def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
            form = BookForm()
            if 'submitted' in request.GET:
                submitted = True
    return render(request,
                  'bookMng/postbook.html',
                  {
                    'form': form,
                    'item_list': MainMenu.objects.all(),
                    'submitted': submitted

                  })

@login_required(login_url=reverse_lazy('login'))
def displaybooks(request):
    books = Book.objects.all()
    for b in books:
        b.picture_path = b.picture.url[14:]

    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                  })

@login_required(login_url=reverse_lazy('login'))
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[14:]
    form = BookRatingForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            bookrating = form.save(commit=False)
            # # print(book.map['test'])
            # if book.map.get(request.user) is None:
            #     book.map[request.user] = bookrating.rating
            # total_rating = 0
            # for books in book.map:
            #    print(books)
            #    total_rating += book.map[books]
            # print(total_rating)
            # print(321312312312)
            # book.total_rating = bookrating.rating + book.total_rating
            # book.avg_rating = total_rating/len(book.map)
            book.save()

            return HttpResponseRedirect('/displaybooks')
    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book,
                      'form': form,
                  })

@login_required(login_url=reverse_lazy('login'))
def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return render(request,
                  'bookMng/book_delete.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  })

@login_required(login_url=reverse_lazy('login'))
def mybooks(request):
    books = Book.objects.filter(username=request.user)
    for b in books:
        b.picture_path = b.picture.url[14:]
    return render(request,
                  'bookMng/mybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                  })

def aboutus(request):
    return render(request,
                  'bookMng/aboutus.html',
                  {
                      'item_list': MainMenu.objects.all()
                  })

@login_required(login_url=reverse_lazy('login'))
def search(request):
    if request.method == 'GET':
        query = request.GET.get('b')

        submitbutton = request.GET.get('submit')

        if query is not None:
            User = get_user_model()
            users = User.objects.filter(username__icontains=query)
            book_by_user = None
            for user in users:
                book_by_user = Q(username=user) or book_by_user
            lookups = Q(id__icontains=query) | Q(name__icontains=query)
            results = Book.objects.filter(lookups).distinct() or Book.objects.filter(book_by_user).distinct()
            for b in results:
                b.picture_path = b.picture.url[14:]

            return render(request, 'bookMng/search.html', {
                      'item_list': MainMenu.objects.all(),
                      'results': results,
                      'submitbutton': submitbutton,
                  })

        else:
            return render(request, 'bookMng/search.html', {
                      'item_list': MainMenu.objects.all()
                  })

    else:
        return render(request, 'bookMng/search.html', {
                      'item_list': MainMenu.objects.all()
                  })