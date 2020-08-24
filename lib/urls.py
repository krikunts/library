from django.urls import path

from . import views

urlpatterns = [
    path('', views.AuthorListView.as_view()),
    path('authors', views.AuthorListView.as_view(), name="author_list"),
    path('author/<int:pk>', views.AuthorBooksView.as_view(), name="author_books"),
    path('shelves', views.BookShelfListView.as_view(), name="shelf_list"),
    path('shelf/<int:pk>', views.BookShelfBooksView.as_view(), name="shelf_books"),
]
