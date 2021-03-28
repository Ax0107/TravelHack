from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import time

# Указать путь к webdriver (https://chromedriver.chromium.org/downloads)
PATH_TO_WEBDRIVER = 'C:\\Programming\\chromedriver.exe'

# Время после загрузки страницы и прогрузки туров
TIMESLEEP_LOADING = 10

driver = webdriver.Chrome(PATH_TO_WEBDRIVER)


def get_elements(adults=2, dateDelta=3, date_from='2021-04-13', date_shift=21, direction_country_to=233909, direction_from=274286, max_cost=2000000, night_from=7, night_to=11):
    """Получает туры по направлению"""

    # Формирование запроса к сайту
    url = f'https://www.tui.ru/search/?adults={adults}&dateDelta={dateDelta}&dateFrom={date_from}&dateShift={date_shift}&directionCountryTo={direction_country_to}&directionFrom={direction_from}&maxCost={max_cost}&nightsFrom={night_from}&nightsTo={night_to}&selected=departure-date&sortType=1'
    # Получаем страницу
    driver.get(url)

    # Ждём загрузки туров
    time.sleep(TIMESLEEP_LOADING)
    # Подсчитываем предложения
    count = int(driver.find_element_by_css_selector('.search-result-count__title').text.replace('Найдены туры в ', '').replace('отель', ''))
    btn = driver.find_element_by_class_name('search-results__show-more')
    actions = ActionChains(driver)
    i = 0
    while i != count:
        try:
            # Спускаемся к кнопке "Показать ещё"
            actions.move_to_element(btn).perform()
            driver.execute_script("window.scrollBy(0, 100);")
            time.sleep(0.25)

            # Нажимаем кнопку"
            btn.click()
            i += 1
        except Exception as e:
            # Если кнопки больше нет
            if 'element is not attached to the page document' in str(e):
                break
            print(e)

    bs = BeautifulSoup(driver.page_source, features="lxml")
    elemts = bs.find_all('div', {'class': 'search-result'})
    print('Имеем {} предложений по запросу.'.format(len(elemts)))
    driver.close()
    return elemts


def parse_element(element):
    """Парсинг данных (ссылка на отель, стикеры и стоимость) из элементов"""

    stickers = [i.text for i in element.findChildren("div", {'class': 'sticker_item'}, recursive=True)]
    details_href = element.findChildren('a', {'class': 'hotel-name-class'}, recursive=True)[0]['href']
    HotelTags = [tag.text for tag in element.findChildren('div', {'class': 'HotelTags'}, recursive=True)]
    price = element.findChildren('span', {'class': 'price'})[0].findChildren('span')[0].text

    print(details_href, stickers, HotelTags, price)
    return details_href, stickers, HotelTags, price


if __name__ == "__main__":
    # Получаем данные
    elements = get_elements(adults=2, dateDelta=3, date_from='2021-04-13', date_shift=21, direction_country_to=233909, direction_from=274286, max_cost=2000000, night_from=7, night_to=11)

    # Парсим данные
    for i in elements:
        details_href, stickers, HotelTags, price = parse_element(i)
        # TODO: Что-то делаем дальше ...

