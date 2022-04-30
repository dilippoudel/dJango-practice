from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
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
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'books_on_loan': num_instance_onloan,
        'totalGenre': num_genre
    }

    return render(request, 'index.html', context=context)
