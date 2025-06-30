import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

@pytest.fixture
def driver():
    # Инициализация драйвера
    driver = webdriver.Chrome()  # Убедитесь, что chromedriver в PATH
    driver.implicitly_wait(2)    # Неявное ожидание элементов
    yield driver
    # Завершение работы
    driver.quit()

def test_letters_in_url_balance(driver):
    """Тест для проверки ввода букв в URL параметр balance"""
    # 1. Открываем страницу с буквенным значением в balance
    test_letter = "a"  # Можно изменить на любой другой символ
    driver.get(f"http://localhost:8000/?balance={test_letter}")
    
    # 2. Проверяем отображение баланса
    try:
        balance_display = driver.find_element(By.ID, "balance-display")  # Измените локатор под ваш интерфейс
        assert "NaN" not in balance_display.text, \
            f"При вводе '{test_letter}' в URL отображается NaN вместо игнорирования символа"
    except NoSuchElementException:
        pytest.fail("Элемент для отображения баланса не найден")

def test_decimal_separators_in_transfer_amount(driver):
    """Тест для проверки ввода точки/запятой в поле суммы перевода"""
    # 1. Открываем страницу
    driver.get("http://localhost:8000/")
    
    # 2. Находим поле для ввода суммы перевода
    try:
        amount_input = driver.find_element(By.NAME, "transfer-amount")  # Измените локатор под ваш интерфейс
    except NoSuchElementException:
        pytest.fail("Поле для ввода суммы перевода не найдено")
    
    # 3. Проверяем точку как разделитель
    test_amount = "100.50"
    amount_input.clear()
    amount_input.send_keys(test_amount)
    
    # Проверяем, что значение сохранилось с точкой
    assert amount_input.get_attribute("value") == test_amount, \
        f"Точка как разделитель не работает. Ожидалось: {test_amount}"
    
    # 4. Проверяем запятую как разделитель
    test_amount = "200,75"
    amount_input.clear()
    amount_input.send_keys(test_amount)
    
    # Проверяем, что значение сохранилось с запятой
    assert amount_input.get_attribute("value") == test_amount, \
        f"Запятая как разделитель не работает. Ожидалось: {test_amount}"
    
    # 5. Дополнительно можно проверить, что кнопка подтверждения активна
    try:
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        assert submit_button.is_enabled(), "Кнопка подтверждения должна быть активна при вводе суммы с разделителем"
    except NoSuchElementException:
        pass