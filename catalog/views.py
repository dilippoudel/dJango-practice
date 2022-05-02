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
        # Get 5 books containing the title war
        # lists = Book.objects.all()
        # list = Book.objects.filter(title__icontains='the')

        # return {lists, list}

        return Book.objects.all()


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'
