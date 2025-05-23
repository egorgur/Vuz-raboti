from pages.main_page import MainPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_go_to_women_section_from_burger_menu(driver):
    print("[TEST START] test_go_to_women_section_from_burger_menu")
    main_page = MainPage(driver)
    main_page.open_burger_menu()
    main_page.go_to_women_section()
    WebDriverWait(driver, 10).until(
        EC.url_contains("/catalog/zhenshchinam")
    )
    assert "/catalog/zhenshchinam" in driver.current_url, "Не удалось перейти в раздел 'Женщинам'"
    print("[TEST PASS] test_go_to_women_section_from_burger_menu")

def test_go_to_addresses_from_nav_panel(driver):
    print("[TEST START] test_go_to_addresses_from_nav_panel")
    main_page = MainPage(driver)
    main_page.go_to_addresses()
    WebDriverWait(driver, 10).until(
        EC.url_contains("/services/besplatnaya-dostavka")
    )
    assert "/services/besplatnaya-dostavka" in driver.current_url, "Не удалось перейти в раздел 'Адреса'"
    print("[TEST PASS] test_go_to_addresses_from_nav_panel")

def test_open_support_chat(driver):
    print("[TEST START] test_open_support_chat")
    main_page = MainPage(driver)
    main_page.open_chat()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(main_page.CHAT_WINDOW)
    )
    chat_window = driver.find_element(*main_page.CHAT_WINDOW)
    assert chat_window.is_displayed(), "Окно поддержки не открылось"
    print("[TEST PASS] test_open_support_chat")
