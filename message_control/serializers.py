from rest_framework import serializers
from .models import GenericFileUpload, Message, MessageAttachment

class GenericFileUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = GenericFileUpload
        fields = "__all__"


class MessageAttachmentSerializer(serializers.ModelSerializer):
    attachment = GenericFileUploadSerializer()

    class Meta:
        model = MessageAttachment
        fields = "__all__"


class MessageUserReferenceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(source="user_profile.first_name")
    last_name = serializers.CharField(source="user_profile.last_name")
    

class MessageSerializer(serializers.ModelSerializer):
    sender = MessageUserReferenceSerializer(read_only=True)
    sender_id = serializers.IntegerField(write_only=True)

    receiver = MessageUserReferenceSerializer(read_only=True)
    receiver_id = serializers.IntegerField(write_only=True)

    attachments = MessageAttachmentSerializer(read_only=True, many=True)
    class Meta:
        model = Message
        fields = "__all__"
