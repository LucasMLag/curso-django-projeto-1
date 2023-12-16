from .test_base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest


@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def get_register_form(self):
        form = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )
        return form

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_register_form()

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('test@email.com')

        callback(form)
        return form

    def test_empty_first_name_error_message(self):

        def callback(form):
            first_name_field = self.get_by_placeholder(form, 'Ex.: John')
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)

            # Form has to be resselected after refresh
            form = self.get_register_form()

            self.assertIn('This field is required.', form.text)

        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):

        def callback(form):
            last_name_field = self.get_by_placeholder(form, 'Ex.: Doe')
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)

            # Form has to be resselected after refresh
            form = self.get_register_form()

            self.assertIn('This field is required.', form.text)

        self.form_field_test_with_callback(callback)

    def test_empty_user_name_error_message(self):

        def callback(form):
            username_field = self.get_by_placeholder(form, 'Your username')
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)

            # Form has to be resselected after refresh
            form = self.get_register_form()

            self.assertIn('This field is required.', form.text)

        self.form_field_test_with_callback(callback)

    # This function is completely wrong, thanks to Luiz Otavio Miranda!
    def test_invalid_email_error_message(self):

        def callback(form):
            email_field = self.get_by_placeholder(form, 'Your e-mail')
            email_field.send_keys('email@invalid')  # Here the second @ is passed to e-mail, generating an error pop-up and not the error message that he was looking for.
            email_field.send_keys(Keys.ENTER)

            # Form has to be resselected after refresh
            form = self.get_register_form()

            self.assertIn('The e-mail must be valid.', form.text)  # And here he decides he would check for the Help Text instead of the Invalid Error message, the cherry on the top of this great test

        self.form_field_test_with_callback(callback)  # Here one @ is passed to e-mail.

    def test_passwords_do_not_match_message(self):

        def callback(form):
            password = self.get_by_placeholder(form, 'Your password')
            password2 = self.get_by_placeholder(form, 'Repeat your password')
            password.send_keys('P@ssw0rd')
            password2.send_keys('P@ssw0rd_Different')
            password2.send_keys(Keys.ENTER)

            # Form has to be resselected after refresh
            form = self.get_register_form()

            self.assertIn("Your password entries don't match.", form.text)

        self.form_field_test_with_callback(callback)

    def test_valid_user_data_register_sucess(self):

        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_register_form()
        self.get_by_placeholder(form, 'Ex.: John').send_keys('First Name')
        self.get_by_placeholder(form, 'Ex.: Doe').send_keys('Last Name')
        self.get_by_placeholder(form, 'Your username').send_keys('UserName')
        self.get_by_placeholder(form, 'Your e-mail').send_keys('test@test.mail')
        self.get_by_placeholder(form, 'Your password').send_keys('P@ssw0rd')
        self.get_by_placeholder(form, 'Repeat your password').send_keys('P@ssw0rd')

        form.submit()

        self.assertIn(
            'Your sign-in was sucessful. Please log-in to your account.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
