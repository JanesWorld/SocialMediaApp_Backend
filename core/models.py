from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model


User = settings.AUTH_USER_MODEL


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    theme = models.CharField(max_length=10, default="light")
    email_notifications = models.BooleanField(default=True)
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following", blank=True
    )

    def followers_count(self):
        return self.followers.count()

    def following_count(self):
        return self.following.count()

    username = models.TextField(max_length=70, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar_height = models.PositiveIntegerField(null=True, blank=True)
    avatar_width = models.PositiveIntegerField(null=True, blank=True)
    profile_pic = models.ImageField(
        upload_to="avatars/",
        height_field="avatar_height",
        width_field="avatar_width",
        blank=True,
        null=True,
    )
    registration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class TimelineEvent(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="timeline_events"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    text_content = models.TextField(blank=True)
    image_content = models.ImageField(upload_to="moments_images/", blank=True)
    likes = models.ManyToManyField(User, related_name="liked_events", blank=True)

    def __str__(self):
        return f"{self.user.username} event at {self.created_at.strftime('%Y-%m-%d')}"

    def is_image(self):
        return bool(self.image_content)

    def is_text(self):
        return bool(self.text_content.strip())


class Comment(models.Model):
    timeline_event = models.ForeignKey(
        TimelineEvent, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.created_at.strftime('%Y-%m-%d')}"
