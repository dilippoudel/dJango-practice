from pprint import pprint
from typing import Any, Callable, Optional, Sequence
from pyexpat import model
from re import template
from django.shortcuts import render, redirect

from .models import Book, Author, BookInstance, Genre, Langauge, Contact
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse

from catalog.forms import RenewBookForm, NameForm, RegistrationForm, AuthorRegistration, ContactForm


class MyView(LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'

    # paginated_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


# Create your views here.

class AllBorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_view_book_instances'
    model = BookInstance
    template_name = 'catalog/bookinstance_all_borrowed.html'
    paginated_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@login_required
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
    # ....... sssion check ... added to the rquest

    num_visits = request.session.get('num_visits', 0)

    request.session['num_visits'] = num_visits + 1

    books_stats = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
        'books_on_loan': num_instance_onloan,
        'totalGenre': num_genre
    }

    return render(request, 'index.html', context=books_stats)


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


# updating the renewal book in backend

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            """ do you own acts like saving data into data base, or retrieving the data or anymore
            """
            return HttpResponseRedirect('/catalog/books')
    else:
        form = NameForm()
        context = {
            "form": form
        }
    return render(request, 'catalog/name.html', context)


"""view for editing book page"""


def edit_book(request, pk=None):
    if pk is not None:
        allBooks = Book.objects.all()
        authors = Author.objects.all()
        genres = Genre.objects.all()
        language = Langauge.objects.all()

        def finding_current_model_book():
            for x in range(len(allBooks)):
                if allBooks[x].id == pk:
                    return allBooks[x]
            return allBooks[x]

        book_name = finding_current_model_book()
        title = book_name.title
        b_id = pk
        isbn = book_name.isbn
        summary = book_name.summary
        author_id = book_name.author_id
        from pprint import pprint

        current_author = Author.objects.get(id=author_id)

        message = ''
        context = {
            "title": title,
            "id": b_id,
            "isbn": isbn,
            "summary": summary,
            "author_id": author_id,
            'authors': authors,
            'languages': language,
            'genres': genres,
            'current_author': current_author,
            'message': message,
        }
        if request.method == 'POST':
            form = request.POST
            record_book = Book(
                title=form['title'],
                summary=form['summary'],
                isbn=form['isbn'],
                author_id=form['author']
            )
            print('#####################################################')
            print(form['isbn'])
            isExitsIsbn = Book.objects.filter(isbn=form['isbn'])

            if isExitsIsbn:
                message = 'The ISBN already exits.'
                context['message'] = message
                return render(request, 'catalog/edit.html', context)
            else:
                print('all good')

            record_book.save()
            return redirect('/catalog/books')
        return render(request, 'catalog/edit.html', context)

    else:

        return render(request, 'catalog/edit.html', context={})


def delete_book(request, pk):
    allBooks = Book.objects.all()

    def finding_delete_model_book():
        for x in range(len(allBooks)):
            if allBooks[x].id == pk:
                return allBooks[x]
        return allBooks[x]

    book_to_del = finding_delete_model_book()

    if request.method == 'POST':
        book_to_del.delete()
        return redirect('/catalog/books')

    context = {
        "id": pk
    }
    print(allBooks)

    return render(request, 'catalog/delete.html', context)


# Adding new Book
def add_book(request):
    authors = Author.objects.all()
    genres = Genre.objects.all()
    language = Langauge.objects.all()
    if request.method == 'POST':
        form = request.POST
        print(form)
        record_book = Book(
            title=form['title'],
            summary=form['summary'],
            isbn=form['isbn'],
            author_id=form['author']
        )

        record_book.save()

        return redirect('/catalog/books')

    context = {
        'authors': authors,
        'genres': genres,
        'languages': language
    }
    return render(request, 'catalog/add_book.html', context)


def registration_form(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/catalog')
    else:
        form = RegistrationForm()
        context = {
            "form": form
        }
    return render(request, 'catalog/registration_form.html', context)


# creating author
def create_author(request):
    if request.method == 'POST':
        form = AuthorRegistration(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            new_author = Author(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                date_of_death=form.cleaned_data['date_of_dead']
            )
            new_author.save()
            redirect('/catalog/authors')
    else:
        form = AuthorRegistration()
    context = {
        "form": form
    }
    return render(request, 'catalog/create_author.html', context)


def contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            record_contact = Contact(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message'],
                phone=form.cleaned_data['contact']
            )
            record_contact.save()
    else:
        form = ContactForm()
    context = {
        'form': form
    }

    return render(request, 'catalog/contact.html', context)
