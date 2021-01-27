from django.db import models

class GenericFileUpload(models.Model):
    file_upload = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_upload}"

class Message(models.Model):
    sender = models.ForeignKey('users.User', related_name='messages_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey('users.User', related_name='messages_received', on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return "message sent by %s to %s" % (self.sender, self.receiver)
    

class MessageAttachment(models.Model):
    message = models.ForeignKey(Message, related_name='attachments', on_delete=models.CASCADE)
    attachment = models.ForeignKey(GenericFileUpload, related_name='message_upload', on_delete=models.CASCADE)
    caption = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
    

