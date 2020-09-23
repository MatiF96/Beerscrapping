from bs4 import BeautifulSoup
from selenium import webdriver
import time, math
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import tkinter as tk
from tkinter import messagebox

master = tk.Tk()
master.title('Beerscrapping')
userInput = tk.StringVar(master)
#master.geometry('500x200')
#master.maxsize(500, 200)

'''photo=tk.PhotoImage(file='bg.gif')
bg = tk.Label(master,image = photo)
bg.image = photo # keep a reference!
#bg.grid(row=0,column=0)
bg.place(x=0, y=0, relwidth=1, relheight=1)
main_frame = tk.Frame(master, width=500, height=200)
main_frame.place(x=100, y=110, relx=0.01, rely=0.01)
label1 = tk.Canvas.create_text(10, 10, text="Paste link to your beer ratings list")
label1.pack(side='left', expand=1)
#label1 = tk.Label(master, text='Paste link to your beer ratings list').pack(side='left', expand=1) #.grid(row=0)
'''
def passAndRun():
    link = userInput.get()
    if len(link)==0:
        messagebox.showwarning(title=None, message="Link is empty!")
    else:
        scrapeAndSave(link)
        
label1 = tk.Label(master, text='Paste link to your beer ratings list:').grid(ipady=3)
textbox = tk.Entry(master, textvariable=userInput, width=50).grid()
label2 = tk.Label(master, text='Example: https://www.ratebeer.com/user/421236/beer-ratings/', fg='grey').grid()
button = tk.Button(master, text = "Get and save beer list", command=passAndRun).grid(pady=3)
tk.mainloop()

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
    
    driver.quit()
    
    export = {'Name': names,
            'Brewery': breweries,
            'Style': styles,
            'My score': myScores,
            'Avg score': meanScores,
            'Date': dates
            }
    
    df = pd.DataFrame(export, columns = ['Name', 'Brewery', 'Style', 'My score', 'Avg score', 'Date'])
    df.to_excel ('Beerscrapping.xlsx', index = False, header=True)
    tk.messagebox.showinfo(message="Done!")
    
        