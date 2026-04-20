from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import User
from .serializers import (
    RegisterSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
    ChangePasswordSerializer,
    AdminUserListSerializer,
    BlockUserSerializer,
)
from .permissions import IsAdmin


class RegisterView(generics.CreateAPIView):
    
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Muvaffaqiyatli ro'yxatdan o'tdingiz!",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    
    permission_classes = [AllowAny]

    def post(self, request):
        from django.contrib.auth import authenticate
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {"error": "Username va parol kiritish majburiy."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"error": "Username yoki parol noto'g'ri."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if user.is_currently_blocked:
            msg = "Hisobingiz bloklangan."
            if user.blocked_until:
                msg += f" Muddati: {user.blocked_until.strftime('%d.%m.%Y %H:%M')}"
            if user.block_reason:
                msg += f" Sabab: {user.block_reason}"
            return Response({"error": msg}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response({
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role,
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        })


class LogoutView(APIView):
  
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Muvaffaqiyatli chiqdingiz."})
        except Exception:
            return Response({"error": "Token noto'g'ri yoki allaqachon bekor qilingan."}, status=400)


class ProfileView(generics.RetrieveUpdateAPIView):
  
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return UserProfileUpdateSerializer
        return UserProfileSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
   
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({"message": "Parol muvaffaqiyatli o'zgartirildi."})




class AdminUserListView(generics.ListAPIView):
    """Admin: barcha foydalanuvchi va jurnalistlarni ko'rish."""
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = AdminUserListSerializer

    def get_queryset(self):
        qs = User.objects.exclude(role=User.ROLE_ADMIN).order_by('-created_at')
        role = self.request.query_params.get('role')
        if role in [User.ROLE_USER, User.ROLE_JOURNALIST]:
            qs = qs.filter(role=role)
        return qs


class AdminBlockUserView(APIView):
    
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, user_id):
        
        user = get_object_or_404(User, id=user_id)
        if user.is_admin:
            return Response({"error": "Adminni bloklash mumkin emas."}, status=400)

        serializer = BlockUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user.is_blocked = True
        user.blocked_until = serializer.validated_data.get('blocked_until')
        user.block_reason = serializer.validated_data.get('block_reason', '')
        user.save(update_fields=['is_blocked', 'blocked_until', 'block_reason'])

        msg = f"'{user.username}' bloklandi."
        if user.blocked_until:
            msg += f" Muddati: {user.blocked_until.strftime('%d.%m.%Y %H:%M')}"
        return Response({"message": msg})

    def delete(self, request, user_id):
      
        user = get_object_or_404(User, id=user_id)
        user.is_blocked = False
        user.blocked_until = None
        user.block_reason = None
        user.save(update_fields=['is_blocked', 'blocked_until', 'block_reason'])
        return Response({"message": f"'{user.username}' blokdan chiqarildi."})


class AdminDeleteNewsView(APIView):
    
    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request, news_id):
        from apps.news.models import News
        news = get_object_or_404(News, id=news_id)
        title = news.title
        news.delete()
        return Response({"message": f"'{title}' yangiligi o'chirildi."})
