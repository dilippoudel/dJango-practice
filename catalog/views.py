from pyexpat import model
from re import template
from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
# Create your views here.


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # available Books status a
    num_instances_available = BookInstance.objects.filter(
        status__exact='a').count()
    num_authors = Author.objects.count()
    num_instance_onloan = BookInstance.objects.filter(
        status__icontains='o').count()
    num_genre = Genre.objects.count()
    roshan = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'books_on_loan': num_instance_onloan,
        'totalGenre': num_genre
    }

    return render(request, 'index.html', context=roshan)


#  class based view
class BookListView(generic.ListView):
    model = Book
    context_object_name = "book_lists"
    # Specify your own template name/location
    template_name = 'book_list.html'

# overriding the method ===>  get_queryset() is a special method in DJango
    def get_queryset(self):

        return Book.objects.all()


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'


class AuthorListView(generic.ListView):
    model = Author
# when we don't over ride the template_name, it automatically watch the template in templates/catalog/author_list.html


class AuthorDetailView(generic.DetailView):
    model = Author
