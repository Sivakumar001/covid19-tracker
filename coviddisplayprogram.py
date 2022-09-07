from tkinter import ttk
from tkinter import *
from scraper import Scraper

mainscreen = Tk()
mainscreen.geometry("600x600")
mainscreen.title("coronavirus tracker")
mainscreen.config(bg='grey')
# screen contents
Label(mainscreen, text="CORONAVIRUS TRACKER",
      font="arial 24 bold", bg='grey').pack()

scraped_data = Scraper()
# combobox to show list of continents
input_data = ttk.Combobox(
    mainscreen, values=scraped_data.list_of_countries(), state="readonly")

input_data.current(0)

list1 = Listbox(mainscreen, width=28)


def show_lists():
    list1.delete(0, END)
    for j in range(1, 14):
        list1.insert(END, scraped_data.show_specific_continent(
            input_data.get())[j])


list1.pack()
input_data.pack()
Button(mainscreen, text='ok', command=show_lists).pack()


mainscreen.mainloop()
