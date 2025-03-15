import sys
import io
from bs4 import BeautifulSoup
import requests
import concurrent.futures
import math

def fetch_rank(university_url):
    rank_page = requests.get(university_url)
    rank_soup = BeautifulSoup(rank_page.text, 'html.parser')

    # Извлекаем рейтинг
    rank_element = rank_soup.select_one(".univ-subsection-full-width-value.bottom-div div")

    if rank_element:
        try:
            rank = rank_element.text.strip().replace("+", "")  # Извлекаем текст и убираем "+"
            rank = rank.replace("=", "").strip()  # Убираем "="
            rank = math.ceil(float(rank))  # Преобразуем в число и округляем
        except ValueError:
            rank = 0  # В случае ошибки преобразования ставим 0
        return rank
    return 0  # Если элемента нет, возвращаем 0

def scrape_universities():
    url = 'https://www.topuniversities.com/student-info/choosing-university/worlds-top-100-universities'

    # Запрашиваем главную страницу
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Парсим данные и создаем список с ссылками и названиями университетов, добавляем поле для рейтинга
    parsed_data = [[link['href'], link.get_text(strip=True), None] for link in soup.select('.top_universities_tbl_list a[href]')]

    # Создаем список URL для всех университетов
    university_urls = ['https://www.topuniversities.com' + data[0] for data in parsed_data]

    # Используем concurrent.futures для параллельных запросов
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        ranks = list(executor.map(fetch_rank, university_urls))

    # Добавляем полученные рейтинги в parsed_data
    for i, rank in enumerate(ranks):
        parsed_data[i][2] = rank

    return parsed_data
