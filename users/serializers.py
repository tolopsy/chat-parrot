from rest_framework import serializers
from .models import User, UserProfile
from message_control.serializers import GenericFileUploadSerializer

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password", )


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    profile_picture = GenericFileUploadSerializer(read_only=True)
    profile_picture_id = serializers.IntegerField(write_only=True, required=False)
    message_count = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = UserProfile
        fields = "__all__"
