from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Article, Category
from .forms import ArticleForm, LoginForm, RegisterForm
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator  # Переход страниц
from django.contrib.auth import login, logout
from django.contrib import messages


# Create your views here.

# def index(request):
#     articles = Article.objects.all()
#     context = {
#         'articles': articles,
#     }
#
#     return render(request, 'blog/all_articles.html', context)


# def articles_by_category(request, pk):
#     articles = Article.objects.filter(category_id=pk)
#     context = {
#         'articles': articles,
#     }
#
#     return render(request, 'blog/all_articles.html', context)


# def article_details(request, pk):  # Полная информация о статье
#     article = Article.objects.get(pk=pk)
#     context = {
#         'title': article.title,
#         'article': article
#     }
#     return render(request, 'blog/article_detail.html', context)


# def add_article(request):
#     if request.method == 'POST':
#         form = ArticleForm(data=request.POST)  # Получаем отправленные данные в форму
#         if form.is_valid():  # Нормальные ли данные в форме
#             # title = form.cleaned_data['title']  # Вот так вытаскиваются данные
#             article = Article.objects.create(**form.cleaned_data)  # Kwargs
#             article.save()
#             return redirect('article_details', article.pk)
#
#     else:
#         form = ArticleForm()
#
#     context = {
#         'form': form,
#         'title': 'Добавить статью'
#     }
#
#     return render(request, 'blog/article_form.html', context)


class ArticleList(ListView):
    paginate_by = 3
    model = Article  # Какая модель получаем
    context_object_name = 'articles'  # objects - Но мы уже прописали, что имя articles
    template_name = 'blog/all_articles.html'
    extra_context = {
        'title': 'Все статьи из класса'
    }

    def get_queryset(self):  # Что выводить
        return Article.objects.filter(is_publisher=True).select_related('category')


class ArticleListByCategory(ArticleList):  # Это тоже список. Но с другим условием
    def get_queryset(self):
        return Article.objects.filter(
            category_id=self.kwargs['pk'],
            is_publisher=True
        ).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()  # Забираем весь контекст который был
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = category.title
        return context


class ArticleDetail(DetailView):
    model = Article

    def get_queryset(self):
        return Article.objects.filter(pk=self.kwargs['pk'], is_publisher=True).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        article = Article.objects.get(pk=self.kwargs['pk'])
        context['title'] = f'Статья: {article.title}'
        return context


class NewArticle(CreateView):
    form_class = ArticleForm
    template_name = 'blog/article_form.html'
    extra_context = {
        'title': 'Добавить статью'
    }

    #  success_url = reverse_lazy('index')


class SearchResults(ArticleList):
    def get_queryset(self):
        word = self.request.GET.get('q')
        articles = Article.objects.filter(
            Q(title__icontains=word) | Q(content__icontains=word), is_publisher=True
        )
        return articles


class ArticleUpdate(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'


class ArticleDelete(DeleteView):
    model = Article
    success_url = reverse_lazy('index')
    context_object_name = 'article'


@login_required  # Запрет на переход на эту страницу не зареганным пользовательям
def profile(request):
    return render(request, 'blog/profile.html', {'title': 'Ваш профиль'})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'Вы успешно авторизовались')
                next = request.POST.get('next', 'index')
                return redirect(next)
            else:
                messages.error(request, 'Что то пошло не так')
                return redirect('index')
    else:
        form = LoginForm()

    context = {
        'title': 'Авторизация пользователья',
        'form': form
    }

    return render(request, 'blog/user_login.html', context)


def UserLogout(request):
    logout(request)
    return redirect('index')


def RegisterUser(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()  # Вот так вот проходит регистрация
            messages.success(request, "Аккаунт успешно создан")
            return redirect('index')
        else:
            messages.error(request, 'Что-то пошло не так, попробуйте снова')
            return redirect('RegisterUser')
    else:
        form = RegisterForm()

    context = {
        'title': 'Регистрация пользователья',
        'form': form
    }

    return render(request, 'blog/register.html', context)
