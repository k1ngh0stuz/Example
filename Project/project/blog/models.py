from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')

    def get_absolute_url(self):
        return reverse('category_list', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Category pk = {self.pk}, title = {self.title}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Article(models.Model):
    # id создается автоматически
    title = models.CharField(max_length=155, verbose_name='Название')
    content = models.TextField(blank=True, verbose_name='Описание')  # Не обязательно для заполнения
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')  # авто время создания
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')  # Авто время обновления
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name='Изображение')
    is_publisher = models.BooleanField(default=True, verbose_name='Опубликовано')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    def get_absolute_url(self):
        return reverse('article_details', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Article pk = {self.pk}, title = {self.title}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']  # Сортировка от новых к старым
