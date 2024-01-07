from collections import defaultdict
from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr
from django.core.exceptions import ValidationError
from authors.validators import AuthorRecipeValidator


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

        # add_attr(self.fields.get('cover'), 'class', 'span-2')
        # Can't add it here as it would overwrite the widgets in Meta

    class Meta:
        model = Recipe

        fields = 'title', 'description', 'preparation_time', 'preparation_time_unit', 'servings', 'servings_unit', 'preparation_steps', 'cover'

        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    # ('VALOR', 'DISPLAY'),
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    # ('VALOR', 'DISPLAY'),
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            ),
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        AuthorRecipeValidator(self.cleaned_data, ErrorClass=ValidationError)
        return super_clean
