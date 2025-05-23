from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProductPage:
    ADD_TO_BASKET_BUTTON = (By.CSS_SELECTOR, "button.order__button.btn-main")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def add_to_basket(self):
        print("[INFO] Добавляем товар в корзину со страницы товара")
        add_button = self.wait.until(EC.element_to_be_clickable(self.ADD_TO_BASKET_BUTTON))
        add_button.click()
        time.sleep(2)
        print("[INFO] Товар добавлен в корзину со страницы товара")
        