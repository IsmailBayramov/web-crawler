from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse

MAX_DEPTH = 100
URL = 'https://caisu1.ning.com/photo/albums/uyjihgpq'

sites = []
depth = 0
counter = 0

def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False
    
def save_links():
    with open("links.txt", "a") as file:
        for site in sites:
            file.write(f"{site}\n")

def print_links():
    print("\n\nRESULT:\n")

    with open('links.txt', 'r') as file:
        for line in file:
            print(line)

def get_links(url = 'https://apple.com/'):
    global depth, counter
    
    if depth >= MAX_DEPTH: return

    try:
        page = requests.get(url)
        print(page.status_code)

        if page.status_code == 200:
            depth += 1
            print(f"Depth: {depth}\n")

            soup = BeautifulSoup(page.text, "html.parser")
            allNews = soup.findAll('a', href=True)

            for news in allNews:
                link: str = news['href']

                if link not in ['', '#']:
                    link = urljoin(url, link)

                    if link not in sites and uri_validator(link):
                        counter += 1

                        sites.append(link)

                        if counter % 100 == 0:
                            save_links()

                        if counter % 10000 == 0:
                            save_links()
                            sites.clear()

                        get_links(link)
    except:
        print(f"Error: {url}")

get_links(URL)
if sites:
    save_links()
print_links()