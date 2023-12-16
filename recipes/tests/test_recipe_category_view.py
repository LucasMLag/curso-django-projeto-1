from django.urls import reverse, resolve
from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeCategoryViewTests(RecipeTestBase):

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

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
            reverse('recipes:recipe', kwargs={'pk': recipe.id})
        )

        # checks if the recipe is not loaded
        self.assertEqual(response.status_code, 404)
