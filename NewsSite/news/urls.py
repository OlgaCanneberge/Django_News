from django.urls import path
from .views import ArticleFromCategory, ArticleDetailView, ArticleCreateView, ArticleUpdateView, UserArticleListView, SearchResultsView, ArticleDeleteView, CommentCreateView


urlpatterns = [
    path('news/search/', SearchResultsView.as_view(), name='search_results'),
    path('news/article/<str:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('news/create/', ArticleCreateView.as_view(), name='article_create'),
    path('news/category/<str:slug>/', ArticleFromCategory.as_view(), name="article_by_category"),
    path('news/article/<str:slug>/update/', ArticleUpdateView.as_view(), name='article_update'),
    path('news/user/<str:username>/', UserArticleListView.as_view(), name='user_articles'),
    path('news/<int:pk>/comments/create/', CommentCreateView.as_view(), name='comment_create_view'),
    path('articles/<str:slug>/delete/', ArticleDeleteView.as_view(), name='articles_delete'),
    # path('search/', SearchResultsView.as_view(), name='search_results'),
]