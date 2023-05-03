from django.urls import path
from accounts.views import Profile
from .views import SingleNews, SearchNews, NewsList, CreateNews, CreateArticle, EditNews, DeleteNews


urlpatterns = [
    path('', NewsList.as_view(), name='main'),
    path('<int:pk>/', SingleNews.as_view(), name='single_news'),
    path('<int:pk>/edit/', EditNews.as_view(), name='post_edit'),
    path('<int:pk>/delete/', DeleteNews.as_view(), name='post_delete'),
    path('search/', SearchNews.as_view()),
    path('create/', CreateNews.as_view()),
    path('article/create/', CreateArticle.as_view()),
    path('profile/', Profile.as_view(), name='profile'),
]
