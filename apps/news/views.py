from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from .models import News, Category
from .serializers import (
    NewsListSerializer,
    NewsDetailSerializer,
    NewsCreateUpdateSerializer,
    CategorySerializer,
)
from apps.accounts.permissions import IsJournalist, IsAdmin, IsNotBlocked


class CategoryListView(generics.ListAPIView):
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class NewsListView(generics.ListAPIView):
    
    serializer_class = NewsListSerializer
    permission_classes = [IsAuthenticated, IsNotBlocked]

    def get_queryset(self):
        qs = News.objects.filter(status=News.STATUS_PUBLISHED).select_related('author', 'category')
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        if category:
            qs = qs.filter(category__slug=category)
        if search:
            qs = qs.filter(title__icontains=search)
        return qs


class NewsDetailView(generics.RetrieveAPIView):
    
    serializer_class = NewsDetailSerializer
    permission_classes = [IsAuthenticated, IsNotBlocked]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return News.objects.all()
        if user.is_journalist:
            
            return News.objects.filter(status=News.STATUS_PUBLISHED) | News.objects.filter(author=user)
        return News.objects.filter(status=News.STATUS_PUBLISHED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        News.objects.filter(pk=instance.pk).update(views_count=instance.views_count + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class NewsCreateView(generics.CreateAPIView):
    
    serializer_class = NewsCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsJournalist]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NewsUpdateView(generics.UpdateAPIView):
    
    serializer_class = NewsCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return News.objects.all()
        if user.is_journalist:
            return News.objects.filter(author=user)
        return News.objects.none()

    def get_permissions(self):
        from apps.accounts.permissions import IsAdminOrJournalist
        return [IsAuthenticated(), IsAdminOrJournalist()]


class NewsDeleteView(generics.DestroyAPIView):
    
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return News.objects.all()
        if user.is_journalist:
            return News.objects.filter(author=user)
        return News.objects.none()

    def get_permissions(self):
        from apps.accounts.permissions import IsAdminOrJournalist
        return [IsAuthenticated(), IsAdminOrJournalist()]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Yangilik o'chirildi."}, status=status.HTTP_200_OK)


class JournalistMyNewsView(generics.ListAPIView):
    
    serializer_class = NewsListSerializer
    permission_classes = [IsAuthenticated, IsJournalist]

    def get_queryset(self):
        return News.objects.filter(author=self.request.user).order_by('-created_at')
