import selenium
from selenium.webdriver.common.by import By
import random
import time

project_url = 'http://127.0.0.1:8000/project/testingpost/'
like_btn = None
testuser_credentials = ['testuser', 'Tst123Tst!']
random_comment = f'Testing comment: {random.randrange(10000)}'

def login(selenium_driver):
    
    selenium_driver.get('http://127.0.0.1:8000/members/login_user')
    username_input = selenium_driver.find_element(by=By.ID, value='username')
    password_input = selenium_driver.find_element(by=By.ID, value='password')

    username_input.send_keys(testuser_credentials[0])
    password_input.send_keys(testuser_credentials[1])

    login_button = selenium_driver.find_element(by=By.ID, value='login-submit')
    login_button.click()

def test_like(selenium_driver):
    login(selenium_driver)
    selenium_driver.get(project_url)
    number_of_likes = selenium_driver.find_element(by=By.ID, value='likes-number')
    number_of_likes_int = int(number_of_likes.get_attribute('innerHTML'))
    like_btn = selenium_driver.find_element(by=By.ID, value='like')
    like_btn.click()

    number_of_likes_new = selenium_driver.find_element(by=By.ID, value='likes-number')
    number_of_likes_int_new = int(number_of_likes_new.get_attribute('innerHTML'))

    assert number_of_likes_int < number_of_likes_int_new

def test_unlike(selenium_driver):
    number_of_likes = selenium_driver.find_element(by=By.ID, value='likes-number')
    number_of_likes_int = int(number_of_likes.get_attribute('innerHTML'))
    like_btn = selenium_driver.find_element(by=By.ID, value='like')
    like_btn.click()

    number_of_likes_new = selenium_driver.find_element(by=By.ID, value='likes-number')
    number_of_likes_int_new = int(number_of_likes_new.get_attribute('innerHTML'))

    assert number_of_likes_int > number_of_likes_int_new


def test_comment(selenium_driver):
    # Arrange
    comment_input = selenium_driver.find_element(by=By.ID, value='comment-input')
    comment_button = selenium_driver.find_element(by=By.ID, value='comment-btn')
    # Act
    comment_input.send_keys(random_comment)
    selenium_driver.execute_script("arguments[0].click();", comment_button)
    # Assert
    p_elements = selenium_driver.find_elements(by=By.TAG_NAME, value='p')
    p_elements_content = []
    for p in p_elements:
        p_elements_content.append(p.get_attribute('innerHTML'))

    assert random_comment in p_elements_content


def test_delete_comment(selenium_driver):
    # Arrange
    delete_comment_button = selenium_driver.find_element(by=By.CLASS_NAME, value='delete-comment-btn')
    delete_comment_confirm_button = selenium_driver.find_element(by=By.CLASS_NAME, value='btn-danger')

    # Act
    selenium_driver.execute_script("arguments[0].click();", delete_comment_button)
    selenium_driver.execute_script("arguments[0].click();", delete_comment_confirm_button)

    # Assert
    p_elements = selenium_driver.find_elements(by=By.TAG_NAME, value='p')
    p_elements_content = []
    for p in p_elements:
        p_elements_content.append(p.get_attribute('innerHTML'))

    assert random_comment not in p_elements_content


def test_empty_comment(selenium_driver):
    # Arrange
    comment_button = selenium_driver.find_element(by=By.ID, value='comment-btn')
    p_elements_length = len(selenium_driver.find_elements(by=By.TAG_NAME, value='p'))

    # Act
    selenium_driver.execute_script("arguments[0].click();", comment_button)
    time.sleep(3)

    # Assert
    p_elements_length_new = len(selenium_driver.find_elements(by=By.TAG_NAME, value='p'))

    assert p_elements_length == p_elements_length_new