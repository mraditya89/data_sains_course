import csv
from datetime import datetime

import requests
from bs4 import BeautifulSoup

months = {
    "Jan": 1, 
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "Mei": 5,
    "Jun": 6,
    "Jul": 7,
    "Agu": 8, 
    "Sep": 9, 
    "Okt": 10, 
    "Nov": 11,
    "Des": 12 
}

class DetikCrawl:
    baseUrl = "https://www.detik.com"

    def __init__(self, query, startDate=datetime.now(), endDate=datetime.now()):
        self.page = 1
        self.url = f"{DetikCrawl.baseUrl}/tag/{query}/?sortby=time"
        self.startDate = self.resetTime(startDate)
        self.endDate = self.resetTime(endDate)
        self.getNewsList()
        self.getNewsDetail()

    def resetTime(self, dateTime):
        return dateTime.replace(hour=0,minute=0,second=0)
        
    def getTitleFromNewsList(self, articleTag):
        return articleTag.find("h2", class_="title").text
    
    def getDateFromNewsList(self, articleTag):
        dateText = articleTag.find("span", class_="date").text.split(",")[-1].strip().replace(" WIB", "")
        splittedDateText = dateText.split()
        date  = int(splittedDateText[0])
        month = months[splittedDateText[1]]
        year = int(splittedDateText[2])
        return datetime(year, month, date, 0, 0, 0)

    def log(self, text):
        print(f"[script] {datetime.now()}: {text}")

    def writeToCsv(self, data):
        self.log("write to file")
        with open('./news_list.csv', "w", encoding='UTF-8', newline="") as f:
            writer = csv.writer(f)
            header = ["created_at", "title", "link", "article"]
            writer.writerow(header)
            writer.writerows(data)

    def getNewsList(self):
        isLoop = True
        page = 1
        self.news=[]

        while isLoop:
            self.log(f"crawling page-{page}")
            response = requests.get(f"{self.url}&page={page}")
            soup = BeautifulSoup(response.text, 'html.parser')
            articleTags = soup.find_all("article")

            latestDate = self.getDateFromNewsList(articleTags[0])
            oldestDate = self.getDateFromNewsList(articleTags[-1])

            if (oldestDate > self.endDate):
                # move to next page
                self.log("move to next page")
                page+= 1
                continue
            elif (latestDate < self.startDate):
                self.log("break")
                break
            
            for article in articleTags:
                title = self.getTitleFromNewsList(article)
                createdAt = self.getDateFromNewsList(article)
                link = article.find("a")['href']
                if (self.startDate<=createdAt and self.endDate>=createdAt):
                    self.news.append([
                        createdAt,
                        title, 
                        link
                    ])

            page += 1
            if page==10: break           


    def getNewsDetail(self):
        for idx, data in enumerate(self.news):
            self.log(f"fetching {data[1]}")
            article=""
            response = requests.get(data[2])
            soup = BeautifulSoup(response.text, 'html.parser')
            bodyText = soup.find("div", class_="detail__body-text")

            paragraphs = bodyText.find_all("p")

            for paragraph in paragraphs:
                article = f"{article}{paragraph.text}\n"
            self.news[idx].append(article)

        self.writeToCsv(self.news)    


doc = DetikCrawl(
    query="ppkm", 
    startDate=datetime(2021,12,6), 
    endDate=datetime(2021,12,6)
)
