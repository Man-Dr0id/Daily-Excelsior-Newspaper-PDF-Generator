from PyPDF2 import PdfFileMerger
import requests
import datetime
import os
from fnmatch import fnmatch
import subprocess
import glob

#Getting our last page via bs4 scraping

# importing the modules
import requests
from bs4 import BeautifulSoup
  
# providing url
url = "https://epaper.dailyexcelsior.com/"
  
# creating requests object
html = requests.get(url).content
  
# creating soup object
soup = BeautifulSoup(html, 'html.parser')
  
# finding all <li> tags
#Finds the number of proterty Listed
all=soup.find_all("div", {"class":"innercontent"})
x=all[0]
li = x.find_all("li")
 
# printing the content in <li> tag
#last page finding
lastpage=(li[-1].text)


today = datetime.date.today()
year=today.year
day=today.day

#Get Todays Month
month=today.strftime("%b")

#Lowercased the Month
lowmonth=month.lower()

#Formatted date to two digit yearstyle
dateFormatted = today.strftime("%y")
yeartwo=("{}".format(dateFormatted))

#FileName
title_file=(f"{day}-{month}-{yeartwo}")

if day in range(1,10):
    day= ("0"+ str(day))

#Website Source URL
web = ("https://epaper.dailyexcelsior.com/epaperpdf/")
urls = [f"{web}{year}/{lowmonth}/{yeartwo}{lowmonth}{day}/page{x}.pdf" for x in range(1,int(lastpage))]
direct= os.getcwd()

def merger():
    merger = PdfFileMerger()
    for url in urls:
        response = requests.get(url)
        title = url.split("/")[-1]
        date = url.split("/")[-2]
        with open(title, 'wb') as f:
            f.write(response.content)
        merger.append(title)

    merger.write(f"{direct}\{title_file} Excelsior Newspaper.pdf")
    merger.close()

#Deleting merged Files 
def delmerger():
    for filename in glob.glob(".\page*"):
        os.remove(filename) 

#opening pdf
def openmerger():
    subprocess.Popen([f"{direct}\{title_file} Excelsior Newspaper.pdf"],shell=True)

#Deleting prev
def old_delete(): 
    for filename in glob.glob("*.pdf"):
        os.remove(filename) 


def merged():
    old_delete()
    merger()
    delmerger()
    openmerger()

#TKinter

import threading
from tkinter import Button, Tk, HORIZONTAL
from tkinter.ttk import Progressbar
from tkinter import *

class NewsApp(Tk):
    def __init__(self):
        super().__init__()

        self.btn = Button(self, text='Read Newspaper Now', command=self.downloadmethod)
        self.btn.place(x=40,y=10)
        self.progress = Progressbar(self, orient=HORIZONTAL, length=140, mode='indeterminate')

    def downloadmethod(self):
        def real_downloadmethod():
            text = Label(self, text="Please Wait Few Seconds")
            text.place(x=33,y=80)
            self.progress.place(x=34,y=50)
            self.progress.start()
            merged()
            self.progress.stop()
            self.progress.grid_forget()

            self.btn['state']='normal'
            text = Label(self, text="Done Processing !")
            text.place(x=33,y=100)

        self.btn['state']='disabled'
        threading.Thread(target=real_downloadmethod).start()


if __name__ == '__main__':
    app = NewsApp()
    app.title("Excelsior PDF Generator") 
    app.geometry("200x200")
    app.mainloop()