from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
from db import add_link, close_connection

MAX_DEPTH = 400
URL = 'https://apple.com'
# FILENAME = 'links.txt'

sites = set()
depth = 0
counter = 0

def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False

# def save_links(filename='links.txt'):
#     with open(filename, "a") as file:
#         for site in sites:
#             file.write(f"{site}\n")

# def print_links():
#     print("\n\nRESULT:\n")
#     with open(FILENAME, 'r') as file:
#         for line in file:
#             print(line)

def get_links(url='https://apple.com/'):
    global depth, counter

    if depth >= MAX_DEPTH: return

    try:
        page = requests.get(url, timeout=10)
        print(page.status_code)

        if page.status_code == 200:
            depth += 1
            print(f"Depth: {depth}\n")

            soup = BeautifulSoup(page.text, "html.parser")
            allNews = soup.findAll('a', href=True)

            for news in allNews:
                link = news['href']
                
                if link not in ['', '#']:
                    link = urljoin(url, link)

                    if link not in sites and uri_validator(link):
                        counter += 1

                        sites.add(link)

                        # if counter % 100 == 0:
                        #     save_links("linkss.txt")

                        # if counter % 10000 == 0:
                        #     save_links()
                        #     sites.clear()
                        add_link(link)

                        get_links(link)
    except Exception as e:
        print(f"Error: {url}, Exception: {e}")

get_links(URL)
close_connection()
# if sites:
#     save_links()
# print_links()
