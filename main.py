import requests
from bs4 import BeautifulSoup
import csv342 as csv

site = "http://books.toscrape.com"
url = "http://books.toscrape.com/catalogue/sharp-objects_997/index.html"

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

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

list_result = [url, res["UPC"], res["title"]]
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


with open('./data/data.csv', 'w') as file_csv:
    writer = csv.writer(file_csv, delimiter='|')
    writer.writerow(en_tete)
    writer.writerow(list_result)