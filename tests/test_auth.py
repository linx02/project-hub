from helper_functions import *
import pytest
import os

base_url = "http://127.0.0.1:8000/"

urls = {
    'signup': f'{base_url}members/register_user',
    'login': f'{base_url}members/login_user',
    'logout': f'{base_url}members/logout_user',
    'submission': f'{base_url}project_submission/',
    'profile_page': f'{base_url}profile_page/',
}


@pytest.mark.skip
def test_create_new_user(selenium_driver):
    # Arrange
    selenium_driver.get(urls['signup'])
    username_input = selenium_driver.find_element(by=By.ID, value='id_username')
    password_input1 = selenium_driver.find_element(by=By.ID, value='id_password1')
    password_input2 = selenium_driver.find_element(by=By.ID, value='id_password2')

    # Act
    username_input.send_keys(testuser_credentials[0])
    password_input1.send_keys(testuser_credentials[1])
    password_input2.send_keys(testuser_credentials[1])

    signup_button = selenium_driver.find_element(by=By.ID, value='signup-submit')
    signup_button.click()

    # Assert
    assert redirect_home_confirm(selenium_driver)


def test_login_user(selenium_driver):
    # Arrange
    logout(selenium_driver)

    # Act
    login(selenium_driver)

    # Assert
    assert redirect_home_confirm(selenium_driver)


def test_access_when_logged_in(selenium_driver):
    # Arrange
    selenium_driver.get(urls['profile_page'])

    # Act
    try:
        profile_header = selenium_driver.find_element(by=By.ID, value='your-profile-header')
    except selenium.common.exceptions.NoSuchElementException:
        assert False

    # Arrange
    selenium_driver.get(urls['submission'])

    # Act
    try:
        submission_container = selenium_driver.find_element(by=By.ID, value='project_submission_container')
    except selenium.common.exceptions.NoSuchElementException:
        assert False

    # Assert
    assert bool(profile_header) and bool(submission_container)
