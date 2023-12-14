from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe'),
        ('username', 'Your username'),
        ('email', 'Your e-mail'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder_is_correct(self, field, needed):
        form = RegisterForm()
        current = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current, needed)

    @parameterized.expand([
        # ('first_name', ''),
        # ('last_name', ''),
        ('username', 'Letters, numbers and @/./+/-/_ only.'),
        ('email', 'The e-mail must be valid.'),
        # ('password', ''),
        # ('password2', ''),
    ])
    def test_fields_help_text_is_correct(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand([
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Confirm Password'),
    ])
    def test_fields_label_is_correct(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs) -> None:
        self.form_data = {
            'username': 'User',
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'email@email.com',
            'password': 'Str0ngP@ssw0rd',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('first_name', 'This field is required.'),
        ('last_name', 'This field is required.'),
        ('username', 'This field is required.'),
        ('email', 'This field is required.'),
        ('password', 'This field is required.'),
        ('password2', 'This field is required.'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        # self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))
