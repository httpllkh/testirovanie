from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_card_input_length(browser):
    card_input = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="0000 0000 0000 0000"]'))
    )
    card_input.clear()
    card_input.send_keys("1" * 20)
    assert len(card_input.get_attribute("value").replace(" ", "")) > 16

def test_card_input_letters_blocked(browser):
    card_input = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="0000 0000 0000 0000"]'))
    )
    card_input.clear()
    card_input.send_keys("abcdef")
    value = card_input.get_attribute("value")
    assert any(c.isalpha() for c in value)

def test_negative_amount_allowed(browser):
    amount_input = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.ID, "placeholder"))
    )
    amount_input.clear()
    amount_input.send_keys("-1000")
    value = amount_input.get_attribute("value")
    assert "-" in value
