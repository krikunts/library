import json

from django.db import transaction, DatabaseError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import ListView

from .models import Author, Book, BookShelf, BookPlace


class AuthorListView(ListView):
    model = Author
    paginate_by = 10


class AuthorBooksView(ListView):
    model = Book
    paginate_by = 10
    template_name = "list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(authors=self.kwargs.get("pk")).order_by("title")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["author"] = Author.objects.get(pk=self.kwargs.get("pk"))
        return context


class BookShelfListView(ListView):
    model = BookShelf
    paginate_by = 10


@method_decorator(ensure_csrf_cookie, name='get')
class BookShelfBooksView(ListView):
    model = BookPlace
    template_name = "lib/shelf_books.html"

    def get_shelf(self):
        return BookShelf.objects.get(pk=self.kwargs.get("pk"))

    def get_queryset(self):
        return super().get_queryset().filter(shelf=self.kwargs.get("pk"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["shelf"] = self.get_shelf()
        return context

    def reorder_error_response(self, message=None):
        book_ids = self.get_shelf().books.values_list("id", flat=True)
        message = message or "При изменении порядка книг произошла ошибка"
        return JsonResponse({"status": "error", "error": message, "books": list(book_ids)})

    def post(self, request, *args, **kwargs):
        shelf = self.get_shelf()
        old_book_ids = shelf.books.values_list("id", flat=True)
        data = json.loads(request.body)[0]
        new_book_ids = [item["book"] for item in data]
        if set(new_book_ids) != set(old_book_ids):
            return self.reorder_error_response("Попытка изменить набор книг на полке")
        if len(new_book_ids) < 2:
            return JsonResponse({"status": "success"})
        book_places = [
            BookPlace(shelf=shelf, book_id=book_id, place=i + 1)
            for i, book_id in enumerate(new_book_ids)
        ]
        try:
            with transaction.atomic():
                shelf.places.all().delete()
                BookPlace.objects.bulk_create(book_places)
        except DatabaseError:
            return self.reorder_error_response()
        return JsonResponse({"status": "success"})
