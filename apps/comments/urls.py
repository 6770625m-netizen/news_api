from django.urls import path
from .views import (
    CommentListView,
    CommentCreateView,
    CommentDeleteView,
    AdminCommentListView,
    JournalistCommentListView,
)

urlpatterns = [
    
    path('news/<int:news_id>/comments/', CommentListView.as_view(), name='comment-list'),
    path('comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:comment_id>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

   
    path('comments/my-news/', JournalistCommentListView.as_view(), name='journalist-comments'),

    
    path('admin/comments/', AdminCommentListView.as_view(), name='admin-comment-list'),
]
