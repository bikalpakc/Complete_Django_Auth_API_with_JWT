from account.models import User
from rest_framework.test import APITestCase
from account.serializers import UserRegistrationSerializer
class UserSerializerTestCase(APITestCase):
    data={
            'email':'test@example.com',
            'name': 'Bikalpa KC',
            'password': 'testpassword',
            'password2': 'testpassword',
            'tc': 'True',
        }
    
    def test_user_serializer_valid_data(self):
        data={
            'email':'test@example.com',
            'name': 'Bikalpa KC',
            'password': 'testpassword',
            'password2': 'testpassword',
            'tc': 'True',
        }

        serializer=UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

    def test_user_serializer_password_mismatch(self):
        data={
            'email':'test@example.com',
            'name': 'Bikalpa KC',
            'password': 'testpassword',
            'password2': 'mismatch-password',
            'tc': 'True',
        }

        serializer=UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['non_field_errors'][0], "Password and Confirm Password doesn't match.")

    def test_user_serializer_duplicate_email(self):
        User.objects.create_user(email='test@example.com', password='testpassword', name='Bikalpa KC', tc=True)
        data=self.data
        serializer=UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue(serializer.errors)

    def test_user_registration_serialzier_create(self):
        data=self.data
        serializer=UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user=serializer.create(serializer.validated_data)
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.name, 'Bikalpa KC')
        self.assertTrue(user.is_active)
