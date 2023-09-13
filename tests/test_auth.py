import selenium
from selenium.webdriver.common.by import By

base_url = 'http://127.0.0.1:8000/'
testuser_credentials = ['testuser', 'Tst123Tst!']

urls = {
    'signup' : f'{base_url}members/register_user',
    'login' : f'{base_url}members/login_user',
    'logout' : f'{base_url}members/logout_user',
    'submission' : f'{base_url}project_submission/',
    'profile_page' : f'{base_url}profile_page/',
}

def login(selenium_driver):
    
    selenium_driver.get(urls['login'])
    username_input = selenium_driver.find_element(by=By.ID, value='username')
    password_input = selenium_driver.find_element(by=By.ID, value='password')

    username_input.send_keys(testuser_credentials[0])
    password_input.send_keys(testuser_credentials[1])

    login_button = selenium_driver.find_element(by=By.ID, value='login-submit')
    login_button.click()

def logout(selenium_driver):
    try:
        logout_button = selenium_driver.find_element(by=By.LINK_TEXT, value='Logout')
        logout_button.click()
    except selenium.common.exceptions.NoSuchElementException:
        return

def redirect_home_confirm(selenium_driver):
    try:
        selenium_driver.find_element(by=By.ID, value='hero-svg')
        return True
    except selenium.common.exceptions.NoSuchElementException:
        return False

def test_create_new_user(selenium_driver):
    
    selenium_driver.get(urls['signup'])
    username_input = selenium_driver.find_element(by=By.ID, value='id_username')
    password_input1 = selenium_driver.find_element(by=By.ID, value='id_password1')
    password_input2 = selenium_driver.find_element(by=By.ID, value='id_password2')

    username_input.send_keys(testuser_credentials[0])
    password_input1.send_keys(testuser_credentials[1])
    password_input2.send_keys(testuser_credentials[1])

    signup_button = selenium_driver.find_element(by=By.ID, value='signup-submit')
    signup_button.click()

def test_login_user(selenium_driver):
    
    logout(selenium_driver)
    login(selenium_driver)

    assert redirect_home_confirm(selenium_driver)

def test_access_when_logged_in(selenium_driver):
    
    selenium_driver.get(urls['profile_page'])

    try:
        profile_header = selenium_driver.find_element(by=By.ID, value='your-profile-header')
    except selenium.common.exceptions.NoSuchElementException:
        assert False

    selenium_driver.get(urls['submission'])

    try:
        submission_container = selenium_driver.find_element(by=By.ID, value='project_submission_container')
    except selenium.common.exceptions.NoSuchElementException:
        assert False

    assert bool(profile_header) and bool(submission_container)