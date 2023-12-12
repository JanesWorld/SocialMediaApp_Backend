from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenObtainPairView.as_view(), name="token_refresh"),
    path("api/register/", views.registration_view, name="register"),
    path("api/profile/", views.user_profile, name="user_profile"),
    path(
        "api/check-availability/", views.check_availability, name="check-availability"
    ),
    path("api/posts/", views.post_list_create, name="post_list_create"),
    path("api/timeline-events/", views.moments_create, name="create-moments"),
    path(
        "api/timeline-events/<int:pk>/",
        views.timeline_event_detail,
        name="moments-detail",
    ),
    path(
        "api/timeline-events/<int:event_id>/comments/",
        views.create_comment,
        name="create-comment",
    ),
    path(
        "api/timeline-events/<int:event_id>/like/",
        views.handle_like,
        name="handle-like",
    ),
    path("api/comments/<int:comment_id>/", views.delete_comment, name="delete_comment"),
    path("api/suggested-users/", views.get_suggested_users, name="suggested_users"),
    path(
        "api/user-profile/<int:user_id>/", views.get_user_profile, name="user_profile"
    ),
]
