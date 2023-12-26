from django.contrib.auth.models import User

from .models import Article, Category
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView
from .forms import ArticleCreateForm
from django.views.generic import UpdateView
from .forms import ArticleUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .services.mixins import AuthorRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.views import View
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import redirect
from .forms import CommentCreateForm
from .models import Comment




class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['form'] = CommentCreateForm
        return context


class ArticleFromCategory(ListView):
    model = Article
    template_name = 'news/article_by_category.html'
    context_object_name = 'articles'
    category = None
    paginate_by = 5
    # queryset = Article.custom.all()  # Переопределение вызова модели

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        queryset = Article.objects.filter(category__slug=self.category.slug)
        if not queryset:
            sub_cat = Category.objects.filter(parent=self.category)
            queryset = Article.objects.filter(category__in=sub_cat)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Статьи из категории: {self.category.title}'
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """
    Представление: создание материалов на сайте
    """
    model = Article
    template_name = 'news/article_create.html'
    form_class = ArticleCreateForm
    login_url = 'index'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи на сайт'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class UserArticleListView(ListView):
    model = Article
    template_name = 'news/user_articles.html'
    context_object_name = 'articles'
    paginate_by = 5
    success_url = reverse_lazy('index')
    login_url = 'index'


    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Article.objects.filter(author = user).order_by('-create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мои статьи'
        return context





class SearchResultsView(View):
    paginate_by = 5
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        results = ""
        if query:
            results = Article.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        paginator = Paginator(results, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'news/search.html', context={
            'title': 'Поиск',
            'results': results,
            'count': len(results)
        })


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление: удаления материала
    """
    model = Article
    success_url = reverse_lazy('index')
    context_object_name = 'article'
    template_name = 'news/articles_delete.html'
    login_url = _url = 'index'
    # messages.msg = 'Запись удалена'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = f'Удаление статьи: {self.object.title}'
    #     return context


    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.author:
            return self.handle_no_permission()
        login_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(login_url)






class ArticleUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: обновления материала на сайте
    """
    model = Article
    template_name = 'news/article_update.html'
    context_object_name = 'article'
    form_class = ArticleUpdateForm
    login_url = 'index'
    success_message = 'Запись была успешно обновлена!'

    class Meta:
        model = Article
        fields = ['title', 'description', 'text', 'thumbnail', 'category']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Обновление статьи'
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs




from django.shortcuts import render

def tr_handler404(request, exception):
    """
    Обработка ошибки 404
    """
    return render(request=request, template_name='errors/error_page.html', status=404, context={
        'title': 'Страница не найдена: 404',
        'error_message': 'К сожалению такая страница была не найдена, или перемещена',
    })


def tr_handler500(request):
    """
    Обработка ошибки 500
    """
    return render(request=request, template_name='errors/error_page.html', status=500, context={
        'title': 'Ошибка сервера: 500',
        'error_message': 'Внутренняя ошибка сайта, вернитесь на главную страницу, отчет об ошибке мы направим администрации сайта',
    })


def tr_handler403(request, exception):
    """
    Обработка ошибки 403
    """
    return render(request=request, template_name='errors/error_page.html', status=403, context={
        'title': 'Ошибка доступа: 403',
        'error_message': 'Доступ к этой странице ограничен',
    })




class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentCreateForm

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def form_invalid(self, form):
        if self.is_ajax():
            return JsonResponse({'error': form.errors}, status=400)
        return super().form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article_id = self.kwargs.get('pk')
        comment.author = self.request.user
        comment.parent_id = form.cleaned_data.get('parent')
        comment.save()

        if self.is_ajax():
            return JsonResponse({
                'is_child': comment.is_child_node(),
                'id': comment.id,
                'author': comment.author.username,
                'parent_id': comment.parent_id,
                'time_create': comment.time_create.strftime('%Y-%b-%d %H:%M:%S'),
                'avatar': comment.author.profile.avatar.url,
                'content': comment.content,
                'get_absolute_url': comment.author.profile.get_absolute_url()
            }, status=200)

        return redirect(comment.article.get_absolute_url())

    def handle_no_permission(self):
        return JsonResponse({'error': 'Необходимо авторизоваться для добавления комментариев'}, status=400)