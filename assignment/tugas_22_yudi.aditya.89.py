from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd

class Crawl:
  def __init__(self, url, agent):
    request = Request(url, headers={
	    'user-agent': agent, 
	    'content-type': 'text/html; charset=utf-8'
	  })
    self.__page = urlopen(request)
    self.__soup = BeautifulSoup(self.__page, 'html.parser')
    self.__topNews = []

  def getTopNews(self, n=10):
    result = self.__soup.find_all('div', class_='most__list')

    for new in result:
      if (len(self.__topNews)==n) : break
      self.__topNews.append(new.find('h4').text)
  
  def showTopNews(self, truncated=True):
    if (not truncated) : 
      pd.set_option('display.max_colwidth', None)
    df = pd.DataFrame(self.__topNews, columns =["Judul Berita Populer"])
    print(df)


if __name__ == "__main__":
  
  AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
  URL = 'https://www.kompas.com/'
  
  kompas = Crawl(URL, AGENT)
  kompas.getTopNews()
  kompas.showTopNews()
