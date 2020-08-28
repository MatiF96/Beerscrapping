from bs4 import BeautifulSoup
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager


url = 'https://www.ratebeer.com/user/421236/beer-ratings/1/5/'
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

time.sleep(1)

soup = BeautifulSoup(driver.page_source)
dane = []
namesstyles = []
names = []
styles = []
breweries = []

table = soup.findAll("td")
for i in table:
    dane.append(i.get_text())
    j=0
    k=0
    for span in i.findAll("a"):
        if j%2 == 0:
            if k%2 == 0:
                print(k)
                k+=1
            else:
                print(k)
                k+=1
            j+=1
        else:
            breweries.append(span.get_text())
            j+=1

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