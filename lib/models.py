from django.db import models


class Author(models.Model):

    class Meta:
        ordering = ("last_name", "first_name", "pk")

    first_name = models.CharField(verbose_name="имя", max_length=100)
    last_name = models.CharField(verbose_name="фамилия", max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class BookShelf(models.Model):
    class Meta:
        ordering = ("code", "pk")
    code = models.CharField(verbose_name="код", max_length=100, unique=True)

    def __str__(self):
        return self.code

    @property
    def books(self):
        return Book.objects.filter(place__shelf=self)


class Book(models.Model):
    title = models.CharField(verbose_name="название", max_length=100)
    authors = models.ManyToManyField(Author, verbose_name="авторы", related_name="books")

    def __str__(self):
        return ", ".join(str(a) for a in self.authors.all()) + f" - {self.title}"


class BookPlace(models.Model):

    class Meta:
        unique_together = ("shelf", "place")
        ordering = ("place", )

    book = models.OneToOneField(Book, verbose_name="книга", on_delete=models.CASCADE, related_name="place")
    shelf = models.ForeignKey(BookShelf, verbose_name="полка", on_delete=models.CASCADE, related_name="places")
    place = models.PositiveIntegerField(verbose_name="место")

    def __str__(self):
        return f"место {self.place}: {self.book}"
