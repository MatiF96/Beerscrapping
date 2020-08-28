from bs4 import BeautifulSoup
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager

# I highly recommend using different libraries than selenium/webdriver - I will recommend some later, just remind me

url = 'https://www.ratebeer.com/user/421236/beer-ratings/1/5/'
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

time.sleep(1)

soup = BeautifulSoup(driver.page_source)
data = []
namesstyles = []
names = []
styles = []
breweries = []

table = soup.findAll("td")
counter = 0
for i in table:
    # 1. Why don't you append whole data in one loop and then iterate later on data only?
    data.append(i.get_text())
    # 2. Here the loop is iterating ~2 times for each loop below
    print('j and k are zeroed')
    j = 0  # 3a. Here there is 0 assign - as it is reference, it is assigned ~2 times each loop below
    k = 0  # 3b. Here there is 0 assign - as it is reference, it is assigned ~2 times each loop below
    # 4. Loop below is called not so often, as there is rarely span items in each <a> element
    for span in i.findAll("a"):
        # 5. Additionaly, you do data.append(i.get_text()) and still i.findAll("a") - just iterate the data itself as told in p.1
        # 6. Here you can actually see how often the counter is called and how often j and k is zeroed
        print('counter: ' + str(counter))
        if j % 2 == 0:
            if k % 2 == 0:
                # print(k)
                k += 1
            else:
                # print(k)
                k += 1
            j += 1
        else:
            breweries.append(span.get_text())
            j += 1
        counter += 1

# """
# page = requests.get("https://www.ratebeer.com/user/421236/beer-ratings")
# #page = requests.get("https://www.ratebeer.com/top")
# soup = BeautifulSoup(page.content, 'html.parser')

# dane = []
# names = []
# styles = []

# table = soup.findAll("td")
# for i in table:
#     dane.append(i.get_text())
#     j=0
#     for span in i.findAll("a"):
#         if j%2 == 0:
#             names.append(span.get_text())
#             j+=1
#         else:
#             styles.append(span.get_text())
#             j+=1

# positions = dane[0::6]
# abvs_p = dane[3::6]
# abvs = [s.replace('%', '') for s in abvs_p]
# scores = dane[4::6]

# to_save = []
# b=0
# for a in positions:
#     to_save.append({
#      "Position": positions[b],
#      "Name": names[b],
#      "Style": styles[b],
#      "ABV": abvs[b],
#      "Score": scores[b]
#      })
#     b+=1

# print (to_save)
# """
