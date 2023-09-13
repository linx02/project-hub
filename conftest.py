import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

@pytest.fixture(scope="module")
def selenium_driver():

    chrome_service = ChromeService(executable_path="./chromedriver")
    driver = webdriver.Chrome(service=chrome_service)

    driver.implicitly_wait(10)

    yield driver

    driver.quit()
