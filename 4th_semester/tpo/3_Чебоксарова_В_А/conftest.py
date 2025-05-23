import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path

@pytest.fixture(scope="function")
def driver():
    service = Service(executable_path=binary_path)
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.wildberries.ru/")
    yield driver
    driver.quit()
