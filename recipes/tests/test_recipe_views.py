from django.urls import reverse, resolve
from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):

    # home view

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

    # category view

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_status_code_404_if_not_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 10000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        # this test needs a recipe
        self.make_recipe()

        # gets content of the http response
        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')

        # checks if the recipe is in the content
        self.assertIn('Recipe Title', content)

    def test_recipe_category_template_doesnt_load_not_published_recipes(self):
        # this test needs a not published recipe
        recipe = self.make_recipe(is_published=False)

        # gets content of the http response
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.id})
        )

        # checks if the recipe is not loaded
        self.assertEqual(response.status_code, 404)

    # recipe view

    def test_recipe_recipe_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_recipe_view_returns_status_code_404_if_not_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 10000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_recipe_template_loads_the_correct_recipe(self):
        # this test needs a recipe
        self.make_recipe()

        # gets content of the http response
        response = self.client.get(reverse('recipes:recipe', args=(1,)))
        content = response.content.decode('utf-8')

        # checks if the recipe is in the content
        self.assertIn('Recipe Title', content)
