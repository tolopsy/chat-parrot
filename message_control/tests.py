from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APITestCase
from six import BytesIO
from PIL import Image


def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='PNG'):
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)


class TestFileUpload(APITestCase):
    file_upload_url = '/message/file-upload'

    def test_file_upload(self):
        # definition

        avatar = create_image(None, 'avatar.png')
        avatar_file = SimpleUploadedFile("front.png", avatar.getvalue())
        data = {
            "file_upload": avatar_file
        }

        # processing
        response =  self.client.post(self.file_upload_url, data=data)
        result = response.json()

        # assertions
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['id'], 1)

class TestMessage(APITestCase):
    message_url = "/message/message"

    def setUp(self):
        from users.models import User, UserProfile

        # sender
        self.sender = User.objects._create_user(username='toluboy', password='toluboy')
        UserProfile.objects.create(user=self.sender, first_name='toluwaa', last_name='olanrewaju')

        # receiver
        self.receiver = User.objects._create_user(username='testman', password='test123')
        UserProfile.objects.create(user=self.receiver, first_name='john', last_name='doe')

        # authenticate
        self.client.force_authenticate(user=self.sender)
    
    def test_message(self):
        payload = {
            "sender_id": self.sender.id,
            "receiver_id": self.receiver.id,
            "message": "Test message",
        }

        response = self.client.post(self.message_url, data=payload)
        result = response.json()

        # assertions
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['message'], "Test message")
        self.assertEqual(result['sender']['user']['username'], 'toluboy')
        self.assertEqual(result['receiver']['user']['username'], 'testman')