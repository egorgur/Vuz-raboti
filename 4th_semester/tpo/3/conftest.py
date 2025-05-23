import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions


@pytest.fixture(scope="function")
def driver():
    options = FirefoxOptions()
    service = Service(executable_path="./geckodriver")
    driver = webdriver.Firefox(service=service, options=options)
    driver.get("https://krasdivan.shop/")
    yield driver
    driver.quit()
