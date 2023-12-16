from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class AuthorLogoutTest(TestCase):
    def test_user_tries_to_logout_using_get_method(self):
        User.objects.create_user(username='user', password='pass')
        self.client.login(username='user', password='pass')

        response = self.client.get(reverse('authors:logout'), follow=True)

        self.assertIn(
            'Invalid logout request.',
            response.content.decode('utf-8')
        )

    def test_user_tries_to_logout_as_another_user(self):
        User.objects.create_user(username='user', password='pass')
        self.client.login(username='user', password='pass')

        response = self.client.post(
            reverse('authors:logout'),
            data={
                'username': 'other_user'
            },
            follow=True
        )

        self.assertIn(
            'Invalid logout user.',
            response.content.decode('utf-8')
        )

    def test_user_can_loggout_sucessfully(self):
        User.objects.create_user(username='user', password='pass')
        self.client.login(username='user', password='pass')

        response = self.client.post(
            reverse('authors:logout'),
            data={
                'username': 'user'
            },
            follow=True
        )

        self.assertIn(
            'Logged out sucessfully.',
            response.content.decode('utf-8')
        )
