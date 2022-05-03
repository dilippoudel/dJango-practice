from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='bookslist'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-details'),
    path('authors/', views.AuthorListView.as_view(), name='authorlist'),
]


# def get_absolute_url(self):
#     """Returns the URL to access a particular author instance."""
#     return reverse('author-details', args=[str(self.id)])
# fullurel ====> http://127.0.0.8080/catalog/book/1
