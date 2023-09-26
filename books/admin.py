from django.contrib import admin

# Register your models here.
from books.models import Category, Author, Book


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')