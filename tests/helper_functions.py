import selenium
from selenium.webdriver.common.by import By

testuser_credentials = ['testuser', 'Tst123Tst!']

def login(selenium_driver):
    
    selenium_driver.get('http://127.0.0.1:8000/members/login_user')
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