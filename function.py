
from math import ceil
#####################
# extract_categories function
#####################

def extract_categories(soup_cat):
    list_categories = []
    list_category_url = []
    list_csv_file = []
    try:
        list_elem = soup_cat.find("ul", class_="nav-list").find_all("a")
        for elem in list_elem:
            list_category_url.append(elem.get("href"))
            list_categories.append(elem.string.strip())
        # print(list_categories)
        # print(list_category_url)    
        return [list_categories, list_category_url]
    except:
        return 'error'

#####################
# extract_items function
#####################

def extract_items(soup_item):
    list_items = []    
    try:
        list_elem = soup_item.find("ol", class_="row").find_all("a")
        def_list = []
        for ls in list_elem:
            knil = ls.get("href").strip("./")
            if knil in def_list:
                continue
            else:
                def_list.append(knil)
        # print(def_list)
        return def_list
    except:
        return 'error'




#####################
# extract_final_data function
#####################

def extract_final_data(soup, site, url):
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
        res["image_url"] = '{}{}'.format(site, '/' + img)



        list_result.append(url)
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
        # print(list_result)
        return list_result
    except:
        return 'error'