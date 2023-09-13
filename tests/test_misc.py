import selenium
from selenium.webdriver.common.by import By

base_url = "http://127.0.0.1:8000/"
urls = {
    'login' : f'{base_url}members/login_user',
    'signup' : f'{base_url}members/register_user'
}

testuser_credentials = ['testuser', 'Tst123Tst!']

def login(selenium_driver):
    
    selenium_driver.get(urls['login'])
    username_input = selenium_driver.find_element(by=By.ID, value='username')
    password_input = selenium_driver.find_element(by=By.ID, value='password')

    username_input.send_keys(testuser_credentials[0])
    password_input.send_keys(testuser_credentials[1])

    login_button = selenium_driver.find_element(by=By.ID, value='login-submit')
    login_button.click()


def redirect_home_confirm(selenium_driver):
    try:
        selenium_driver.find_element(by=By.ID, value='hero-svg')
        return True
    except selenium.common.exceptions.NoSuchElementException:
        return False

def test_access_signup_page_logged_in(selenium_driver):
    
    login(selenium_driver)
    selenium_driver.get(urls['signup'])
    assert redirect_home_confirm(selenium_driver)


def test_access_login_page_logged_in(selenium_driver):
    
    selenium_driver.get(urls['login'])
    assert redirect_home_confirm(selenium_driver)