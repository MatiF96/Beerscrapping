from bs4 import BeautifulSoup
from selenium import webdriver
import time, math
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

names = []
styles = []
breweries = []
meanScores = []
myScores = []
dates = []

driver = webdriver.Chrome(ChromeDriverManager().install())

url = 'https://www.ratebeer.com/user/421236/beer-ratings/'
driver.get(url)

time.sleep(1)

soup = BeautifulSoup(driver.page_source)

ratings = int(soup.find("div", class_="stat-value", id="beer-ratings").text)
pages = int(math.ceil(ratings/50))


for currentPage in range(pages):
    
    currentUrl = url+str(currentPage+1)+'/'
    driver.get(currentUrl)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source)
    j = 0
    k = 0
    firstName, firstBrewery = True, True
    for num in soup.findAll("td", class_="hidden-xs hidden-sm"):
        if j%3 == 1:
            meanScores.append(num.get_text())
            j+=1
        elif j%3 == 2:
            dates.append(num.get_text()[:-1])
            j+=1
        else:
            styles.append(num.get_text())
            j+=1
    
    for i in soup.findAll("td"):
        for my in i.findAll("b"):
            myScores.append(my.get_text())
        for span in i.findAll("a"):
            if k%3 == 1:
                if firstName:
                    firstName = False
                    k+=1
                else:
                    names.append(span.get_text())
                    k+=1
            elif k%3 == 2:
                if firstBrewery:
                    firstBrewery = False
                    k+=1
                else:
                    breweries.append(span.get_text())
                    k+=1
            else:
                k+=1

export = {'Name': names,
        'Brewery': breweries,
        'Style': styles,
        'My score': myScores,
        'Avg score': meanScores,
        'Date': dates
        }

df = pd.DataFrame(export, columns = ['Name', 'Brewery', 'Style', 'My score', 'Avg score', 'Date'])
df.to_excel ('Beerscrapping.xlsx', index = False, header=True)