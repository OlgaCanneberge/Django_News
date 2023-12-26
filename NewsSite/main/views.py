from django.views import View

from django.core.paginator import Paginator
from django.views.generic import ListView
from django.db.models import Q

from news.models import Article
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View




class MainView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.all().order_by('-create')
        paginator = Paginator(articles, 3)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'main/index.html', context={
            'page_obj': page_obj
        })

class SearchResultsView(View):

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        results = ""
        if query:
            results = Article.objects.filter(
                Q(h1__icontains=query) | Q(description__icontains=query)
            )
        paginator = Paginator(results, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'news/search.html', context={
            'title': 'Поиск',
            'results': page_obj,
            'count': paginator.count
        })


class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main/about.html'
        )

class ContactView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main/contact.html'
        )



def custom_404(request, exception):
    return render(request, '404_403.html', status=404, context={
        'title': 'Ничего не найдено'
          })

def custom_403(request, exception):
    return render(request, '404_403.html', status=403, context={
        'title': 'Доступ ограничен'
          })





