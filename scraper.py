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

url = 'http://books.toscrape.com/catalogue/set-me-free_988/index.html'

response = requests.get(url)

if response.ok:
    soup = BeautifulSoup(response.text, 'lxml')
    
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

