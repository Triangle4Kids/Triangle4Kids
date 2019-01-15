import requests
from bs4 import BeautifulSoup

url_pagination = "http://www.carolinaparent.com/CP/Camp-Listings/"
r = requests.get(url_pagination)
soup = BeautifulSoup(r.content, "html.parser")

page_url = "http://www.carolinaparent.com/CP/Camp-Listings/"
last_page = soup.find(
    'div', class_='pagination').find(
        'li', class_='active').a['href'].split('=')[1]
camp_page_url = [page_url.format(i) for i in range(1, int(last_page) + 1)]

print(camp_page_url)
