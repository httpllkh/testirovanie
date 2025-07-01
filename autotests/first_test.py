import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


@pytest.fixture
def browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("http://localhost:8000")
    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()


def test_card_input_length(browser):
    card_input = browser.find_elements(By.CSS_SELECTOR, 'input[type="text"]')[0]
    card_input.clear()
    card_input.send_keys("1" * 20)
    assert len(card_input.get_attribute("value").replace(" ", "")) > 16


def test_card_input_letters_blocked(browser):
    card_input = browser.find_elements(By.CSS_SELECTOR, 'input[type="text"]')[0]
    card_input.clear()
    card_input.send_keys("abcdef")
    value = card_input.get_attribute("value")
    assert any(c.isalpha() for c in value)


def test_negative_amount_allowed(browser):
    amount_input = browser.find_element(By.ID, "placeholder")
    amount_input.clear()
    amount_input.send_keys("-1000")
    value = amount_input.get_attribute("value")
    assert "-" in value


def test_currency_blocks_present(browser):
    page_source = browser.page_source
    assert "Рубли" in page_source
    assert "Доллары" in page_source
    assert "Евро" in page_source


def test_transfer_with_zero_balance(browser):
    transfer_button = browser.find_element(By.XPATH, '//button[contains(text(), "Перевести")]')
    transfer_button.click()
    time.sleep(1)
    page_source = browser.page_source
    assert "ошибк" in page_source.lower() or "нельзя" in page_source.lower()
