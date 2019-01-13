import urllib
import urllib.request
import requests
from bs4 import BeautifulSoup
from string import ascii_lowercase


def getCampBizList(url):

    pageUrl = urllib.request.urlopen(url)
    soupdata = BeautifulSoup(pageUrl, "html.parser")
    return soupdata


# loops through and pulls all addresses (number, street, suite)
campdatasaved = ""
soup = getCampBizList(
    "http://www.carolinaparent.com/CP/Camp-Listings/index.php?")
for camp in soup.findAll("ul", {"listings"}):
    campdata = ""
    for data in camp.findAll("p", {"class": "address1"}):
        campdata = campdata + "," + data.text
    campdatasaved = campdatasaved + "\n" + campdata[1:]

print(campdatasaved)

#gets all 50 listings on a page
for record in soup.findAll("ul", {"class": "listings"}):

# gets all premium listings
for record in soup.findAll("li", {"class": "premium listing"}):

# gets all addresses (number, street, suite)
for record in soup.findAll("p", {"class": "address1"}):

# gets address, city / state / zip, phone
for record in soup.findAll("div", {"class": "contact"})

# gets phone
for record in soup.findAll("p", {"class": "phone"})
