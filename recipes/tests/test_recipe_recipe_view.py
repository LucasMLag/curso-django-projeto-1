from django.urls import reverse, resolve
from recipes.views import site
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeRecipeViewTests(RecipeTestBase):

    def test_recipe_recipe_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'pk': 1}))
        self.assertIs(view.func.view_class, site.RecipeDetail)

    def test_recipe_recipe_view_returns_status_code_404_if_not_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': 10000})
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
