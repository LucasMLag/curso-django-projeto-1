import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# This method can change the widget atributes of the field without overwritting it
def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


# This method can change the widget 'placeholder' atribute of the field without overwritting it
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

    # Fields inside of the meta class would be overwritten by the ones outside
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your Password'
        }),
        error_messages={
            'required': 'Password is required'
        },
        # help_text=('Password must have at least one uppercase letter, one lowercase letter and one number. The length should be at least 8 characters.'),
        validators=[strong_password]
    )

    # Fields inside of the meta class would be overwritten by the ones outside
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password',
        })
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

        # selects all model fields, but excludes the listed ones
        # excludes = ['first_name']

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email': 'E-mail',
            'password': 'Password',
        }

        help_texts = {
            'email': 'The e-mail must be valid.',
            'username': ' Letters, numbers and @/./+/-/_ only.',
        }

        error_messages = {
            'email': {
                'invalid': 'This email is not valid.',
            },
            'password': {
                'required': 'This field must not be empty.',
            },
            'username': {
                'required': 'This field must not be empty.',
                'max_length': 'Username is too long. 150 characters is the limit.'
            },
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Username',
                'class': 'input text-input'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Your Password',
            }),
        }

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

        if username in password:
            raise ValidationError({
                'password': ValidationError(
                    'Your password must not contain your username.',
                    code='invalid',
                ),

            })
