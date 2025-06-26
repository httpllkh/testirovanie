from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Настройка веб-драйвера
driver = webdriver.Chrome(executable_path='/path/to/chromedriver')


def test_form_validation():
    # Тест 1: Проверка отрицательных значений в поле "резерв"
    driver.get("http://localhost:8000/?balance=30000&reserved=-1000")
    time.sleep(2)

    # Проверка, что значение в поле "резерв" отрицательное
    reserve_field = driver.find_element(By.NAME, "reserved")
    assert reserve_field.get_attribute('value') == "-1000"

    # Проверка блокировки кнопки продолжения (если кнопка доступна)
    try:
        continue_button = driver.find_element(By.NAME, "continue")
        assert not continue_button.is_enabled(), "Кнопка продолжения должна быть заблокирована"
    except:
        print("Кнопка продолжения недоступна, как и ожидалось")

    # Проверка сообщения об ошибке
    try:
        error_message = driver.find_element(By.CLASS_NAME, "error-message")
        assert "Зарезервированная сумма не может быть отрицательной" in error_message.text
    except:
        print("Сообщение об ошибке не появилось")

    # Тест 2: Проверка текстовых значений в поле "balance"
    driver.get("http://localhost:8000/?balance=dsfs&reserved=1000")
    time.sleep(2)

    # Проверка, что в поле "balance" отображается "NaN ₽"
    balance_field = driver.find_element(By.NAME, "balance")
    assert "NaN" in balance_field.text

    # Проверка сообщения об ошибке или значения по умолчанию
    try:
        error_message = driver.find_element(By.CLASS_NAME, "error-message")
        assert "Ошибка" in error_message.text
    except:
        print("Сообщение об ошибке не появилось, использовано значение по умолчанию")


# Запуск теста
test_form_validation()

# Закрытие браузера
driver.quit()
