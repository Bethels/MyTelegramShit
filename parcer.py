import requests
from bs4 import BeautifulSoup

url = 'https://helpix.ru/currency/'
page = requests.get(url).text
soup = BeautifulSoup(page, 'lxml')


def table_check(table):
    if '-' in table.values():
        pass


def get_table(day):
    columns = 6
    cells = [i.text for i in soup.find_all(class_='b-tabcurr__td')]
    cells = [cells[i] for i in range((day - 1) * columns, day * columns)]
    headers = [i.text for i in soup.find_all(class_='b-tabcurr__th')]
    result = dict(zip(cells, headers))
    return dict(zip(headers, cells))
