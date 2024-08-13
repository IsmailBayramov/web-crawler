from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
import db

MAX_DEPTH = 4
URL = 'http://apple.com/'

# Хранение уже обработанных ссылок
visited_links = set()

def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False

def get_links(url, depth, connection):
    if depth >= MAX_DEPTH: 
        return

    try:
        page = requests.get(url, timeout=10)
        if page.status_code == 200:
            print(f"Depth: {depth} - URL: {url}")

            soup = BeautifulSoup(page.text, "html.parser")
            allNews = soup.findAll('a', href=True)

            for news in allNews:
                href = news['href']
                href = urljoin(url, href)
                parsed = urlparse(href)
                href = parsed.scheme + "://" + parsed.netloc + parsed.path

                if uri_validator(href) and parsed.scheme in ('http', 'https') and href not in visited_links:
                    visited_links.add(href)
                    db.add_link(connection, href)
                    # Рекурсивный вызов с увеличением глубины
                    get_links(href, depth + 1, connection)

    except Exception as e:
        print(f"Error: {url}, Exception: {e}")

if __name__ == "__main__":
    connection = db.init_db()

    # Начальная обработка
    links = []
    page = requests.get(URL, timeout=10)

    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "html.parser")
        allNews = soup.findAll('a', href=True)

        for news in allNews:
            href = news['href']
            href = urljoin(URL, href)
            parsed = urlparse(href)
            href = parsed.scheme + "://" + parsed.netloc + parsed.path

            if uri_validator(href) and parsed.scheme in ('http', 'https'):
                visited_links.add(href)
                db.add_link(connection, href)
                links.append(href)
    
    for link in links:
        get_links(link, 0, connection)

    connection.close()
