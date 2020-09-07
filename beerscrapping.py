from bs4 import BeautifulSoup
from selenium import webdriver
import time, math
from webdriver_manager.chrome import ChromeDriverManager


url = 'https://www.ratebeer.com/user/421236/beer-ratings/'
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

time.sleep(1)

soup = BeautifulSoup(driver.page_source)

ratings = int(soup.find("div", class_="stat-value", id="beer-ratings").text)
pages = int(math.ceil(ratings/50))

names = []
styles = []
breweries = []
meanScores = []
myScores = []
dates = []

j, k = 0, 0
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

"""
page = requests.get("https://www.ratebeer.com/user/421236/beer-ratings")
#page = requests.get("https://www.ratebeer.com/top")
soup = BeautifulSoup(page.content, 'html.parser')

dane = []
names = []
styles = []

table = soup.findAll("td")
for i in table:
    dane.append(i.get_text())
    j=0
    for span in i.findAll("a"):
        if j%2 == 0:
            names.append(span.get_text())
            j+=1
        else:
            styles.append(span.get_text())
            j+=1

positions = dane[0::6]
abvs_p = dane[3::6]
abvs = [s.replace('%', '') for s in abvs_p]
scores = dane[4::6]

to_save = []
b=0
for a in positions:
    to_save.append({
     "Position": positions[b],
     "Name": names[b],
     "Style": styles[b],
     "ABV": abvs[b],
     "Score": scores[b]
     })
    b+=1

print (to_save)
"""