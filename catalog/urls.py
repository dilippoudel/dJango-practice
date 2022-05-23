from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books', views.BookListView.as_view(), name='bookslist'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-details'),
    path('authors/', views.AuthorListView.as_view(), name='authorlist'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.AllBorrowedBooksListView.as_view(), name='all-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian,
         name='renew-book-librarian'),
    path('user/signup/', views.SignUpView.as_view(), name='registration-name'),
    path('book/delete/<int:pk>', views.delete_book, name='delete-book'),
    path('author/create/', views.create_author, name='create-author'),
    path('author/edit/<int:pk>', views.edit_author, name='edit-author'),
    path('author/delete/<int:pk>', views.delete_author, name='delete-author'),
    path('contact/', views.contact_form, name='contact-form'),
    path('book/create/', views.create_new_books, name='create-new-book'),
    path('book/edit/<int:pk>', views.edit_book, name='edit-book'),
]
