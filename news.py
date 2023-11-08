import requests
from bs4 import BeautifulSoup

def getNewsTitles():
    r = requests.get("https://www.bart.gov/news/articles")
    soup = BeautifulSoup(r.text, "html.parser")

    d = []

    for article in soup.find_all("div", {"class": "views-row"}):
        try:
            dateText = article.find("span", {"class": "views-field views-field-field-news-date"}).text.strip()
            title = article.find("a").text.strip()
            url = "https://www.bart.gov" + article.find_all("a")[1].get("href")

            d.append({"date": dateText, "title": title, "url": url})
        except:
            fds = ""
    return d

print(getNewsTitles())