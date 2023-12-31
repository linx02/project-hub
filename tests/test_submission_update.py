from helper_functions import *

test_post_id = 42
submission_url = 'http://127.0.0.1:8000/project_submission/'
update_url = f'http://127.0.0.1:8000/project_update/{test_post_id}/'

def test_submission_invalid_github_link(selenium_driver):

    # Arrange
    login(selenium_driver)
    selenium_driver.get(submission_url)
    github_repo_link_input = selenium_driver.find_element(by=By.ID, value='github_repo_link')
    error_text_github = selenium_driver.find_element(by=By.ID, value='error-text-github')
    live_link_input = selenium_driver.find_element(by=By.ID, value='live-link')

    # Act
    github_repo_link_input.send_keys('Test')
    live_link_input.click()

    # Assert
    assert error_text_github.is_displayed()

def test_submission_no_title(selenium_driver):
    
    # Arrange
    submit_btn = selenium_driver.find_element(By.ID, value='submit-btn')

    # Act
    selenium_driver.execute_script("arguments[0].click();", submit_btn)

    # Assert
    assert submit_btn.is_displayed()

def test_update_invalid_github_link(selenium_driver):
    
    # Arrange
    selenium_driver.get(update_url)
    github_repo_link_input = selenium_driver.find_element(by=By.ID, value='github_repo_link')
    error_text_github = selenium_driver.find_element(by=By.ID, value='error-text-github')
    live_link_input = selenium_driver.find_element(by=By.ID, value='live-link')

    # Act
    github_repo_link_input.send_keys('Test')
    live_link_input.click()

    # Assert
    assert error_text_github.is_displayed()


def test_update_no_title(selenium_driver):
    
    # Arrange
    title_input = selenium_driver.find_element(by=By.ID, value='title')
    submit_btn = selenium_driver.find_element(By.ID, value='submit-btn')

    # Act
    title_input.clear()
    selenium_driver.execute_script("arguments[0].click();", submit_btn)
    
    # Assert
    assert submit_btn.is_displayed()