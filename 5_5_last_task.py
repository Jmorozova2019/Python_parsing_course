import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def set_option_values(block_tag, span_val):
    # В выпадающем списке в каждом контейнере найдите и выберите тот же HEX цвет что и у родительского контейнера.
    block_tag.find_element(By.TAG_NAME, 'select').click()
    option_tags = block_tag.find_elements(By.TAG_NAME, 'option')

    for option_tag in option_tags:
        if option_tag.text in span_val:
            option_tag.click()
            break

start = time.time()

with webdriver.Chrome() as browser:
    browser.get('https://parsinger.ru/selenium/5.5/5/1.html')
    block_tags = browser.find_elements(By.CSS_SELECTOR, 'div[id="main-container"]>div')

    for block_tag in block_tags:
        # Получите цвет в формате HEX из каждого элемента <span>.
        span_val = block_tag.find_element(By.TAG_NAME, 'span').text

        # В выпадающем списке в каждом контейнере найдите и выберите тот же HEX цвет что и у родительского контейнера.
        set_option_values(block_tag, span_val)

        # Найдите и нажмите на кнопку, у которой атрибут data-hex совпадает с HEX цветом родительского контейнера.
        block_tag.find_element(By.XPATH, './/div/button[@data-hex="' + span_val + '"]').click()

        # Поставьте галочку в чек-боксе на странице
        block_tag.find_element(By.XPATH, './input[@type="checkbox"]').click()

        # Вставьте в текстовое поле тот же HEX-цвет, который имеет фон родительского контейнера.
        block_tag.find_element(By.XPATH, './input[@type="text"]').send_keys(span_val)

        # Нажмите на кнопку "Проверить": если вставлен корректный HEX, то на кнопке появится "ОК".
        block_tag.find_element(By.XPATH, './button').click()

    # нажмите на кнопку "Проверить все элементы"
    browser.find_element(By.CSS_SELECTOR, 'body>button').click()

    # Из алерт-окна получите числовой код
    print(browser.switch_to.alert.text)

finish = time.time()
print(finish - start)
