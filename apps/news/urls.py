from django.urls import path
from .views import (
    CategoryListView,
    NewsListView,
    NewsDetailView,
    NewsCreateView,
    NewsUpdateView,
    NewsDeleteView,
    JournalistMyNewsView,
)

urlpatterns = [
   
    path('categories/', CategoryListView.as_view(), name='category-list'),

    
    path('news/', NewsListView.as_view(), name='news-list'),
    path('news/create/', NewsCreateView.as_view(), name='news-create'),
    path('news/my/', JournalistMyNewsView.as_view(), name='news-my'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail'),
    path('news/<int:pk>/update/', NewsUpdateView.as_view(), name='news-update'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news-delete'),
]
