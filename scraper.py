import requests
import re
from bs4 import BeautifulSoup

"""

récupération des catégories d'ouvrages

"""


"""

récupération de tout les ouvrages d'une catégorie

"""


""" 

récupération des données de l'ouvrage

"""

product_page_url = 'http://books.toscrape.com/catalogue/set-me-free_988/index.html'

response = requests.get(product_page_url)

if response.ok:
    soup = BeautifulSoup(response.text, 'lxml')
    
    category = soup.find('ul', class_= 'breadcrumb').find(href=re.compile('../category/books/')).text
    
    product_main = soup.find('div', class_= 'col-sm-6 product_main')

    title = product_main.find('h1').text
    
    image_url = re.compile(r'\.\./\.\./')
    image_url = 'http://books.toscrape.com/' + image_url.sub('', soup.find(attrs={'alt': title})['src'])
    
    number_available = re.search('\d+', product_main.find('p', class_= 'instock availability').text)
    
    review_rating = product_main.find('p', class_= re.compile('star-rating'))['class'][1]

    if review_rating == "Five":
        review_rating = "5"
    elif review_rating == "Four":
        review_rating = "4"
    elif review_rating == "Three":
        review_rating = "3"
    elif review_rating == "Two":
        review_rating = "2"
    elif review_rating == "One":
        review_rating = "1"
    else:
        review_rating = "0"

product_description = soup.select_one('#product_description + p').text

tablesoup = soup.find('table', class_= 'table table-striped')

th = []
td = []
for i in tablesoup.find_all('th'):
    th.append(i.text)
for i in tablesoup.find_all('td'):
    td.append(i.text)

table = dict(zip(th, td))

universal_product_code = table.get('UPC')

price_excluding_tax = table.get('Price (excl. tax)')

price_including_tax = table.get('Price (incl. tax)')

print(f'\'{category}\' \'{title}\' en stock : {number_available.group()} note : {review_rating} \n{product_description} \n \n {image_url} ')
print(f'\n {universal_product_code} \n {price_excluding_tax} \n {price_including_tax}')

quit()
"""
http://books.toscrape.com/catalogue/set-me-free_988/index.html
● product_page_url

body > div container-fluid page > div page_inner > ul breadcrumb > li > href="../category/books/"
● category


body > div container-fluid page > div page_inner > div content > div content_inner > article product_page


div row > div col-sm-6 product_main > h1
● title


div row > div col-sm-6 product_main > p instock availability
● number_available


div row > div col-sm-6 product_main > p star-rating five
● review_rating


p
● product_description


table > table table-striped > tbody > tr > th(name) > td (value)
● universal_ product_code (upc)
● price_including_tax
● price_excluding_tax

"""

