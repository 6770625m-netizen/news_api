from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render, redirect
from rest_framework_simplejwt.views import TokenRefreshView


def register_view(request): return render(request, 'register.html')
def login_view(request):    return render(request, 'login.html')
def profile_view(request):  return render(request, 'profile.html')
def yangilik_view(request): return render(request, 'yangilik.html')
def home_view(request):     return render(request, 'home.html')
def redirect_register_html(request): return redirect('/')
def redirect_login_html(request):    return redirect('/login/')
def redirect_profile_html(request):  return redirect('/profile/')
def redirect_yangilik_html(request): return redirect('/yangilik/')
def redirect_home_html(request):     return redirect('/home/')


urlpatterns = [
    path('admin/', admin.site.urls),

    
    path('', register_view, name='register-page'),
    path('login/', login_view, name='login-page'),
    path('profile/', profile_view, name='profile-page'),
    path('yangilik/', yangilik_view, name='yangilik-page'),
    path('home/', home_view, name='home-page'),
    
    
    path('register.html', redirect_register_html),
    path('login.html', redirect_login_html),
    path('profile.html', redirect_profile_html),
    path('yangilik.html', redirect_yangilik_html),
    path('home.html', redirect_home_html),

   
    path('api/auth/', include('apps.accounts.urls')),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('apps.news.urls')),
    path('api/', include('apps.comments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
