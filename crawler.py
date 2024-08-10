from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import json

sites = []
depth = 0

def get_links(url = 'https://apple.com/'):
    global depth
    
    if depth >= 100: return

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

                    if link not in sites:
                        sites.append(link)
                        get_links(link)
    except:
        print(f"Error: {url}")

get_links("https://caisu1.ning.com/photo/albums/uyjihgpq")

sites.reverse()

print("\n\nRESULT:\n")
for site in sites:
    print(site)