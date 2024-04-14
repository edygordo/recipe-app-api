from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    "A class to handle tests over Authenticatio user model"

    def test_create_user_with_email_successful(self):
        "Create a user and test it's in db"
        email = 'aditya@example.com'
        password = "changeme"
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(raw_password=password))

    def test_create_user_with_normalized_email_successful(self):
        "Create user who has a normalized email"
        emails = ['aditya1@Example.CoM','aditya2@examplE.COM', 'AdityA3@examPle.com', 'aditya_sahU.96@gMaiL.cOm']
        results= ['aditya1@example.com','aditya2@example.com', 'AdityA3@example.com', 'aditya_sahU.96@gmail.com']
        for index,email in enumerate(emails):
            user = get_user_model().objects.create_user(email=email)
            self.assertEqual(user.email,results[index])

    def test_invalid_email_throws_error(self):
        "A user should always have a valid email"
        
        emails = ['', ' ', 'aditya1@exam', 'aditya@#$^gmail.com','ad@gmail@com', 'a`~d@gmail.com',
                  'a%d@gmail.com']

        for email in emails:
            with self.assertRaises(ValueError):
                user = get_user_model().objects.create_user(email=email)

    def test_creating_superuser(self):
        "Test a super user creation"

        email = 'aditya@example.com'
        password = 'test123'

        user = get_user_model().objects.create_superuser(email=email, password=password)

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
