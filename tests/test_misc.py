from helper_functions import *

base_url = "http://127.0.0.1:8000/"
urls = {
    'login' : f'{base_url}members/login_user',
    'signup' : f'{base_url}members/register_user'
}

def test_access_signup_page_logged_in(selenium_driver):
    # Arrange
    login(selenium_driver)

    # Act
    selenium_driver.get(urls['signup'])

    # Assert
    assert redirect_home_confirm(selenium_driver)


def test_access_login_page_logged_in(selenium_driver):
    # Act
    selenium_driver.get(urls['login'])

    # Assert
    assert redirect_home_confirm(selenium_driver)