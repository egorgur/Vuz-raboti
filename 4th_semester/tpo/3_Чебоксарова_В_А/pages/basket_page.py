from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC


class BasketPage:
    BASKET_PRODUCT_NAMES = (By.CSS_SELECTOR, "span.good-info__good-name")
    DELETE_BUTTONS = (By.CSS_SELECTOR, "button.btn__del.j-basket-item-del")
    EMPTY_BASKET_TITLE = (By.CSS_SELECTOR, "h1.basket-empty__title.empty-page__title")
    COUNT_PLUS_BUTTONS = (By.CSS_SELECTOR, "button.count__plus.plus")
    COUNT_MINUS_BUTTONS = (By.CSS_SELECTOR, "button.count__minus.minus")
    QUANTITY_INPUTS = (By.CSS_SELECTOR, "input.count__numeric")
    TOTAL_SUM = (By.CSS_SELECTOR, "span[data-link*='calcTotalSum']")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def get_all_product_names(self):
        elements = self.wait.until(EC.presence_of_all_elements_located(self.BASKET_PRODUCT_NAMES))
        return [el.text.strip().lower() for el in elements]
    
    def delete_first_product(self):
        print("[INFO] Удаляем первый товар из корзины")
        delete_buttons = self.wait.until(EC.presence_of_all_elements_located(self.DELETE_BUTTONS))
        if delete_buttons:
            first_button = delete_buttons[0]
            product_container = first_button.find_element(By.XPATH, "./ancestor::div[contains(@class, 'accordion__list-item')]")
            first_button.click()
            self.wait.until(EC.staleness_of(product_container))
            time.sleep(2)
            print("[INFO] Товар удалён из корзины")

    def is_basket_empty(self):
        try:
            empty_title = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(self.EMPTY_BASKET_TITLE)
            )
            return "в корзине пока пусто" in empty_title.text.lower()
        except:
            return False
        
    def get_quantity_of_first_product(self):
        inputs = self.wait.until(EC.presence_of_all_elements_located(self.QUANTITY_INPUTS))
        return int(inputs[0].get_attribute("value"))

    def increase_quantity_of_first_product(self):
        print("[INFO] Увеличиваем количество первого товара в корзине")
        plus_buttons = self.wait.until(EC.presence_of_all_elements_located(self.COUNT_PLUS_BUTTONS))
        self.wait.until(EC.element_to_be_clickable(plus_buttons[0]))
        plus_buttons[0].click()
        self.wait.until(lambda d: int(d.find_elements(*self.QUANTITY_INPUTS)[0].get_attribute("value")) > 1)
        print("[INFO] Количество товара увеличено")

    def get_total_sum(self):
        total_element = self.wait.until(EC.visibility_of_element_located(self.TOTAL_SUM))
        text = total_element.text
        cleaned_text = text.replace('\xa0', '').replace(' ', '').replace('₽', '').strip()
        print(f"[INFO] Итоговая сумма корзины: {cleaned_text} ₽")
        return int(cleaned_text)
