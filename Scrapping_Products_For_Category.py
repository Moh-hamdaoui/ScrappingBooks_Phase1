import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin,urlparse


def getBook(url):
    baseURL = "https://books.toscrape.com/catalogue/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    absolute_url = baseURL + url
    print(absolute_url)
    response = requests.get(absolute_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.find("h1").text.strip() #title

        tableauInfos = soup.find('table', class_='table table-striped')
        td_infosValues = tableauInfos.find_all('td')
        infosProduct = [td.get_text() for td in td_infosValues]
        upc = infosProduct[0] #UPC
        price_excluding_tax = infosProduct[1] #price_exc_tax
        price_including_tax = infosProduct[2] #price_inc_tax
        number_available = infosProduct[5] #available
        review_rating = infosProduct[6] #review_rating

        getParagraph = soup.find_all('p')
        product_description_avec_tag = getParagraph[3]
        product_description = product_description_avec_tag.get_text() #productDescription

       
        imgage_element = soup.find('img')
        img_url = imgage_element['src'] #URL_image

        ul_category = soup.find('ul', class_='breadcrumb')
        links_a = ul_category.find_all('a')
        category = links_a[2].get_text() #category
        


        data = {'UPC': upc, 'tirle' : title, 'URL': absolute_url, 'Price (excl. tax)': price_excluding_tax, 'Price (incl. tax)': price_including_tax, 'Availability': number_available, 'Number of reviews': review_rating,'Description' : product_description, 'category' : category, 'Image URL' : img_url}
        with open('Product_for_one_category.csv', 'a+', newline='', encoding='utf-8') as fichier_csv:
            writer = csv.DictWriter(fichier_csv, fieldnames=data)
            writer.writerow(data)
            print('Données bien enregistrées!')



headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
urlCategory = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html" #URL
response = requests.get(urlCategory, headers=headers)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    titre_links = soup.find_all('h3')
 
    links = []
    for block in titre_links:
        links.append(block.find('a')['href'])
        
for link in links:
    clean_link = link.replace("../../../", "")
    getBook(clean_link)    