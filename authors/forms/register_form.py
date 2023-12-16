from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import strong_password


class RegisterForm(forms.ModelForm):

    # Fields inside of the meta class would be overwritten by the ones outside

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex.: John',
        }),
        label='First Name',

        # required=True,          # this is not needed, as it is default
        error_messages={
            'required': 'This field is required.'
        },
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex.: Doe',
        }),
        label='Last Name',
        error_messages={
            'required': 'This field is required.'
        },
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Your username',
        }),
        label='Username',
        help_text=('Letters, numbers or @/./+/-/_ only. Between 4 and 150 characters.'),

        error_messages={
            'required': 'This field is required.',
            'min_length': 'Username must have at least 4 characters.',
            'max_length': 'Username must have 150 or less characters.'
        },
        min_length=4,
        max_length=150,
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Your e-mail',
        }),
        label='E-mail',
        help_text=('The e-mail must be valid.'),

        error_messages={
            'required': 'This field is required.',
            'invalid': 'Enter a valid e-mail.',
        },
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password',
        }),
        label='Password',

        error_messages={
            'required': 'This field is required.'
        },
        validators=[strong_password],
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password',
        }),
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

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if 'abc123' in password:
            raise ValidationError(
                'Your password contains easy to guess patterns.',
                code='invalid',
            )

        return password

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'This e-mail is already in use.',
                code='invalid',
            )

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        username = cleaned_data.get('username')

        if password != password2:
            raise ValidationError(
                "Your password entries don't match."
            )

        if username:
            if password:
                if username in password:
                    raise ValidationError({
                        'password': ValidationError(
                            'Your password must not contain your username.',
                            code='invalid',
                        ),
                    })
