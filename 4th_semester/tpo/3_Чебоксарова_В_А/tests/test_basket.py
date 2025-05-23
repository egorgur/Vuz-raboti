from pages.main_page import MainPage
from pages.product_page import ProductPage
from pages.basket_page import BasketPage


def test_add_product_to_basket_from_search(driver):
    print("[TEST START] test_add_product_to_basket_from_search")
    main_page = MainPage(driver)
    basket_page = BasketPage(driver)

    driver.get("https://www.wildberries.ru")

    main_page.accept_cookies()
    main_page.search_product("ноутбук")

    product_cards = main_page.get_product_cards()
    assert product_cards, "Товары не найдены после поиска"

    first_product = product_cards[0]
    product_name = main_page.get_product_name(first_product)

    main_page.add_product_to_basket(first_product)

    driver.get("https://www.wildberries.ru/lk/basket")

    basket_product_names = basket_page.get_all_product_names()

    assert any(product_name.lower()[:10] in name for name in basket_product_names), \
    f"Товар '{product_name}' не найден в корзине"

    print("[TEST PASS] test_add_product_to_basket_from_search")

def test_add_product_to_basket_from_product_page(driver):
    print("[TEST START] test_add_product_to_basket_from_product_page")
    main_page = MainPage(driver)
    product_page = ProductPage(driver)
    basket_page = BasketPage(driver)

    driver.get("https://www.wildberries.ru")

    main_page.accept_cookies()
    main_page.search_product("ноутбук")

    product_name = main_page.open_first_product_page()

    product_page.add_to_basket()

    driver.get("https://www.wildberries.ru/lk/basket")

    basket_product_names = basket_page.get_all_product_names()

    assert any(product_name.lower()[:10] in name for name in basket_product_names), \
    f"Товар '{product_name}' не найден в корзине"

    print("[TEST PASS] test_add_product_to_basket_from_product_page")

def test_delete_product_from_basket(driver):
    print("[TEST START] test_delete_product_from_basket")
    main_page = MainPage(driver)
    basket_page = BasketPage(driver)

    driver.get("https://www.wildberries.ru")

    main_page.accept_cookies()
    main_page.search_product("ноутбук")

    product_cards = main_page.get_product_cards()
    assert product_cards, "Товары не найдены после поиска"

    first_product = product_cards[0]
    main_page.add_product_to_basket(first_product)

    driver.get("https://www.wildberries.ru/lk/basket")

    basket_product_names = basket_page.get_all_product_names()
    assert basket_product_names, "Корзина пуста после добавления товара"

    basket_page.delete_first_product()

    assert basket_page.is_basket_empty(), "Товар не удалён из корзины"

    print("[TEST PASS] test_delete_product_from_basket")

def test_change_quantity_in_basket(driver):
    print("[TEST START] test_change_quantity_in_basket")
    main_page = MainPage(driver)
    basket_page = BasketPage(driver)

    driver.get("https://www.wildberries.ru")

    main_page.accept_cookies()
    main_page.search_product("ноутбук")

    product_cards = main_page.get_product_cards()
    assert product_cards, "Товары не найдены после поиска"

    first_product = product_cards[0]
    main_page.add_product_to_basket(first_product)

    driver.get("https://www.wildberries.ru/lk/basket")

    initial_quantity = basket_page.get_quantity_of_first_product()
    assert initial_quantity == 1, f"Начальное количество товара должно быть 1, но {initial_quantity}"

    initial_total = basket_page.get_total_sum()

    basket_page.increase_quantity_of_first_product()

    new_quantity = basket_page.get_quantity_of_first_product()
    assert new_quantity == initial_quantity + 1, f"Количество товара не увеличилось: ожидается {initial_quantity + 1}, получено {new_quantity}"

    new_total = basket_page.get_total_sum()
    assert new_total > initial_total, f"Итоговая сумма не увеличилась: было {initial_total}, стало {new_total}"

    print("[TEST PASS] test_change_quantity_in_basket")
