from django.contrib.syndication.views import Feed
from django.urls import reverse
from news.models import Article

class LatestArticleFeed(Feed):
    title = "Мой блог на Django - последние записи"
    link = "/feeds/"
    description = "Новые записи на моем сайте."

    def items(self):
        return Article.objects.order_by('-update')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return reverse('article_detail', args=[item.slug])