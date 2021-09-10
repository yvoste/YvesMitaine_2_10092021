import requests
from bs4 import BeautifulSoup
import csv342 as csv
from math import ceil
from function import extract_categories, extract_items, extract_final_data

# general paramters
site = "http://books.toscrape.com"
catalog = "http://books.toscrape.com/catalogue/"
list_book_url = []
en_tete = [
    "product_page_url",
    "universal_product_code",
    "title",
    "price_including_tax",
    "price_excluding_tax",
    "number_available",
    "product_description",
    "category",
    "review_rating",
    "image_url"
]

global_url = "http://books.toscrape.com"

# filled list_categories
page = requests.get(global_url)
soup_cat = BeautifulSoup(page.content, 'html.parser')

ret = extract_categories(soup_cat)
list_categories = ret[0]
list_categories.remove('Books') # remove the first item books
list_category_url = ret[1]
list_category_url.pop(0)   # remove the first item books
            
"""
categories_url = []
for category_url in list_category_url:
    url_cat = 'http://books.toscrape.com/'+ category_url
    page_cat = requests.get(url_cat)
    soup_pag = BeautifulSoup(page_cat.content, 'html.parser')
    val = check_paging(soup_pag)
    print(val) 
    if val == 1:
        categories_url.append(url_cat)
    else:
        i = 1        
        while i <= val:
            if i == 1:
                categories_url.append(url_cat)
            else:
                url_modifying = category_url.replace("index", "page_" + str(i))
                categories_url.append(url_modifying)
            i += 1

print(categories_url)
print(len(list_categories))
print(list_categories)
print(list_category_url)

"""
i = 0
while i < len(list_categories):
    url_cat = 'http://books.toscrape.com/'+ list_category_url[i]  #url category
    page_cat = requests.get(url_cat)
    soup_pag = BeautifulSoup(page_cat.content, 'html.parser')
    c = soup_pag.find("form", class_="form-horizontal")
    nb_item_by_cat = c.text.split()[0]
    get_items = extract_items(soup_pag)  # list of item in first page of category
    print(list_categories[i])
    with open("./data/"+ list_categories[i] +".csv", 'w') as file_csv:  # create and open csv
        writer = csv.writer(file_csv, delimiter='|')
        writer.writerow(en_tete)
        for get_item in get_items:
            url_item = catalog + get_item  # url item 
            poge = requests.get(url_item)
            soup_item = BeautifulSoup(poge.content, 'html.parser')
            data_item = extract_final_data(soup_item, site, url_item)   # data of item
            print(data_item[1])        
            writer.writerow(data_item)
    

    if int(nb_item_by_cat) > 20:
        indice = ceil(int(nb_item_by_cat) / 20)
        w = 2        
        while w <= indice:            
            url_modifying = url_cat.replace("index", "page-" + str(w))
            print(url_modifying)
            page_cat = requests.get(url_modifying)
            soup_pag = BeautifulSoup(page_cat.content, 'html.parser')

            get_items = extract_items(soup_pag)

            with open("./data/"+ list_categories[i] +".csv", 'a') as file_csv:
                writer = csv.writer(file_csv, delimiter='|')
                for get_item in get_items:
                    url_item = catalog + get_item
                    poge = requests.get(url_item)
                    soup_item = BeautifulSoup(poge.content, 'html.parser')
                    data_item = extract_final_data(soup_item, site, url_item)                
                    writer.writerow(data_item)
                   
            w += 1
        
    i += 1
