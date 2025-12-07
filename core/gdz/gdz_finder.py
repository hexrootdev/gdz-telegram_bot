import requests
from bs4 import BeautifulSoup


def _get_name_author(link: str):
    r = requests.get(link).text  
    content = BeautifulSoup(r, 'html.parser')
    meta = content.find('meta', {'name': 'keywords'}).get('content')  
    return meta.split()[1] 

def get_authors(cls: str, subject: str):
    response = requests.get(f'https://gdz.ru/class-{cls}/{subject}')
    content = BeautifulSoup(response.content, "html.parser")

    links = []
    authors = {}

    for i in content.find_all('a', class_='book__link'):
        links.append(i.get('href'))

    count = 0  
    for i in links:
        if count < 5:  
            name = _get_name_author(link=f'https://gdz.ru{i}')
            authors.setdefault(name, f'https://gdz.ru{i}')
            count += 1  
    return authors

def get_tasks(link: str):
    tsk = {}

    response = requests.get(link)
    content = BeautifulSoup(response.content, "html.parser")
    tasks = content.find_all('a', class_='task__button js-task-button prevent')

    for task in tasks:
        number = task.get('href').split('/')[-2].split('-')
        for el in number:
            if not el.isdigit():
                number.remove(el)
        tsk.setdefault('-'.join(number), 'https://gdz.ru' + task.get('href'))

    return tsk

def get_images(link: str):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_='task-img-container')
    comps = []

    for item in items:
        comps.append(item.find('img').get('src'))

    return comps


