from rest_framework import serializers
from .models import UserProfile, Post, Comment, TimelineEvent


class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    username = serializers.CharField(source="user.username")

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "username",
            "profile_pic",
            "first_name",
            "last_name",
            "theme",
            "email_notifications",
        ]
        read_only_fields = ("id",)

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        user = instance.user
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.save()
        return super().update(instance, validated_data)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "content", "created_at"]


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()
    author_avatar = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "timeline_event",
            "author",
            "author_username",
            "author_avatar",
            "content",
            "created_at",
        ]
        read_only_fields = ("author", "timeline_event", "id", "created_at")

    def get_author_username(self, obj):
        return obj.author.username

    def get_author_avatar(self, obj):
        request = self.context.get("request")
        if obj.author.userprofile.profile_pic and hasattr(
            obj.author.userprofile.profile_pic, "url"
        ):
            return request.build_absolute_uri(obj.author.userprofile.profile_pic.url)
        else:
            return "/media/avatars/DefaultAvatar.jpg"


class TimelineEventSerializer(serializers.ModelSerializer):
    is_image = serializers.SerializerMethodField()
    is_text = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    likes_by_current_user = serializers.SerializerMethodField()

    class Meta:
        model = TimelineEvent
        fields = [
            "id",
            "user",
            "created_at",
            "text_content",
            "image_content",
            "is_image",
            "comments",
            "is_text",
            "likes_count",
            "likes_by_current_user",
        ]

    def get_is_image(self, obj):
        return obj.is_image()

    def get_is_text(self, obj):
        return obj.is_text()

    def get_likes_by_current_user(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return obj.likes.filter(id=request.user.id).exists()
        return False
