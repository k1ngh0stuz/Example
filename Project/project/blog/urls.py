from django.urls import path
from .views import *


urlpatterns = [
    # path('', index, name='index'),
    # path('category/<int:pk>/', articles_by_category, name='category_list'),
    # path('article/<int:pk>/', article_details, name='article_details'),
    # path('new/', add_article, name='add_article'),
    path('profile/', profile, name='profile'),
    path('login/', user_login, name='login'),
    path('logout/', UserLogout, name='logout'),
    path('register/', RegisterUser, name="register"),

    path('', ArticleList.as_view(), name='index'),  # Путь на классах
    path('category/<int:pk>/', ArticleListByCategory.as_view(), name='category_list'),
    path('article/<int:pk>/', ArticleDetail.as_view(), name='article_details'),
    path('new/', NewArticle.as_view(), name='add_article'),
    path('search/', SearchResults.as_view(), name='search_results'),
    path('article/<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),


]