from django.conf import settings
from django.contrib.auth import authenticate
from django.db.models import Q, Count, F

from rest_framework.views import APIView
from chat_parrot.custom_utils import CustomIsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

import jwt
from datetime import datetime, timedelta
import random
import string
import re

from .models import Jwt, UserProfile
from .models import User
from .serializers import (
    LoginSerializer, 
    RegisterSerializer, 
    RefreshSerializer,
    UserProfileSerializer,
)

from .authentication import Authentication



def get_random(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def get_access_token(payload):
    return jwt.encode(
        {"exp": datetime.now() + timedelta(minutes=5), **payload},
        settings.SECRET_KEY,
        algorithm="HS256"
    )


def get_refresh_token():
    return jwt.encode(
        {"exp": datetime.now() + timedelta(days=365), "data": get_random(10)},
        settings.SECRET_KEY,
        algorithm="HS256"
    )


def decode_jwt(token, key=settings.SECRET_KEY, algorithm="HS256"):
    return jwt.decode(token, key=key, algorithms=algorithm)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'])

        if not user:
            return Response({"error": "Invalid username or password"}, status="400")

        Jwt.objects.filter(user_id=user.id).delete()

        access = get_access_token({"user_id": user.id})
        refresh = get_refresh_token()

        Jwt.objects.create(
            user_id=user.id, access=access, refresh=refresh
        )

        return Response({"access": access, "refresh": refresh})


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        User.objects._create_user(**serializer.validated_data)

        return Response({"success": "User created."}, status=201)


class RefreshView(APIView):
    serializer_class = RefreshSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            active_jwt = Jwt.objects.get(
                refresh=serializer.validated_data["refresh"])
        except Jwt.DoesNotExist:
            return Response({"error": "refresh token not found"}, status="400")
        if not Authentication.verify_token(serializer.validated_data["refresh"]):
            return Response({"error": "Token is invalid or has expired"})

        access = get_access_token({"user_id": active_jwt.user.id})
        refresh = get_refresh_token()

        active_jwt.access = decode_jwt(access)
        active_jwt.refresh = decode_jwt(refresh)
        active_jwt.save()

        return Response({"access": access, "refresh": refresh})



class UserProfileView(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (CustomIsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        queryset = (
            self.queryset.select_related("user", "profile_picture")
            .prefetch_related("user__messages_sent", "user__messages_received")
            .annotate(
                messages_received_from=Count(
                    "user__messages_sent", filter=Q(
                        Q(user__messages_sent__receiver_id=user.id),
                        ~Q(user__messages_received__sender_id=user.id)  # to remove message to self
                    ),
                    distinct=True
                ),
                messages_sent_to=Count(
                    "user__messages_received", filter=Q(user__messages_received__sender_id=user.id),
                    distinct=True
                ),
                message_count=F("messages_sent_to") + F("messages_received_from"),
            )
        )

        keyword = self.request.query_params.get("keyword", None)

        if keyword:
            search_fields = ('user__username', 'first_name', 'last_name')
            query = self.get_query(keyword, search_fields)
            
            return queryset.filter(query).distinct()

        return queryset
    

    @staticmethod
    def get_query(query_string, search_fields):
        query = None  # Query to search for every search term
        terms = UserProfileView.normalize_query(query_string)
        for term in terms:
            or_query = None  # Query to search for a given term in each field
            for field_name in search_fields:
                q = Q(**{"%s__icontains" % field_name: term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query & or_query
        return query

    @staticmethod
    def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
        return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]