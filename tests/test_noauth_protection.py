import selenium
from selenium.webdriver.common.by import By

base_url = "http://127.0.0.1:8000/"
test_post_id = 14
test_post_slug = 'testingpost'
test_post_comment = 12
urls = {
    'project_details' : f'{base_url}project/{test_post_slug}/',
    'submission' : f'{base_url}project_submission/',
    'profile_page' : f'{base_url}profile_page/',
    'delete_post' : f'{base_url}delete_post/{test_post_id}/',
    'update' : f'{base_url}project_update/{test_post_id}/',
    'comment' : f'{base_url}post_comment/{test_post_id}/',
    'delete_comment' : f'{base_url}delete_comment/{test_post_comment}/{test_post_id}/',
    'browse_project' : '{base_url}browse_project/<int:pp>/<str:sort_by>/',
    'like' : f'{base_url}like_post/{test_post_id}/',
    'profile' : f'{base_url}profile/linx/',
}

def redirect_home_confirm(selenium_driver):
    try:
        selenium_driver.find_element(by=By.ID, value='hero-svg')
        return True
    except selenium.common.exceptions.NoSuchElementException:
        return False

def test_noauth_like(selenium_driver):
    # Act
    selenium_driver.get(urls['like'])

    # Assert
    assert redirect_home_confirm(selenium_driver)


def test_noauth_comment(selenium_driver):
    # Act
    selenium_driver.get(urls['comment'])

    # Assert
    assert redirect_home_confirm(selenium_driver)


def test_noauth_delete_comment(selenium_driver):
    # Act
    selenium_driver.get(urls['delete_comment'])

    # Assert
    assert redirect_home_confirm(selenium_driver)

def test_noauth_project_submission(selenium_driver):
    # Act
    selenium_driver.get(urls['submission'])

    # Assert
    assert redirect_home_confirm(selenium_driver)


def test_noath_project_update(selenium_driver):
    # Act
    selenium_driver.get(urls['update'])

    # Assert
    assert redirect_home_confirm(selenium_driver)


def test_noauth_project_delete(selenium_driver):
    # Act
    selenium_driver.get(urls['delete_post'])

    # Assert
    assert redirect_home_confirm(selenium_driver)


def test_noauth_access_profile_page(selenium_driver):
    # Act
    selenium_driver.get(urls['profile_page'])

    # Assert
    assert redirect_home_confirm(selenium_driver)