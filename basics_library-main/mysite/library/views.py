from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Book, BookInstance, Author, Genre

# Create your views here.

def index(request):

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # laisvos knygos
    num_instances_available = BookInstance.objects.filter(status__exact='g').count()

    num_authors = Author.objects.all().count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books':num_books,
        'num_instances':num_instances,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors,
        'num_visits':num_visits
    }

    return render(request, 'library/index.html', context=context)


def authors(request):
    paginator = Paginator(Author.objects.all(), 3)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)
    context = {
        'authors': paged_authors
    }
    return render(request, 'library/authors.html', context=context)


# def books(request):
#     books = Book.objects.all()
#     context = {
#         'books': books
#     }
#     return render(request, 'library/books.html', context=context)


class BookListView(generic.ListView):
    model = Book
    template_name = 'library/book_list.html'
    context_object_name = 'my_book_list'


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'library/book_detail.html'

def author(request, author_id):
    single_author = get_object_or_404(Author, pk=author_id)
    # author = {
    #     'author':single_author
    # }
    return render(request, 'library/author.html', {'author': single_author})

def search(request):
    query = request.GET.get('query')
    lt_letters = {'ž': 'z', 'š': 's', 'į':'i'}
    # 1. Loop through query
    # query = ''
    for raide in query:
       if raide in lt_letters.keys():
           print(lt_letters[raide])
    search_results = Book.objects.filter(Q(title__icontains=query) | Q(summary__icontains = query))
    return render(request, 'library/search.html', {'books': search_results, 'query': query})

