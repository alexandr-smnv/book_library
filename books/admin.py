from django.contrib import admin

# Register your models here.
from books.models import Author, Basket, Book, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('book',)
    extra = 0
