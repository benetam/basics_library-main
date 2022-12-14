import uuid

from django.db import models
from django.urls import reverse

# Create your models here.
class Genre(models.Model):
    name = models.CharField('Pavadinimas', max_length=100, help_text='Nurodykite žanro pavadinimą (pvz. detektyvas)')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Žanras'
        verbose_name_plural = 'Žanrai'


class Book(models.Model):
    """Modelis reprezentuojantis knygą"""
    title = models.CharField('Pavadinimas', max_length=200)
    author = models.ForeignKey('Author', max_length=200, null=True, on_delete=models.SET_NULL, related_name='books')
    summary = models.TextField('Aprašymas', max_length=1000, help_text='Trumpas knygos aprašymas')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 simbolių unikalus ISBN kodas')
    genre = models.ManyToManyField(Genre, help_text='Išsirinkite knygos žanrą(us)')
    cover = models.ImageField('Viršelis', upload_to='covers', null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Nurodo konkretaus knygos aprašymo galutinį adresą"""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ','.join(genre.name for genre in self.genre.all()[:3])

class BookInstance(models.Model):
    """Modelis aprašantis konkrečios knygos kopijos būseną"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unikalus ID knygos kopijai')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    due_back = models.DateField('Bus prieinama', null=True, blank=True)

    LOAN_STATUS = (
        ('a', 'Administruojama'),
        ('p', 'Paimta'),
        ('g', 'Galima paimti'),
        ('r', 'Rezervuota')
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, default='a', help_text='Statusas', blank=True)

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} {self.book.title}'


class Author(models.Model):
    """Modelis reprezentuojantis knygos autorių."""
    first_name = models.CharField('Vardas', max_length=80)
    last_name = models.CharField('Pavardė', max_length=80)
    description = models.TextField('Aprašymas', max_length=200, default='')

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Nurodo konkretaus autoriaus galutinį adresą"""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    def display_books(self):
        return ', '.join(book.title for book in self.books.all()[:3])

    display_books.short_description = 'Knygos'

