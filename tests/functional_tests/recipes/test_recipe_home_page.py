import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .test_base import RecipeBaseFunctionalTest
from unittest.mock import patch


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    def test_recipe_home_no_recipes_found_message_if_no_recipes_found(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found', body.text)

    @patch('recipes.views.site.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        # At least one recipe is needed for this test
        recipes = self.make_recipes(3)

        # User opens home page
        self.browser.get(self.live_server_url)

        # Sees a seach input with placeholder: "Search for a recipe..."
        search_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Search for a recipe..."]')

        # Clicks the button        This step is not needed
        # search_input.click()

        # Searches for the a recipe title
        search_input.send_keys(recipes[0].title)
        search_input.send_keys(Keys.ENTER)

        # Asserts if he found the recipe in the search result
        body = self.browser.find_element(By.CLASS_NAME, 'main-content-list')
        self.assertIn(recipes[0].title, body.text)

    @patch('recipes.views.site.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipes(3)

        # User opens home page
        self.browser.get(self.live_server_url)

        # Sees pagination and clicks on page 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page2.click()

        # Sees that there is one recipe on page 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            1,
        )
