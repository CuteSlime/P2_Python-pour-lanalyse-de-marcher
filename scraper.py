# coding: utf-8

import requests
import pathlib
import re
import csv
from bs4 import BeautifulSoup

pathlib.Path('./ScrapedData/IMG').mkdir(parents=True, exist_ok=True)
"""

récupération des catégories d'ouvrages

"""


"""

récupération de tout les ouvrages d'une catégorie

"""
#i = 2
# while f"{url catégorie}/page-{i}.html exist:
# category_page_url = f"http://books.toscrape.com/catalogue/category/books/{category}_??/"

""" 

récupération des données de l'ouvrage

"""

product_page_url = 'http://books.toscrape.com/catalogue/set-me-free_988/index.html'

response = requests.get(product_page_url)

if response.ok:
    soup = BeautifulSoup(response.content, 'lxml')
    
category = soup.find('ul', class_= 'breadcrumb').find(href=re.compile('../category/books/')).text

product_main = soup.find('div', class_= 'col-sm-6 product_main')

title = product_main.find('h1').text

image_url = re.compile(r'\.\./\.\./')
image_url = 'http://books.toscrape.com/' + image_url.sub('', soup.find(attrs={'alt': title})['src'])

number_available = re.search('\d+', product_main.find('p', class_= 'instock availability').text)[0]

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

book = {'product_page_url': str(product_page_url), 'universal_product_code (upc)': str(universal_product_code), 'title': str(title), 'price_including_tax': str(price_including_tax), 'price_excluding_tax': str(price_excluding_tax), 'number_available': str(number_available), 'product_description': str(product_description), 'category': str(category), 'review_rating': str(review_rating), 'image_url': str(image_url)}

with open(f'ScrapedData/{category}.csv', 'w', encoding="utf-8-sig") as bk:
    fieldnames = ['product_page_url', 'universal_product_code (upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
    reader = csv.DictReader(bk, dialect='excel', delimiter=';', fieldnames=fieldnames)
    writer = csv.DictWriter(bk, dialect='excel', delimiter=';', fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerow(book)


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

