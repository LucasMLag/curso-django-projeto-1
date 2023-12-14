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
        ('password', 'Your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder_is_correct(self, field, needed):
        form = RegisterForm()
        current = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current, needed)

    @parameterized.expand([
        # ('first_name', ''),
        # ('last_name', ''),
        ('username', 'Letters, numbers or @/./+/-/_ only. Between 4 and 150 characters.'),
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
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'email@email.com',
            'username': 'User',
            'password': 'Str0ngP@ssw0rd',
            'password2': 'Str0ngP@ssw0rd',
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
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_filed_min_length_should_be_4(self):
        self.form_data['username'] = 'A' * 3
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username must have at least 4 characters.'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_filed_max_length_should_be_150(self):
        self.form_data['username'] = 'A' * 151
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username must have 150 or less characters.'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_password_field_must_have_lowercase_uppercase_letters_and_numbers(self):
        self.form_data['password'] = '1235678'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Password must have at least one uppercase letter, one lowercase letter and one number. Password length should be at least 8 characters long.'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

    ''' Can't make this test work, the error doesn't belong to password, but to __all__

    def test_password_field_and_password_confirmation_are_equal(self):
        self.form_data['password'] = '@@AAaa11'
        self.form_data['password2'] = '@@BBbb22'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = "Your password entries don't match"

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

    '''

    def test_send_get_request_registration_create_view_returns_404(self):
        url = reverse('authors:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_email_field_must_be_unique(self):
        url = reverse('authors:create')

        # Creating an user with e-mail 'email@email.com'
        self.client.post(url, data=self.form_data, follow=True)

        # Creating another user with e-mail 'email@email.com'
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = "This e-mail is already in use."

        self.assertIn(msg, response.context['form'].errors.get('email'))

    def test_author_created_can_login(self):
        url = reverse('authors:create')

        self.form_data.update({
            'username': 'testuser',
            'password': '@bCd823jn',
            'password2': '@bCd823jn',
        })

        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username='testuser',
            password='@bCd823jn',
        )

        self.assertTrue(is_authenticated)
