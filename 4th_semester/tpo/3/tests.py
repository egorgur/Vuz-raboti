from pages import HomePage
import requests


def test_login(driver):
    homepage = HomePage(driver)
    homepage.login("admin", "admin")
    assert "?login=yes" in driver.current_url, "Login failed"


def test_navigation(driver):
    homepage = HomePage(driver)

    homepage.navigate_to_actions()
    assert "Акции" in driver.title, "Navigation failed"

    homepage.navigate_to_services()
    assert "Услуги" in driver.title, "Navigation failed"


def test_search(driver):
    homepage = HomePage(driver)

    homepage.search_product("divan")
    assert "divan" in driver.current_url, "Search failed"

    homepage.search_product("диван")
    homepage.sort_products_alphabetically()
    assert "sort_by=name&sort_order=desc" in driver.current_url, "Sorting failed"


def test_compare(driver):
    homepage = HomePage(driver)

    homepage.search_product("диван")
    homepage.add_product_to_compare()
    homepage.navigate_to_compare_page()
    assert homepage.compare_table.is_displayed(), "Product not added to compare"

    homepage.delete_product_from_compare()
    assert homepage.notetext.is_displayed(), "Product not deleted from compare"


def test_404_request():
    url = "https://krasdivan.shop/kaksdkasdk"
    response = requests.get(url)
    assert response.status_code == 404, "Bad response from server"
