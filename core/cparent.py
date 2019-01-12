import requests
from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException
from contextlib import closing

source = requests.get('http://www.carolinaparent.com/CP/Camp-Listings/index.php?').text
    
soup = BeautifulSoup(source, 'lxml')

listing = soup.find(id="listing0")

business_tag = 
for child in listing_header

name = listing.h4.text

#address = 

#city = 

# for article in soup.find_all('div', class_='business-name')
#
# create a function in Python class called save_business and pass in parameter of name of the 
# business model and then make another that is called save_event
# create a new business model object
# once I have a name, query the db and then get back the record that matches that name
# if no record comes back, create a new one
# add what you have to an array
# outside the loop where you scrape...you loop through each of business objects you created and save them
# need query for pagination...pass me page 1 with x items per page
# find out how many pages there are in advance and do a for loop from page 1 to page last
# if can't, 
# 
#
# 
#
# 

# headline = article.h2.a.text


# def simple_get(url):
#     """
#     Attempts to get the content at `url` by making an HTTP GET request.
#     If the content-type of response is some kind of HTML/XML, return the
#     text content, otherwise return None.
#     """
#     try:
#         with closing(get(url, stream=True)) as resp:
#             if is_good_response(resp):
#                 return resp.content
#             else:
#                 return None

#     except RequestException as e:
#         log_error('Error during requests to {0} : {1}'.format(url, str(e)))
#         return None


# def is_good_response(resp):
#     """
#     Returns True if the response seems to be HTML, False otherwise.
#     """
#     content_type = resp.headers['Content-Type'].lower()
#     return (resp.status_code == 200 
#             and content_type is not None 
#             and content_type.find('html') > -1)


# def log_error(e):
#     """
#     It is always a good idea to log errors. 
#     This function just prints them, but you can
#     make it do anything.
#     """
#     print(e)