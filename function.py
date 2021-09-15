from math import ceil
import requests
from bs4 import BeautifulSoup
import csv342 as csv
from pathlib import Path

# extract data and filled list categories and list url categories
def fill_list_categories(global_url):
    try:
        page = requests.get(global_url)
        soup_cat = BeautifulSoup(page.content, 'html.parser')
        ret = extract_categories(soup_cat)
        return ret
    except:
        return 'Nothing found'



# extract_categories function
def extract_categories(soup_cat):
    list_categories = []
    list_category_url = []
    try:
        list_elem = soup_cat.find("ul", class_="nav-list").find_all("a")
        for elem in list_elem:
            list_category_url.append(elem.get("href"))
            list_categories.append(elem.string.strip())
        # print(list_categories)
        # print(list_category_url)    
        return [list_categories, list_category_url]
    except:
        return 'Nothing found'

# extract number item by category
def get_paging_url(url_cat):
    retour = []
    try:
        page_cat = requests.get(url_cat)
        soup_pag = BeautifulSoup(page_cat.content, 'html.parser')
        c = soup_pag.find("form", class_="form-horizontal")
        nb_items = c.text.split()[0]
        retour.append(nb_items)
        list_url_items = extract_items(soup_pag)
        retour.append(list_url_items)
        return retour
    except:
        return 'error'



# extract all items by page by category
def extract_items(soup_item):
    try:
        list_elem = soup_item.find("ol", class_="row").find_all("a")
        list_url_item = []
        for ls in list_elem:
            knil = ls.get("href").strip("./")
            if knil in list_url_item:
                continue
            else:
                list_url_item.append(knil)
        # print(list_url_item)
        return list_url_item
    except:
        return 'error'


# create csv by category
def create_csv(catalog, en_tete, category, get_items, global_url):
    try:
        with open("./data/"+ category +".csv", 'w') as file_csv:  # create and open csv
            writer = csv.writer(file_csv, delimiter='|')
            writer.writerow(en_tete)        
            for get_item in get_items:
                url_item = catalog + get_item  # url item 
                poge = requests.get(url_item)
                soup_item = BeautifulSoup(poge.content, 'html.parser')
                data_item = extract_final_data(soup_item, global_url, url_item, category)   # data of item
                # print(data_item[1])        
                writer.writerow(data_item)
        return True
    except:
        return False


# add data in csv
def add_data_in_csv(catalog, url_cat, category, get_items, global_url, indice):
    try:
        w = 2
        while w <= indice:            
            url_modifying = url_cat.replace("index", "page-" + str(w))
            # print(url_modifying)
            page_cat = requests.get(url_modifying)
            soup_pag = BeautifulSoup(page_cat.content, 'html.parser')

            get_items = extract_items(soup_pag)

            with open("./data/"+ category +".csv", 'a') as file_csv:
                writer = csv.writer(file_csv, delimiter='|')
                for get_item in get_items:
                    url_item = catalog + get_item
                    page = requests.get(url_item)
                    soup_item = BeautifulSoup(page.content, 'html.parser')
                    data_item = extract_final_data(soup_item, global_url, url_item, category)                
                    writer.writerow(data_item)
                
            w += 1
        return True
    except:
        return False



# extract final data for each item
def extract_final_data(soup, global_url, url_item, category):
    list_result = []
    try:
        tr_data = soup.find_all("tr")
        res = {}

        for i in range(len(tr_data)):
            res[tr_data[i].find('th').text] = tr_data[i].find('td').text

        res["title"]= soup.find("h1").text

        res["product_description"] = soup.find("p", class_="").text

        list_li = soup.find("ul", class_="breadcrumb")
        content_li = list_li.findChildren()[4]
        res["category"] = content_li.find("a").text

        elem = soup.find("img")
        img = elem['src'].strip("./")
        res["image_url"] = '{}{}'.format(global_url, '/' + img)



        list_result.append(url_item)
        list_result.append(res["UPC"])
        list_result.append(res["title"])
        tax_in = res["Price (incl. tax)"].strip("£")
        list_result.append(tax_in)
        tax_ex = res["Price (excl. tax)"].strip("£")
        list_result.append(tax_ex)
        modify_1 = res["Availability"]
        modify_2 = modify_1[modify_1.find('(') + 1: modify_1.find(')')]
        modify_3 = modify_2.split(" ")
        list_result.append(modify_3[0])
        list_result.append(res["product_description"])
        list_result.append(res["category"])
        list_result.append(res["Number of reviews"])
        list_result.append(res["image_url"])
        download_img(res["title"], res["image_url"], category)
        # print(list_result)
        return list_result
    except:
        return 'error'

# download image
def download_img(title, image_url, category):
    path = Path("img/" + category)
    path.mkdir(parents=True, exist_ok=True)
    print(image_url)
    print(path)
    f = open("img/" + category +'/' + title + '.jpg', 'wb')
    response = requests.get(image_url)
    print(response)
    if response.content:
        print('OK')
        f.write(response.content)    
        f.close()
    else:
        print('KO')
        f.close()
