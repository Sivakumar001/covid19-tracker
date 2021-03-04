import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter.ttk import *
# import time


def webscraper():
    searchurl = "https://www.worldometers.info/coronavirus/"
    html = requests.get(searchurl)
    soup = BeautifulSoup(html.text, "html.parser")
    table_value = soup.findAll('div', {'class': 'maincounter-number'})
    html.close()
    return table_value


window = Tk()
window.title("covid tracker")
window.geometry("500x500")
Label(window, text="covid tracker", font="aria 24").pack(fill=Y)
Label(window, text="total no of cases: ").pack(fill=X)
Label(window, text=f"{webscraper()[0].text}").pack()
Label(window, text="total no of deaths: ").pack(fill=X)
Label(window, text=webscraper()[1].text).pack()
Label(window, text="total no of recoverey: ").pack(fill=X)
Label(window, text=webscraper()[2].text).pack()
# progress = Progressbar(window, orient=HORIZONTAL,
#                        length=300, mode='indeterminate')
# progress.pack(expand=True)
# progress['value'] = 5
# time.sleep(5)
# progress['value'] = 20
# print(webscraper())
# progress['value'] = 60
# time.sleep(2)
# progress['value'] = 100
window.mainloop()
