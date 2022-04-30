from atexit import register
from pyexpat import model
from django.contrib import admin
from .models import Genre, Book, BookInstance, Langauge, Author, Student
# Register your models here.


# Define the admin class

# Define the admin class

# admin.site.register(Book)
# admin.site.register(Author)
# Define the admin class


# CHALANNGE 1
class BookAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'status', 'due_back', 'id')


# admin.site.register(BookInstance)

# @admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

# Register the Admin classes for BookInstance using the decorator


class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    fieldsets = (
        ('Book Details', {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        })
    )


"""Inline editable display view"""


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]


# challenge 2
class BooksInline(admin.TabularInline):
    model = Book


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name',
                    'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', 'date_of_birth']
    inlines = [BooksInline, ]


# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(Langauge)
admin.site.register(Student)
