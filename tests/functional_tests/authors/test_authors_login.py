from .test_base import AuthorsBaseTest
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_valid_user_can_login_sucessfully(self):
        username = 'my_user'
        password = 'P@ssw0rd'
        user = User.objects.create_user(username=username, password=password)

        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        self.get_by_placeholder(form, 'Type your username').send_keys(username)
        self.get_by_placeholder(form, 'Type your password').send_keys(password)

        form.submit()

        self.assertIn(
            f'You are logged in as {user.username}.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_raises_404_if_request_not_POST_method(self):
        self.browser.get(self.live_server_url + reverse('authors:login_create'))

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_with_invalid_credentials(self):
        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        self.get_by_placeholder(form, 'Type your username').send_keys(' ')
        self.get_by_placeholder(form, 'Type your password').send_keys(' ')

        form.submit()

        self.assertIn(
            'Invalid credentials.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_with_wrong_username_or_password(self):
        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        self.get_by_placeholder(form, 'Type your username').send_keys('InvalidUser')
        self.get_by_placeholder(form, 'Type your password').send_keys('InvalidPassword')

        form.submit()

        self.assertIn(
            'Wrong username or password.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
