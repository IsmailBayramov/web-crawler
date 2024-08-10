from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import json

sites = []
depth = 0

def get_links(url = 'https://apple.com/'):
    global depth
    
    if depth >= 100: return

    main_url = url.split('/')
    main_url = f"{main_url[0]}//{main_url[2]}"

    try:
        page = requests.get(url)
        allNews = []

        print(page.status_code)

        if page.status_code == 200:
            depth += 1
            print(f"Depth: {depth}")

            soup = BeautifulSoup(page.text, "html.parser")
            allNews = soup.findAll('a', href=True)

            for news in allNews:
                link: str = news['href']

                if link not in ['', '/'] and link.count(':') == 0 and link.count('#') == 0:
                    if link[:4] != 'http':
                        link = link if link[0] == '/' else '/' + link
                        news['href'] = f"{main_url}{link}"

                    if news['href'] not in sites:
                        sites.append(news['href'])
                        get_links(news['href'])
    except:
        print(f"Error: {url}")

get_links("https://caisu1.ning.com/photo/albums/uyjihgpq")

sites.reverse()

print("\n\nRESULT:\n")
for site in sites:
    print(site)