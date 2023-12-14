from django.urls import reverse, resolve
from recipes import views
from unittest.mock import patch
from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTests(RecipeTestBase):

    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get((reverse('recipes:home')))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get((reverse('recipes:home')))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get((reverse('recipes:home')))
        self.assertIn(
            'No recipes found',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_doesnt_load_not_published_recipes(self):
        # this test needs a not published recipe
        self.make_recipe(is_published=False)

        # gets content of the http response
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')

        # checks if the recipe is not loaded
        self.assertIn(
            'No recipes found',
            content
        )

    def test_recipe_home_is_paginated(self):
        # this test needs multiple recipes
        for i in range(3):
            kwargs = {'author_data': {'username': f'u{i}'}, 'slug': f's{i}'}
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=2):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 2)
            self.assertEqual(len(paginator.get_page(1)), 2)
            self.assertEqual(len(paginator.get_page(2)), 1)

    def test_invalid_page_querry_uses_page_1(self):
        response = self.client.get(reverse('recipes:home') + '?page=A')
        self.assertEqual(response.context['recipes'].number, 1)
