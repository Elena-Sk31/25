from os import environ

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

# 25.3.1

valid_email = environ.get('USERNAME')
valid_password = environ.get('PASSWORD')


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Firefox()

    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    yield driver

    driver.quit()


def test_show_all_pets(driver):
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(valid_email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    # Переход на страницу питомцев (неявное ожидание)
    driver.implicitly_wait(10)
    driver.get("https://petfriends.skillfactory.ru/my_pets")
    # Загрузка строк таблицы
    pets_rows = driver.find_elements(By.XPATH, '//tbody//tr')

    # Загрузка изображений
    pets_images = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//tbody//tr//img'))
    )

    pets_names = list()
    pets_animal_types = list()
    pets_ages = list()

    for row in pets_rows:
        pet_info = row.find_elements(By.TAG_NAME, 'td')

        pets_names.append(pet_info[0].text)
        pets_animal_types.append(pet_info[1].text)
        pets_ages.append(pet_info[2].text)

    pets_cnt = driver.find_element(By.CLASS_NAME, '\.col-sm-4').text
    pets_cnt = pets_cnt.split('\n')[1]
    pets_cnt = int(pets_cnt.replace('Питомцев: ', ''))

    # Присутствуют все питомцы
    assert pets_cnt == len(pets_images) == len(pets_names) == len(pets_animal_types) == len(pets_ages)

    # Хотя бы у половины питомцев есть фото
    images_cnt = 0
    for img in pets_images:
        if img.get_attribute('src'):
            images_cnt += 1

    assert images_cnt >= pets_cnt / 2

    # У всех питомцев есть имя, возраст и порода
    assert pets_cnt == len([name for name in pets_names if name])
    assert pets_cnt == len([animal_type for animal_type in pets_animal_types if animal_type])
    assert pets_cnt == len([age for age in pets_ages if age])

    # У всех питомцев разные имена
    assert pets_cnt == len(set(pets_names))

    # В списке нет повторяющихся питомцев
    uniq_pets = {(pets_names[i], pets_animal_types[i], pets_ages[i]) for i in range(pets_cnt)}
    assert pets_cnt == len(uniq_pets)

"""

В написанном тесте (проверка карточек питомцев) добавьте неявные ожидания всех элементов 
(фото, имя питомца, его возраст).

В написанном тесте (проверка таблицы питомцев) добавьте явные ожидания элементов страницы.

Чеклист для самопроверки:
 В тестах используются элементы класса WebDriverWait.
"""
