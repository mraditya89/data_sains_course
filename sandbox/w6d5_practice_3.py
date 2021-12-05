import requests
from bs4 import BeautifulSoup


class PRCrawl:
    __baseUrl = "https://www.pikiran-rakyat.com"
    __pageLimit = 10        

    def __init__(self, category, numPage=1):
        self.__url = f"{PRCrawl.__baseUrl}/{category}"
        self.__numPage = numPage if numPage<= PRCrawl.__pageLimit else PRCrawl.__pageLimit
        self.__getTitleList()
        self.__mainDocs = []
    
    def __getTitleList(self):
        for idx in range(self.__numPage):
            page = idx+1
            response = requests.get(f"{self.__url}?page={page}" )
            self.__mainDocs.append(
                BeautifulSoup(response.text, 'html.parser')
            )
            


            




        # response = requests.get(url)
        # self.__doc = BeautifulSoup(response.text, 'html.parser')
    

doc = PRCrawl("nasional", numPage=2)

