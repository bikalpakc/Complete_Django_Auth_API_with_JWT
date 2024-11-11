from django.test import TestCase
from account.models import User

class UserModelTest(TestCase):
    def test_create_user(self):  #test_<method name>
        email='test@example.com'
        name='Bikalpa KC'
        password='testpassword'
        tc=True

        user=User.objects.create_user(email=email, password=password, name=name, tc=tc)

        self.assertEqual(user.email, email)
        self.assertEqual(user.name, name)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.tc)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        email='test@example.com'
        name='Bikalpa KC'
        password='testpassword'
        tc=True

        superuser=User.objects.create_superuser(email=email, password=password, name=name, tc=tc)

        self.assertEqual(superuser.email, email)
        self.assertEqual(superuser.name, name)
        self.assertTrue(superuser.check_password(password))
        self.assertTrue(superuser.tc)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.is_staff)
        

class User_Class_Methods_Test(TestCase):
    email='test@example.com'
    name='Bikalpa KC'

    def test_has_perm(self):
        user=User(email=self.email, name=self.name) 
        self.assertFalse(user.has_perm('some_permission'))  

    def test_has_module_perms(self):
        user=User(email=self.email, name=self.name) 
        self.assertTrue(user.has_module_perms('some_app'))       

    def test_is_staff(self):
        user=User(email=self.email, name=self.name) 
        self.assertFalse(user.is_staff )       