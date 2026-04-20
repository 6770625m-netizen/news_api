from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    ProfileView,
    ChangePasswordView,
    AdminUserListView,
    AdminBlockUserView,
    AdminDeleteNewsView,
)

urlpatterns = [
   
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

   
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/change-password/', ChangePasswordView.as_view(), name='change-password'),

   
    path('admin/users/', AdminUserListView.as_view(), name='admin-users'),
    path('admin/users/<int:user_id>/block/', AdminBlockUserView.as_view(), name='admin-block-user'),
    path('admin/news/<int:news_id>/delete/', AdminDeleteNewsView.as_view(), name='admin-delete-news'),
]
