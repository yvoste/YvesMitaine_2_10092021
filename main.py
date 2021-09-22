from math import ceil
from function import fill_list_categories, get_paging_url, create_csv, add_data_in_csv

# general paramters
global_url = "http://books.toscrape.com"
catalog = "http://books.toscrape.com/catalogue/"
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

# filled list_categories
ret = fill_list_categories(global_url)
list_categories = ret[0]
list_categories.remove('Books') # remove the first item books
list_category_url = ret[1]
list_category_url.pop(0)   # remove the first item books
# print(list_category_url)  


i = 0
while i < len(list_categories):
    # print(list_categories[i])
    url_cat = 'http://books.toscrape.com/'+ list_category_url[i]  #url category
    paging_and_list_items = get_paging_url(url_cat)
    nb_item_by_cat = paging_and_list_items[0] # nb items by category
    get_items = paging_and_list_items[1]  # list of item in first page of category
    is_file = create_csv(catalog, en_tete, list_categories[i], get_items, global_url)
    if is_file is False:
        break
    
    if int(nb_item_by_cat) > 20:
        indice = ceil(int(nb_item_by_cat) / 20)
        is_file = add_data_in_csv(catalog, url_cat, list_categories[i], get_items, global_url, indice)
        
        if is_file is False:
            break

    i += 1

