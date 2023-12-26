from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import Category, Article


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    """
    Админ-панель модели категорий
    """
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Админ-панель модели записей
    """
    prepopulated_fields = {'slug': ('title',)}



from .models import Comment

@admin.register(Comment)
class CommentAdminPage(DjangoMpttAdmin):
    """
    Админ-панель модели комментариев
    """
    pass