import pytest
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(os.getenv("BANK_URL", "http://localhost:8000"))
    driver.maximize_window()
    yield driver
    driver.quit()

def test_card_input_length(browser):
    card_input = browser.find_element(By.XPATH, '//input[@placeholder="0000 0000 0000 0000"]')
    card_input.clear()
    card_input.send_keys("1" * 20)
    assert len(card_input.get_attribute("value").replace(" ", "")) > 16

def test_card_input_letters_blocked(browser):
    card_input = browser.find_element(By.XPATH, '//input[@placeholder="0000 0000 0000 0000"]')
