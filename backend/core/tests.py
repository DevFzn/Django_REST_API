from . models import Contact
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status

class ContactTestCase(APITestCase):
    """
    Test suite para Contact
    """
    def setUp(self):
        self.client = APIClient()
        self.data = {
            "name": "DevFzn",
            "message": "Este es un mensaje de prueba",
            "email": "devfzn@test.com"
        }
        self.url = "/contact/"

    def test_create_contact(self):
        '''
        test ContactViewSet método create
        '''
        data = self.data
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Contact.objects.get().title, "DevFzn")

    def test_create_contact_without_name(self):
        '''
        test ContactViewSet método create cuando nombre no está en los datos
        '''
        data = self.data
        data.pop("name")
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_when_name_equals_blank(self):
        '''
        test ContactViewSet método create cuando nombre está en blanco
        '''
        data = self.data
        data["name"] = ""
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_without_message(self):
        '''
        test ContactViewSet método create cuando mensaje no está en los datos
        '''
        data = self.data
        data.pop("message")
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_when_message_equals_blank(self):
        '''
        test ContactViewSet método create cuando mensaje está en blanco
        '''
        data = self.data
        data["message"] = ""
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_without_email(self):
        '''
        test ContactViewSet método create cuando email no está en los datos
        '''
        data = self.data
        data.pop("email")
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_when_email_equals_blank(self):
        '''
        test ContactViewSet método create cuando email está en blanco
        '''
        data = self.data
        data["email"] = ""
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_when_email_equals_non_email(self):
        '''
        test ContactViewSet método create cuando email no es un email
        '''
        data = self.data
        data["email"] = "test"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

