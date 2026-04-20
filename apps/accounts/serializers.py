from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, label="Parolni tasdiqlang")

    
    role = serializers.ChoiceField(choices=[
        (User.ROLE_USER, 'Foydalanuvchi'),
        (User.ROLE_JOURNALIST, 'Jurnalist'),
    ])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'role', 'first_name', 'last_name']

    def validate_role(self, value):
        if value not in User.REGISTERABLE_ROLES:
            raise serializers.ValidationError(
                "Ro'yxatdan o'tishda faqat 'user' yoki 'journalist' rolini tanlash mumkin."
            )
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password2": "Parollar mos kelmadi."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'bio', 'avatar', 'is_blocked', 'blocked_until',
            'block_reason', 'created_at',
        ]
        read_only_fields = ['id', 'role', 'is_blocked', 'blocked_until', 'block_reason', 'created_at']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio', 'avatar']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password2": "Yangi parollar mos kelmadi."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Eski parol noto'g'ri.")
        return value


class AdminUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'is_blocked', 'blocked_until', 'block_reason',
            'is_active', 'created_at',
        ]


class BlockUserSerializer(serializers.Serializer):
    
    blocked_until = serializers.DateTimeField(
        required=False,
        allow_null=True,
        help_text="Bloklash tugash vaqti. Bo'sh qoldirilsa, doimiy bloklanadi."
    )
    block_reason = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Bloklash sababi."
    )
