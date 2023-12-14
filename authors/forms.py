import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# This method can change the widget atributes of the field without overwritting
def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


# This method can change the widget 'placeholder' atribute of the field without overwritting
def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(
            'Password must have at least one uppercase letter, one lowercase letter and one number. Password length should be at least 8 characters long.',
            code='invalid'
        )


class RegisterForm(forms.ModelForm):

    # __init__ is used to call the method to change placeholders
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_placeholder(self.fields['password'], 'Type your password')
        add_placeholder(self.fields['password2'], 'Repeat your password')

    # Fields inside of the meta class would be overwritten by the ones outside

    first_name = forms.CharField(
        label='First Name',
        # required=True,          # this is not needed, as it is default
        error_messages={
            'required': 'This field is required.'
        },
    )

    last_name = forms.CharField(
        label='Last Name',
        error_messages={
            'required': 'This field is required.'
        },
    )

    username = forms.CharField(
        label='Username',
        error_messages={
            'required': 'This field is required.'
        },
        help_text=('Letters, numbers and @/./+/-/_ only.'),
    )

    email = forms.EmailField(
        label='E-mail',
        error_messages={
            'required': 'This field is required.'
        },
        help_text=('The e-mail must be valid.'),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Password',
        error_messages={
            'required': 'This field is required.'
        },
        validators=[strong_password],
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Confirm Password',
        error_messages={
            'required': 'This field is required.'
        },
    )

    class Meta:

        # selects the model for the form
        model = User

        # selects the model fields that will be used in the form
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        '''
        # selects all model fields, but excludes the listed ones
        # excludes = ['first_name']

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email': 'E-mail',
        }

        help_texts = {
            'email': 'The e-mail must be valid.',
            'username': 'Letters, numbers and @/./+/-/_ only.',
        }

        error_messages = {
            'username': {
                'max_length': 'Username is too long. 150 characters is the limit.',
            },
        }
        '''

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'abc123' in data:
            raise ValidationError(
                'Your password contains easy to guess patterns.',
                code='invalid',
            )

        return data

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        username = cleaned_data.get('username')

        if password != password2:
            raise ValidationError(
                'Your password entries don\'t match'
            )

        if password:
            if username in password:
                raise ValidationError({
                    'password': ValidationError(
                        'Your password must not contain your username.',
                        code='invalid',
                    ),
                })
