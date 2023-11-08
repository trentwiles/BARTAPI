import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

def getTitles(endpoint):
    r = requests.get(endpoint)
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

def getLatestTitles():
    return getTitles("https://www.bart.gov/news/articles")

def getTitlesByYear(year):
    return getTitles(f"https://www.bart.gov/news/articles/{str(year)}")

def getArticleContent(link):
    # 
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "html.parser")


    # add https://www.bart.gov in front of each URL
    # we are assuming the rendered markdown/html will not be displayed on BART's website
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and not href.startswith('http'):
            link['href'] = 'https://www.bart.gov' + href

    rawL = soup.find("div", {"class": "field field--field-legacy-body-content field--string-long"}).contents
    raw = ""
    for x in rawL:
        if x != "\n":
            raw += str(x)

    return {"title": soup.title.text, "date": soup.find("div", {"class": "field field--field-news-date field--datetime"}).text.strip(), "html": raw, "markdown": md(raw)}