from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:
    def __init__(self, driver):
        self.driver = driver

        self.log_in_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "auth-popup-btn.login-link.icon-custom"))
        )

    def login(self, number, password):
        self.log_in_button.click()

        self.number_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "USER_LOGIN"))
        )
        self.password_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "USER_PASSWORD"))
        )
        self.submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "Login"))
        )

        self.number_input.clear()
        self.number_input.send_keys(number)
        self.password_input.clear()
        self.password_input.send_keys(password)
        self.submit_button.click()


    def navigate_to_actions(self):
        self.actions_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Акции"))
        )
        self.actions_button.click()

    def navigate_to_services(self):
        self.services_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Услуги"))
        )
        self.services_button.click()

    def navigate_to_compare_page(self):
        self.compare_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "compare-link.icon-custom"))
        )
        self.compare_button.click()
        self.compare_table = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "compare-table"))
        )

    def search_product(self, product):
        self.search = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "title-search-input"))
        )
        self.search.clear()
        self.search.send_keys(product)
        self.search.submit()
        sleep(5)

    def sort_products_alphabetically(self):
        self.sort_by_alphabet = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "По алфавиту"))
        )
        self.sort_by_alphabet.click()

    def add_product_to_compare(self):
        self.add_to_compare_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "bx_3966226736_23852_7e1b8e3524755c391129a9d7e6f2d206_compare_link"))
        )
        self.add_to_compare_button.click()

    def delete_product_from_compare(self):
        self.delete_from_compare_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "close.icon-custom"))
        )
        self.delete_from_compare_button.click()
        self.notetext = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "notetext"))
        )
        
    def navigate_to_unknown_page(self, url):
        self.driver.get(url)