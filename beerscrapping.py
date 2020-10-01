from bs4 import BeautifulSoup
from selenium import webdriver
import time, math
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import tkinter as tk
from tkinter import messagebox

def passAndRun():
    link = userInput.get()
    if len(link) == 0:
        messagebox.showwarning(title=None, message="Link is empty!")
    else:
        try:
            scrapeAndSave(link)
        except Exception as e: 
            messagebox.showerror(title=None, message="Link is not correct!")
            print(e)
            
def paste():
    clipboard = master.clipboard_get()
    userInput.set(clipboard)

def scrapeAndSave(url):
    names = []
    styles = []
    breweries = []
    meanScores = []
    myScores = []
    dates = []
    
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    
    time.sleep(1)
    
    soup = BeautifulSoup(driver.page_source)
    
    ratings = int(soup.find("div", class_="stat-value", id="beer-ratings").text)
    pages = int(math.ceil(ratings / 50))
      
    for currentPage in range(pages):        
        currentUrl = url + str(currentPage + 1) + '/'
        driver.get(currentUrl)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source)
        j = 0
        k = 0
        firstName, firstBrewery = True, True
        for num in soup.findAll("td", class_="hidden-xs hidden-sm"):
            if j % 3 == 1:
                meanScores.append(num.get_text())
                j += 1
            elif j % 3 == 2:
                dates.append(num.get_text()[:-1])
                j += 1
            else:
                styles.append(num.get_text())
                j += 1        
        for i in soup.findAll("td"):
            for my in i.findAll("b"):
                myScores.append(my.get_text())
            for span in i.findAll("a"):
                if k % 3 == 1:
                    if firstName:
                        firstName = False
                        k += 1
                    else:
                        names.append(span.get_text())
                        k += 1
                elif k % 3 == 2:
                    if firstBrewery:
                        firstBrewery = False
                        k += 1
                    else:
                        breweries.append(span.get_text())
                        k += 1
                else:
                    k += 1
    
    driver.quit()
    export = {'Name': names,
            'Brewery': breweries,
            'Style': styles,
            'My score': myScores,
            'Avg score': meanScores,
            'Date': dates
            }
    
    df = pd.DataFrame(export, columns = ['Name', 'Brewery', 'Style', 'My score', 'Avg score', 'Date'])
    df.to_excel ('Beerscrapping.xlsx', index = False, header = True, encoding= 'mac_roman')
    messagebox.showinfo(message="Done!")

master = tk.Tk()
master.title('Beerscrapping')
userInput = tk.StringVar(master)
     
label1 = tk.Label(master, text='Paste link to your beer ratings list:').grid(row = 0, column = 0, ipady = 3)
textbox = tk.Entry(master, textvariable = userInput, width = 50).grid(row = 1, column = 0)
pasteButton = tk.Button(master, text = "Paste", command = paste, width = 5).grid(row = 1, column = 1, padx = 5)
label2 = tk.Label(master, text = 'Example: https://www.ratebeer.com/user/421236/beer-ratings/', fg = 'grey').grid(row = 2, column = 0)
button = tk.Button(master, text = "Get and save beer list", command = passAndRun).grid(row = 3, column = 0, pady = 3)

tk.mainloop()     