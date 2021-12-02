from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse

from .models import MainMenu
from .forms import BookForm, BookRatingForm, BookMessageForm, IndivMessageForm
from .models import Book, BookRating, Messages, IndivMessages, UserCart
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum


class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = SignUpForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)


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
    form = BookRatingForm(request.POST, request.FILES)
    lookups = Q(book=book) & Q(username=request.user)
    results = BookRating.objects.filter(lookups).distinct()
    result = None
    for res in results:
        result = res
        break
    if request.method == 'POST':
        if form.is_valid():
            book_rating = result
            if book_rating is not None:
                rating = form.save(commit=False)
                book_rating.username = request.user
                book_rating.rating = rating.rating
                book_rating.book = book
                book_rating.save()
            else:
                book_rating = form.save(commit=False)
                book_rating.username = request.user
                book_rating.book = book
                book.total_rating = book_rating.rating
                book_rating.save()

            all_ratings = BookRating.objects.filter(book=book)
            total_rating = 0
            total_number_of_ratings = 0
            for rating in all_ratings:
                total_number_of_ratings += 1
                total_rating += rating.rating
            if total_number_of_ratings != 0:
                book.avg_rating = total_rating / total_number_of_ratings
            else:
                book.avg_rating = 0
            book.save()
            return HttpResponseRedirect('/book_detail/' + str(book_id))
    all_ratings = BookRating.objects.filter(book=book)
    total_rating = 0
    total_number_of_ratings = 0
    for rating in all_ratings:
        total_number_of_ratings += 1
        total_rating += rating.rating
    if total_number_of_ratings != 0:
        book.avg_rating = total_rating / total_number_of_ratings
    else:
        book.avg_rating = None
        return render(request,
                      'bookMng/book_detail.html',
                      {
                          'item_list': MainMenu.objects.all(),
                          'book': book,
                          'form': form,
                      })
    if result is None:
        return render(request,
                      'bookMng/book_detail.html',
                      {
                          'item_list': MainMenu.objects.all(),
                          'book': book,
                          'form': form,
                      })
    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book,
                      'form': form,
                      'book_rating': result.rating,
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
def rating_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[14:]
    lookups = Q(book=book) & Q(username=request.user)
    results = BookRating.objects.filter(lookups).distinct()
    result = None
    for res in results:
        result = res
        break
    if result is not None:
        result.delete()
    else:
        return render(request,
                      'bookMng/rating_delete_fail.html',
                      {
                          'item_list': MainMenu.objects.all(),
                      })
    return render(request,
                  'bookMng/rating_delete.html',
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
                # or Book.objects.filter(book_by_user).distinct() Q(id__icontains=query) |
            lookups = Q(id__icontains=query) | Q(name__icontains=query)
            if book_by_user is None:
                results = Book.objects.filter(lookups).distinct()
            else:
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


@login_required(login_url=reverse_lazy('login'))
def messagebox(request):
    messages = Messages.objects.all()
    imessages = IndivMessages.objects.filter(receiver=request.user)
    books = Book.objects.all()
    return render(request,
                  'bookMng/messagebox.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'messages': messages,
                      'books': books,
                      'imessages': imessages,

                  })

@login_required(login_url=reverse_lazy('login'))
def book_message(request):
    if request.method == 'POST':
        form = BookMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            try:
                message.username = request.user
            except Exception:
                pass
            message.save()
            return HttpResponseRedirect('/messagebox')
    else:
        form = BookMessageForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'bookMng/book_message.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      # 'submitted': submitted,
                  })

@login_required(login_url=reverse_lazy('login'))
def book_imessage(request):
    user = get_user_model()
    users = user.objects.all()
    error = '0'
    if request.method == 'POST':
        form = IndivMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            for u in users:
                if u.username == message.receiver:
                    try:
                        message.username = request.user
                    except Exception:
                        pass
                    message.save()
                    return HttpResponseRedirect('/messagebox')
        error = '1'
        return  render(request,
                  'bookMng/book_imessage.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'error': error,
                      # 'submitted': submitted,
                  })
    else:
        form = IndivMessageForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'bookMng/book_imessage.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'error': error,
                      # 'submitted': submitted,
                  })

@login_required(login_url=reverse_lazy('login'))
def shoppingcart(request):
    books = UserCart.objects.filter(username=request.user)
    totalPrice = list(books.aggregate(Sum('price')).values())[0]
    return render(request,
        'bookMng/shoppingcart.html',
        {
            'item_list': MainMenu.objects.all(),
            'books': books,
            'totalPrice': totalPrice
        })


@login_required(login_url=reverse_lazy('login'))
def book_addCart(request, book_id):
    books = Book.objects.all()
    book = Book.objects.get(id=book_id)
    item = UserCart()
    item.username = request.user
    item.bookId = book
    item.price = book.price
    item.name = book.name
    item.save()
    return redirect('displaybooks')


@login_required(login_url=reverse_lazy('login'))
def book_deleteCart(request, cart_id):
    cartItem = UserCart.objects.get(id=cart_id)
    cartItem.delete()
    return redirect('shoppingcart')
