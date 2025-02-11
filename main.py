import requests
import bs4
from fake_headers import Headers

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
URL = 'https://habr.com'

HEADERS = Headers(browser='chrome', os="win", headers=True).generate()
response = requests.get(URL + '/ru/articles', headers=HEADERS)

if response.status_code != 200:
    print(f'Ошибка {response.status_code}: Не удалось получить страницу.')
    exit()

soup = bs4.BeautifulSoup(response.text, features='lxml')
article = soup.find_all(class_='tm-articles-list__item')

for art in article:
    text = art.get_text().lower() # Приводим текст статьи к нижнему регустру для поиска ключевых слов
    if any(keyword in text for keyword in KEYWORDS): # Проверяем, есть ли хотя бы одно ключевое слово
        date_tag = art.find(class_='tm-user-info tm-article-snippet__author')
        date = date_tag.find('time'). get ('title', 'Дата не найдена') if date_tag else 'Дата не найдена'

        title_tag = art.find(class_='tm-title__link')
        title = title_tag.find('span').get_text(strip = True) if title_tag else 'Заголовок не найден'

        href = title_tag.get('href', '') if title_tag else ''
        link = URL + href if href else 'Сылка отсутствует'


    #
    # for key in KEYWORDS:
    #     if key in art.text:
    #         data = art.find(class_='tm-user-info tm-article-snippet__author').find('time').attrs['title']
    #         href = art.find(class_='tm-title__link').attrs['href']
    #         title = art.find(class_='tm-title__link').find('span').text

        print(f'Дата: {date}')
        print(f'Заголовок: {title}')
        print(f'Ссылка: {link}')
        print('-'* 80)