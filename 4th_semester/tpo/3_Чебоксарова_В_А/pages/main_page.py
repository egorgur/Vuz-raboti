from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
import time


class MainPage:
    BURGER_BUTTON = (By.CLASS_NAME, "j-menu-burger-btn")
    WOMEN_SECTION_LINK = (By.XPATH, "//a[@href='/catalog/zhenshchinam' and contains(@class, 'menu-burger__main-list-link')]")
    MENU_ITEM = (By.CLASS_NAME, "menu-burger__main-list-link")
    ADDRESSES_LINK = (By.CSS_SELECTOR, 'a.navbar-pc__link.j-wba-header-item[data-wba-header-name="Pick_up_points"]')
    CHAT_BUTTON = (By.CSS_SELECTOR, "button.fixed-block__chat.j-btn-chat-open.j-online-chat")
    CHAT_WINDOW = (By.CLASS_NAME, "chat__content")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.search-catalog__input")
    PRODUCT_PRICE = (By.CSS_SELECTOR, "ins.price__lower-price.wallet-price")
    ALL_FILTERS_BUTTON = (By.CSS_SELECTOR, "button.dropdown-filter__btn--all")
    MIN_PRICE_INPUT = (By.CSS_SELECTOR, "input.j-price[name='startN']")
    MAX_PRICE_INPUT = (By.CSS_SELECTOR, "input.j-price[name='endN']")
    APPLY_FILTERS_BUTTON = (By.CSS_SELECTOR, "button.filters-desktop__btn-main.btn-main")
    RATING_FILTER_TOGGLE = (By.CSS_SELECTOR, "div.filters-desktop__switch--frating button.btn-switch__btn")
    PRODUCT_RATING = (By.CSS_SELECTOR, "span.address-rate-mini.address-rate-mini--sm")
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".product-card")
    PRODUCT_NAME_LINK = (By.CSS_SELECTOR, "a.product-card__link")
    ADD_TO_BASKET_BUTTON = (By.CSS_SELECTOR, "a.product-card__add-basket.j-add-to-basket.btn-main")
    ACCEPT_COOKIES_BUTTON = (By.CSS_SELECTOR, "button.cookies__btn.btn-minor-md")
    PRODUCT_LINK = (By.CSS_SELECTOR, "a.product-card__link")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open_burger_menu(self):
        print("[INFO] Открываем бургер-меню")
        burger_button = self.wait.until(EC.element_to_be_clickable(self.BURGER_BUTTON))
        burger_button.click()
        self.wait.until(EC.visibility_of_element_located(self.MENU_ITEM))
        print("[INFO] Бургер-меню открыто")

    def go_to_women_section(self):
        print("[INFO] Переходим в раздел 'Женщинам'")
        women_link = self.wait.until(EC.element_to_be_clickable(self.WOMEN_SECTION_LINK))
        self.driver.execute_script("arguments[0].scrollIntoView();", women_link)
        women_link.click()
        print("[INFO] Перешли в раздел 'Женщинам'")

    def go_to_addresses(self):
        print("[INFO] Переходим в раздел 'Адреса'")
        addresses_link = self.wait.until(EC.element_to_be_clickable(self.ADDRESSES_LINK))
        addresses_link.click()
        print("[INFO] Перешли в раздел 'Адреса'")

    def open_chat(self):
        print("[INFO] Открываем окно поддержки")
        chat_button = self.wait.until(EC.element_to_be_clickable(self.CHAT_BUTTON))
        chat_button.click()
        self.wait.until(EC.visibility_of_element_located(self.CHAT_WINDOW))
        print("[INFO] Окно поддержки открыто")

    def search_product(self, product_name):
        print(f"[INFO] Выполняем поиск товара: {product_name}")
        search_input = self.wait.until(EC.element_to_be_clickable(self.SEARCH_INPUT))
        search_input.clear()
        search_input.send_keys(product_name)
        search_input.send_keys(Keys.RETURN)
        print("[INFO] Поиск выполнен")


    def open_all_filters(self):
        print("[INFO] Открываем фильтры")
        button = self.wait.until(EC.element_to_be_clickable(self.ALL_FILTERS_BUTTON))
        button.click()
        self.wait.until(EC.visibility_of_element_located(self.MIN_PRICE_INPUT))
        print("[INFO] Фильтры открыты")

    def set_price_filter(self, min_price=None, max_price=None):
        print("[INFO] Задаем минимальную и максимальную цену")
        if min_price is not None:
            min_input = self.wait.until(EC.element_to_be_clickable(self.MIN_PRICE_INPUT))
            min_input.clear()
            min_input.send_keys(str(min_price))
        if max_price is not None:
            max_input = self.wait.until(EC.element_to_be_clickable(self.MAX_PRICE_INPUT))
            max_input.clear()
            max_input.send_keys(str(max_price))
        print("[INFO] Минимальная и максимальная цены заданы")

    def apply_filters(self):
        apply_btn = self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON))
        apply_btn.click()
        self.wait.until(EC.invisibility_of_element_located(self.APPLY_FILTERS_BUTTON))
        print("[INFO] Нажата кнопка 'Применить фильтры'")

    def get_all_product_prices(self):
        prices = []
        product_cards = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-card"))
        )
        for card in product_cards:
            try:
                price_element = card.find_element(By.CSS_SELECTOR, 'ins[class*="price__lower-price"]')
                price_text = price_element.text.replace("\xa0", "").replace("₽", "").replace(" ", "")
                price = int(price_text)
                prices.append(price)
            except StaleElementReferenceException:
                continue
            except:
                continue
        return prices

    def enable_rating_filter(self):
        print("[INFO] Включаем фильтр по рейтингу")
        toggle = self.wait.until(EC.element_to_be_clickable(self.RATING_FILTER_TOGGLE))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", toggle)
        import time
        time.sleep(0.3)
        if "active" not in toggle.get_attribute("class"):
            toggle.click()
        print("[INFO] Фильтр по рейтингу включен")

    def get_all_product_ratings(self):
        ratings = []
        product_cards = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-card"))
        )
        for card in product_cards:
            try:
                rating_element = card.find_element(*self.PRODUCT_RATING)
                text = self.driver.execute_script("return arguments[0].textContent;", rating_element)
                text = text.replace(",", ".").strip()
                rating = float(text)
                ratings.append(rating)
            except StaleElementReferenceException:
                continue
            except:
                continue
        return ratings

    def accept_cookies(self):
        try:
            button = self.wait.until(EC.element_to_be_clickable(self.ACCEPT_COOKIES_BUTTON))
            self.driver.execute_script("arguments[0].click();", button)
        except TimeoutException:
            pass
        print("[INFO] Cookies приняты")

    def get_product_cards(self):
        return self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_CARDS))

    def get_product_name(self, product_card):
        link_element = product_card.find_element(*self.PRODUCT_NAME_LINK)
        aria_label = link_element.get_attribute("aria-label")
        if aria_label:
            return aria_label.strip()
        else:
            return link_element.text.strip()

    def add_product_to_basket(self, product_card):
        print("[INFO] Добавляем товар в корзину")
        add_button = product_card.find_element(*self.ADD_TO_BASKET_BUTTON)
        add_button.click()
        time.sleep(2)
        print("[INFO] Товар добавлен в корзину")

    def open_first_product_page(self):
        print("[INFO] Открываем страницу товара")
        product_cards = self.get_product_cards()
        first_product_link = product_cards[0].find_element(*self.PRODUCT_LINK)
        product_name = first_product_link.get_attribute("aria-label") or first_product_link.text
        first_product_link.click()
        print("[INFO] Страница товара открыта")
        return product_name.strip()
    