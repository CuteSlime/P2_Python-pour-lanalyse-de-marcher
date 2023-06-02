# coding: utf-8

import requests, re, csv
from pathlib import Path
from urllib import request
from bs4 import BeautifulSoup



def replace_all(text, dic):
            for i, j in dic.items():
                text = text.replace(i, j)
            return text
"""

récupération des catégories d'ouvrages

"""
base_url = "http://books.toscrape.com/catalogue/category/books_1/index.html"

response_all = requests.get(base_url)

if response_all.ok:
    
    soup = BeautifulSoup(response_all.content, 'lxml')

category_list = soup.find('ul', class_='nav nav-list').select('a')

links = ["http://books.toscrape.com/catalogue/category" +
         el.get('href')[2:] for el in category_list[1:]]

names = [" ".join(el.text.split()) for el in category_list[1:]]

categorys = dict(zip(names, links))
"""

récupération de tout les ouvrages d'une catégorie

"""
# for every category
for category, category_page_url in categorys.items():
    
    Path(f'./ScrapedData/{category}/IMG').mkdir(parents=True, exist_ok=True)
    
    response_cat = requests.get(category_page_url[:-10] + "index.html")
    
    page_number = 2
    
    books_links = []

    print(f'\n {category} \n')
   
    while response_cat.ok:
        soup = BeautifulSoup(response_cat.content, 'lxml')
        
        response_cat = requests.get(category_page_url[:-10] + f"page-{str(page_number)}.html") 
        
        page_number += 1
         
    # get full url by taking relative link from very book starting index 7 and adding original url on the begining
        books_links.extend(["http://books.toscrape.com/catalogue" + book_link.get('href')[8:] for book_link in soup.find('ol', class_='row').select('h3 > a')])

    
    

    """ 

    récupération des données de l'ouvrage

    """
    for product_page_url in books_links:

        response = requests.get(product_page_url)

        if response.ok:
            soup = BeautifulSoup(response.content, 'lxml')
            
        # category = soup.find('ul', class_= 'breadcrumb').find(href=re.compile('../category/books/')).text

        product_main = soup.find('div', class_= 'col-sm-6 product_main')

        title = product_main.find('h1').text 
        
        cleaner = {",": "","#": ""," ": "_","*": "","?": "",":": "","/": "","\\": "","|": "","<": "",">": "","\"": ""}

        image_url = ("http://books.toscrape.com" +
             soup.find(attrs={'alt': title})['src'][5:]) 

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

        book_detail = {'product_page_url': str(product_page_url), 'universal_product_code (upc)': str(universal_product_code), 'title': str(title), 'price_including_tax': str(price_including_tax), 'price_excluding_tax': str(price_excluding_tax), 'number_available': str(number_available), 'product_description': str(product_description), 'category': str(category), 'review_rating': str(review_rating), 'image_url': str(image_url)}
        
        fieldnames = ['product_page_url', 'universal_product_code (upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
        reader = csv.DictReader(bk, dialect='excel', delimiter=';', fieldnames=fieldnames)
        writer = csv.DictWriter(bk, dialect='excel', delimiter=';', fieldnames=fieldnames)
        
        if Path(f'ScrapedData/{category}/{category}.csv').is_file():
            with open(f'ScrapedData/{category}/{category}.csv', 'a', encoding="utf-8-sig") as bk:
                writer.writerow(book_detail)
        else :
            with open(f'ScrapedData/{category}/{category}.csv', 'w', encoding="utf-8-sig") as bk:
                writer.writeheader()
                writer.writerow(book_detail)


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

