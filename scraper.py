# coding: utf-8

import requests
import re
import csv
from pathlib import Path
from urllib import request
from bs4 import BeautifulSoup

# cleaner fonction for file name


def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


"""

getting all books category

"""

base_url = "http://books.toscrape.com/catalogue/category/books_1/index.html"

response_all = requests.get(base_url)

if response_all.ok:

    soup = BeautifulSoup(response_all.content, 'lxml')

# get all categorys <a> tag with links and names
category_list = soup.find('ul', class_='nav nav-list').select('a')

# get link from category_list and use it to make the full link to category
links = ["http://books.toscrape.com/catalogue/category" +
         el.get('href')[2:] for el in category_list[1:]]

# get clean name from caterory list
names = [" ".join(el.text.split()) for el in category_list[1:]]

# send name and link into a dictionary
categorys = dict(zip(names, links))


"""

get every books from  every category

"""

# for every categorys take name and link renamed category and category_page_url
for category, category_page_url in categorys.items():

    response_cat = requests.get(category_page_url[:-10] + "index.html")

    # if a category have more than one page, link while start at "page-2.html", initialize page_number at 2
    page_number = 2

    books_links = []

    # print who help to know where the scraping is at
    print(f'\n {category} \n')

    # get every page
    while response_cat.ok:
        soup = BeautifulSoup(response_cat.content, 'lxml')

        response_cat = requests.get(
            category_page_url[:-10] + f"page-{str(page_number)}.html")

        page_number += 1

    # get full url by taking relative link from every book starting index 8 and adding original url on the begining
        books_links.extend(["http://books.toscrape.com/catalogue" + book_link.get('href')[8:]
                           for book_link in soup.find('ol', class_='row').select('h3 > a')])

    """ 

    get data from a book

    """

    for product_page_url in books_links:

        response = requests.get(product_page_url)

        if response.ok:
            soup = BeautifulSoup(response.content, 'lxml')

        # shortcut for others variables
        product_main = soup.find('div', class_='col-sm-6 product_main')

        title = product_main.find('h1').text

        # getting image_url befor cleanning title
        image_url = ("http://books.toscrape.com" +
                     soup.find(attrs={'alt': title})['src'][5:])

        # initialize a dict to use into replace_all function
        cleaner = {",": "", "#": "", " ": "_", "*": "", "?": "", ":": "",
                   "/": "", "\\": "", "|": "", "<": "", ">": "", "\"": ""}
        title = "".join(replace_all(title, cleaner).split("_(", 1)[0])

        # save image from url with the book name without space and the right img format
        image = request.urlretrieve(
            image_url, f'./ScrapedData/{category}/IMG/{title}.{image_url.split(".")[-1]}')

        # regex to find number available
        number_available = re.search(
            '\d+', product_main.find('p', class_='instock availability').text)[0]
        # use regex to found every class starting with "star-rating"
        review_rating = product_main.find(
            'p', class_=re.compile('star-rating'))['class'][1]

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

        # test if correct to avoid error
        product_description = soup.select_one('#product_description + p')

        if product_description == None:
            product_description = ""
        else:
            product_description = product_description.text

        tablesoup = soup.find('table', class_='table table-striped')

        # init varriable and populate them with the html table
        th = []
        td = []
        for i in tablesoup.find_all('th'):
            th.append(i.text)
        for i in tablesoup.find_all('td'):
            td.append(i.text)

        # transform it into a dict
        table = dict(zip(th, td))

        universal_product_code = table.get('UPC')

        price_excluding_tax = table.get('Price (excl. tax)')

        price_including_tax = table.get('Price (incl. tax)')

        # create dict with all the date using fieldname for the key value
        book_detail = {'product_page_url': str(product_page_url), 'universal_product_code (upc)': str(universal_product_code), 'title': str(title), 'price_including_tax': str(price_including_tax), 'price_excluding_tax': str(
            price_excluding_tax), 'number_available': str(number_available), 'product_description': str(product_description), 'category': str(category), 'review_rating': str(review_rating), 'image_url': str(image_url)}

        fieldnames = ['product_page_url', 'universal_product_code (upc)', 'title', 'price_including_tax',
                      'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']

        # verify if directory exist, if not, create it with parent folder
        Path(
            f'./ScrapedData/{category}/IMG').mkdir(parents=True, exist_ok=True)

        # verify if CSV exist, if exist, add a new book to it, if not, create a header and add the first book to it.
        if Path(f'ScrapedData/{category}/{category}.csv').is_file():
            with open(f'ScrapedData/{category}/{category}.csv', 'a', encoding="utf-8-sig", newline="") as bk:
                reader = csv.DictReader(
                    bk, dialect='excel', delimiter=';', fieldnames=fieldnames)
                writer = csv.DictWriter(
                    bk, dialect='excel', delimiter=';', fieldnames=fieldnames)
                writer.writerow(book_detail)
        else:
            with open(f'ScrapedData/{category}/{category}.csv', 'w', encoding="utf-8-sig", newline="") as bk:
                reader = csv.DictReader(
                    bk, dialect='excel', delimiter=';', fieldnames=fieldnames)
                writer = csv.DictWriter(
                    bk, dialect='excel', delimiter=';', fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(book_detail)
