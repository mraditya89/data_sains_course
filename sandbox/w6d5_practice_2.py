from urllib import request
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

BASE_URL = 'https://www.newegg.com/p/pl'
KEYWORD = 'Samsung+1TB+SSD'
BASE_URL = f'{BASE_URL}?d={KEYWORD}'

def getNumPage(doc):
    pagination = doc.find('span', class_='list-tool-pagination-text').strong.text.split('/')
    numPage = pagination[1]
    return numPage

def getName(productTag):
    try:
        return productTag.find('a', class_='item-title').text[0:20]
    except Exception as err:
        return None

def getDocument(url):
    request = Request(url)
    response = urlopen(request)
    return BeautifulSoup(response, 'html.parser')

def getPrice(productTag):
    try:
        return float(productTag.find('li', class_='price-current').text.split("(")[0][1:-1:1])
    except Exception as err:
        return None

if __name__ == '__main__':
    doc = getDocument(BASE_URL)
    numPage = int(getNumPage(doc))
    products = []
    for page in range(1,numPage+1):
        url = BASE_URL
        if (page!=1 or doc ==None):
            url = f'{url}&page={page}'
            doc = getDocument(url)
        
        productTags = doc.find_all('div', class_='item-cell')
        # print(type(productTags))
        for product in productTags:
            name = getName(product)
            price = getPrice(product)
            if (name==None or price ==None): continue
            products.append({
                'name' : name, 
                'price' : price 
            })
        
            print(name, f'${price}')

