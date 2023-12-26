from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from main.services.utils import unique_slugify



class Article(models.Model):
    """
    Модель новости
    """

    h1 = models.CharField(max_length=200)
    title = models.CharField(verbose_name='Название статьи', max_length=255)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True)
    description = models.TextField(verbose_name='Краткое описание', max_length=500)
    text = models.TextField(verbose_name='Полный текст статьи')
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='articles', verbose_name='Категория')
    thumbnail = models.ImageField(
        verbose_name='Изображение статьи',

        upload_to='images/thumbnails/%Y/%m/%d/',
        default='images/thumbnails/1234567.jpg',
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))]
    )
    status = models.CharField(default='published', verbose_name='Статус статьи', max_length=10)
    create = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    author = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.SET_DEFAULT, related_name='author_articles',
                               default=1)
    updater = models.ForeignKey(to=User, verbose_name='Обновил', on_delete=models.SET_NULL, null=True,
                                related_name='updater_articles', blank=True)
    fixed = models.BooleanField(verbose_name='Прикреплено', default=False)

    class Meta:
        db_table = 'news_article'
        ordering = ['-fixed', '-create']
        indexes = [models.Index(fields=['-fixed', '-create', 'status'])]
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Получаем прямую ссылку на статью
        """
        return reverse('article_detail', kwargs={'slug': self.slug})

        # Функции str и get_absolute_url

# Функции str и get_absolute_url

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)





class Category(MPTTModel):
    """
    Модель категорий с вложенностью
    """
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, verbose_name='URL категории', blank=True)
    description = models.TextField(verbose_name='Описание категории', max_length=300)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name='children',
        verbose_name='Родительская категория'
    )

    class MPTTMeta:
        """
        Сортировка по вложенности
        """
        order_insertion_by = ('title',)

    class Meta:
        """
        Сортировка, название модели в админ панели
        """
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'app_categories'


    def get_absolute_url(self):
        """
        Получаем прямую ссылку на категорию
        """
        return reverse('article_by_category', kwargs={'slug': self.slug})

    def __str__(self):
        """
        Возвращение заголовка статьи
        """
        return self.title



class Comment(MPTTModel):
    """
    Модель древовидных комментариев
    """

    STATUS_OPTIONS = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )

    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Запись', related_name='comments')
    author = models.ForeignKey(User, verbose_name='Автор комментария', on_delete=models.CASCADE, related_name='comments_author')
    content = models.TextField(verbose_name='Текст комментария', max_length=3000)
    time_create = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)
    time_update = models.DateTimeField(verbose_name='Время обновления', auto_now=True)
    status = models.CharField(choices=STATUS_OPTIONS, default='published', verbose_name='Статус поста', max_length=10)
    parent = TreeForeignKey('self', verbose_name='Родительский комментарий', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    class MTTMeta:
        """
        Сортировка по вложенности
        """
        order_insertion_by = ('-time_create',)

    class Meta:
        """
        Сортировка, название модели в админ панели, таблица в данными
        """
        ordering = ['-time_create']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author}:{self.content}'