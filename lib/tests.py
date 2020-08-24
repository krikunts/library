import json

from django.core.management import call_command
from django.test import TestCase, Client
from django.urls import reverse

from .models import BookShelf, BookPlace, Author


class FixtureTestCase(TestCase):
    fixture = 'fixtures/test_data.json'
    client = Client()
    STATUS_OK = 200

    def setUp(self):
        call_command('loaddata', self.fixture, verbosity=0)


class ReadTestCase(FixtureTestCase):

    def get_is_ok(self, view_name, kwargs=None):
        response = self.client.get(reverse(view_name, kwargs=kwargs or {}))
        self.assertEqual(response.status_code, self.STATUS_OK)

    def test_read_views(self):
        self.get_is_ok("author_list")

        author = Author.objects.first()
        self.get_is_ok("author_books", kwargs={"pk": author.pk})

        self.get_is_ok("shelf_list")

        shelf = BookShelf.objects.first()
        self.get_is_ok("shelf_books", kwargs={"pk": shelf.pk})


class ReorderTestCase(FixtureTestCase):

    def reorder_post(self, shelf, book_places):
        data = [[{"id": place.id, "book": place.book_id} for place in book_places]]
        return self.client.post(reverse("shelf_books", kwargs={"pk": shelf.pk}),
                                data=json.dumps(data),
                                content_type='application/json')

    def test_reorder_success(self):
        shelf = BookShelf.objects.first()
        places = BookPlace.objects.filter(shelf=shelf)
        old_books = list(places.values_list("book", flat=True))
        # reverse the books order
        response = self.reorder_post(shelf, reversed(list(places)))
        # check results
        self.assertEqual(response.status_code, self.STATUS_OK)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'status': 'success'})
        new_places = BookPlace.objects.filter(shelf=shelf).values_list("book", flat=True)
        self.assertEqual(list(reversed(new_places)), old_books)

    def test_reorder_error(self):
        shelf = BookShelf.objects.first()
        book_ids = list(shelf.books.values_list('id', flat=True))
        # post only the first book on the shelf
        response = self.reorder_post(shelf, [shelf.places.first()])
        # check results
        self.assertEqual(response.status_code, self.STATUS_OK)
        resp_json = json.loads(response.content)
        self.assertEqual(resp_json.get('status'), 'error')
        self.assertEqual(resp_json.get('books'), book_ids)
