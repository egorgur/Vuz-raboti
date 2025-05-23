from pages.main_page import MainPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def test_successful_search_existing_product(driver):
    print("[TEST START] test_successful_search_existing_product")
    main_page = MainPage(driver)
    main_page.search_product("ноутбук")

    WebDriverWait(driver, 10).until(
        EC.url_contains("catalog")
    )

    product_cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-card"))
    )
    assert len(product_cards) > 0, "Товары не найдены на странице результатов поиска"

    aria_labels = []
    for card in product_cards:
        try:
            link_element = card.find_element(By.CSS_SELECTOR, "a.product-card__link")
            aria_label = link_element.get_attribute("aria-label").lower()
            aria_labels.append(aria_label)
        except:
            continue

    assert any("ноутбук" in label for label in aria_labels), \
        "В названиях товаров не найдено слово 'ноутбук'"
    
    print("[TEST PASS] test_successful_search_existing_product")

def test_search_nonexistent_product(driver):
    print("[TEST START] test_search_nonexistent_product")
    main_page = MainPage(driver)
    main_page.search_product("  ")  

    not_found_title = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.content404__title"))
    )
    assert "ничего не найдено" in not_found_title.text.lower(), \
        "Сообщение о ненайденном товаре не появилось"
    
    print("[TEST PASS] test_search_nonexistent_product")
    
def test_filter_products_by_price_range(driver):
    print("[TEST START] test_filter_products_by_price_range")
    main_page = MainPage(driver)
    main_page.search_product("ноутбук")

    WebDriverWait(driver, 10).until(EC.url_contains("catalog"))

    main_page.open_all_filters()

    min_price = 20000
    max_price = 50000
    main_page.set_price_filter(min_price=min_price, max_price=max_price)

    main_page.apply_filters()

    prices = main_page.get_all_product_prices()

    assert len(prices) > 0, "После фильтрации товары не найдены"
    assert all(min_price <= price <= max_price for price in prices), \
        f"Найдены товары с ценами вне диапазона {min_price}-{max_price}: {prices}"
    
    print("[TEST PASS] test_filter_products_by_price_range")

def test_filter_products_by_rating(driver):
    print("[TEST START] test_filter_products_by_rating")
    main_page = MainPage(driver)
    main_page.search_product("ноутбук")

    WebDriverWait(driver, 10).until(EC.url_contains("catalog"))

    main_page.open_all_filters()

    main_page.enable_rating_filter()

    main_page.apply_filters()

    ratings = main_page.get_all_product_ratings()

    assert len(ratings) > 0, "После фильтрации товары с рейтингом не найдены"
    assert all(r >= 4.7 for r in ratings), f"Найдены товары с рейтингом ниже 4.7: {ratings}"

    print("[TEST PASS] test_filter_products_by_rating")
