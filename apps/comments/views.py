from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from .models import Comment
from .serializers import CommentSerializer, CommentCreateSerializer
from apps.accounts.permissions import IsAdmin, IsNotBlocked
from apps.news.models import News


class CommentListView(generics.ListAPIView):
    authentication_classes = []
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        news_id = self.kwargs['news_id']
        get_object_or_404(News, id=news_id)
        return Comment.objects.filter(news_id=news_id).select_related('author')


class CommentCreateView(generics.CreateAPIView):
   
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated, IsNotBlocked]

    def get_permissions(self):
        from apps.accounts.permissions import IsNotBlocked
        from rest_framework.permissions import IsAuthenticated
        return [IsAuthenticated(), IsNotBlocked()]

    def perform_create(self, serializer):
        user = self.request.user
        # Faqat oddiy foydalanuvchilar izoh yoza oladi
        if not user.is_user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Faqat foydalanuvchilar izoh yoza oladi.")
        serializer.save(author=user)


class CommentDeleteView(APIView):
    
    permission_classes = [IsAuthenticated]

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        user = request.user

        if user.is_admin or comment.author == user:
            comment.delete()
            return Response({"message": "Izoh o'chirildi."}, status=status.HTTP_200_OK)

        return Response(
            {"error": "Siz faqat o'z izohingizni o'chira olasiz."},
            status=status.HTTP_403_FORBIDDEN
        )


class AdminCommentListView(generics.ListAPIView):
    
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        qs = Comment.objects.select_related('author', 'news').order_by('-created_at')
        news_id = self.request.query_params.get('news_id')
        user_id = self.request.query_params.get('user_id')
        if news_id:
            qs = qs.filter(news_id=news_id)
        if user_id:
            qs = qs.filter(author_id=user_id)
        return qs


class JournalistCommentListView(generics.ListAPIView):
   
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from apps.accounts.permissions import IsJournalist
        user = self.request.user
        if not (user.is_journalist or user.is_admin):
            return Comment.objects.none()
        return Comment.objects.filter(
            news__author=user
        ).select_related('author', 'news').order_by('-created_at')
