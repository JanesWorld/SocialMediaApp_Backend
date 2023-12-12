from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post
from .models import UserProfile
from .models import TimelineEvent
from .serializers import PostSerializer
from .serializers import CommentSerializer
from .serializers import UserProfileSerializer
from .serializers import TimelineEventSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Comment


# Profile Settings
@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def user_profile(request):
    print("User:", request.user)
    print("Authenticated:", request.user.is_authenticated)
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        print("UserProfile does not exist")
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = UserProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Registration View
@api_view(["POST"])
def registration_view(request):
    if request.method == "POST":
        username = request.data.get("username")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        password = request.data.get("password")
        password2 = request.data.get("confirmPassword")

        if password == password2:
            if User.objects.filter(username=username).exists():
                return Response(
                    {"error": "Username exists. Choose another"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif User.objects.filter(email=email).exists():
                return Response(
                    {"error": "Email registered. Log in"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name or "",
                    last_name=last_name or "",
                    email=email,
                    password=password,
                )
                Token.objects.create(user=user)
                UserProfile.objects.create(user=user)
                return Response(
                    {"success": "You have successfully registered!"},
                    status=status.HTTP_201_CREATED,
                )
        else:
            return Response(
                {"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST
            )


# Check username availability
@api_view(["POST"])
def check_availability(request):
    username = request.data.get("username")
    email = request.data.get("email")
    data = {
        "usernameAvailable": not User.objects.filter(username=username).exists(),
        "emailAvailable": not User.objects.filter(email=email).exists(),
    }

    return Response(data)


# create the posts
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def post_list_create(request):
    if request.method == "GET":
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Moments Comments & Likes
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def moments_create(request):
    if request.method == "GET":
        events = TimelineEvent.objects.all()
        serializer = TimelineEventSerializer(
            events, many=True, context={"request": request}
        )
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = TimelineEventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def timeline_event_detail(request, pk):
    try:
        event = TimelineEvent.objects.get(pk=pk, user=request.user)
    except TimelineEvent.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = TimelineEventSerializer(event)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = TimelineEventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_comment(request, event_id):
    print("Received Data", request.data)
    try:
        timeline_event = TimelineEvent.objects.get(pk=event_id)
    except TimelineEvent.DoesNotExist:
        return Response(
            {"message": "Moment not found."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = CommentSerializer(data=request.data, context={"request": request})

    print("Received Data", request.data)
    if serializer.is_valid():
        serializer.save(timeline_event=timeline_event, author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def handle_like(request, event_id):
    try:
        event = TimelineEvent.objects.get(pk=event_id)
    except TimelineEvent.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    event.like = request.data.get("liked", False)
    event.save()
    return Response({"status": "like updated"})


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def upload_avatar(request):
    user_profile = UserProfile.objects.get(user=request.user)
    serializer = UserProfileSerializer(user_profile, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_user_profile(request, user_id):
    users = {
        1: {
            "name": "Bob Marley",
            "avatar": "/media/avatars/bobmarley.jpg",
            "followerCount": 7900000,
            "communities": [],
            "bio": "Robert Nesta Marley OM, baptised Berhane Selassie, was a Jamaican singer, musician, and songwriter. Considered one of the pioneers of reggae, his musical career was marked by fusing elements of reggae, ska, and rocksteady, as well as his distinctive vocal and songwriting style.",
        },
        2: {
            "name": "Britney Spears",
            "avatar": "/media/avatars/britneyspears.webp",
            "followerCount": 42700000,
            "communities": ["Dog Training", "Tech Talk"],
            "bio": "Britney Jean Spears is an American singer. She is credited with influencing the revival of teen pop during the late 1990s and early 2000s. Spears has sold over 150 million records worldwide, making her one of the world's best-selling music artists.",
        },
        3: {
            "name": "Wayne Rooney",
            "avatar": "/media/avatars/waynerooney.jpg",
            "followerCount": 16300000,
            "communities": ["Dog Training"],
            "bio": "Wayne Mark Rooney is an English professional football manager and former player who is the manager of EFL Championship club Birmingham City.",
        },
    }
    user_data = users.get(user_id)
    if user_data:
        return Response(user_data)
    else:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_suggested_users(request):
    suggested_users = [
        {
            "id": 1,
            "name": "Bob Marley",
            "avatar": "/media/avatars/bobmarley.jpg",
            "followerCount": 7900000,
            "communities": [],
            "bio": "Robert Nesta Marley OM, baptised Berhane Selassie, was a Jamaican singer, musician, and songwriter. Considered one of the pioneers of reggae, his musical career was marked by fusing elements of reggae, ska, and rocksteady, as well as his distinctive vocal and songwriting style.",
        },
        {
            "id": 2,
            "name": "Britney Spears",
            "avatar": "/media/avatars/britneyspears.webp",
            "followerCount": 42700000,
            "communities": ["Dog Training", "Tech Talk"],
            "bio": "Britney Jean Spears is an American singer. She is credited with influencing the revival of teen pop during the late 1990s and early 2000s. Spears has sold over 150 million records worldwide, making her one of the world's best-selling music artists.",
        },
        {
            "id": 3,
            "name": "Wayne Rooney",
            "avatar": "/media/avatars/waynerooney.jpg",
            "followerCount": 16300000,
            "communities": ["Dog Training"],
            "bio": "Wayne Mark Rooney is an English professional football manager and former player who is the manager of EFL Championship club Birmingham City.",
        },
    ]
    return Response(suggested_users)
