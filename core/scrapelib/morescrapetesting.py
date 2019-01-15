import urllib
import urllib.request
from bs4 import BeautifulSoup

campUrl = "http://www.carolinaparent.com/CP/Camp-Listings/"
pageUrl = urllib.request.urlopen(campUrl)
soup = BeautifulSoup(pageUrl, "html.parser")

print(soup.title.text)
# gets all featured and premium listing names
for link in soup.findAll("h4", {"class": "business-name"}):
    print(link.text)

# gets all free listing names
for name in soup.findAll("h5", {"class": "business-name"}):
    print(name.text)