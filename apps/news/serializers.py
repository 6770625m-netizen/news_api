from rest_framework import serializers
from .models import News, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class NewsListSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)

    class Meta:
        model = News
        fields = [
            'id', 'title', 'author_name', 'category',
            'image', 'status', 'views_count', 'created_at',
        ]

    def get_author_name(self, obj):
        return obj.author.get_full_name() or obj.author.username


class NewsDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            'id', 'title', 'content', 'author_name', 'category',
            'image', 'status', 'views_count', 'comments_count',
            'created_at', 'updated_at',
        ]

    def get_author_name(self, obj):
        return obj.author.get_full_name() or obj.author.username

    def get_comments_count(self, obj):
        return obj.comments.count()


class NewsCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['title', 'content', 'category', 'image', 'status']
