# import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk


class Scraper:
    def __init__(self):
        """i have made a offline file inorder to experiment with the offline
         data instead of importing requests frequently"""
        file = open('rename.html', 'r').read()
        self.soup = BeautifulSoup(file, 'html.parser')
        self.table = self.soup.find(
            'table',
            class_='table table-bordered table-hover main_table_countries',
            id='main_table_countries_today')
        self.maindata = self.soup.find()

    def table_header_values(self):
        """this function is used to get title values
        like totalcases/ no of deaths etc"""
        self.header_values = []
        for values in self.table.thead.findAll('th'):
            self.header_values.append(values.text)

    def table_dict_continents(self):
        """this function is used to get the values and countries
        in a form of dictionary to store the data"""
        continental_value = self.table.findAll(
            'tr', class_='total_row_world row_continent')
        self.continents = {}  # dictionary set here
        for values in continental_value:
            self.continents[values.nobr.text] = [
                i.text for i in values.findAll('td')]

    def show_specific_continent(self, userinput):
        """this function fetches the list of continent math values
        to the user in a list"""
        if userinput in self.continents.keys():
            list1.delete(0, END)
            for _ in range(2, 10):
                value = f"{self.header_values[_]}    :    {self.continents[userinput][_]}"
                list1.insert(END, value)
        else:
            print('enter the valid continent name')

    def list_continents_in_combo(self):
        """this function is used to display continents in a combo box"""
        list_of_continents = []
        for v in self.continents.keys():
            list_of_continents.append(v)
        return list_of_continents


example = Scraper()
example.table_header_values()
example.table_dict_continents()

mainscreen = Tk()
mainscreen.geometry("400x400")
mainscreen.title("coronavirus tracker")
# screen contents
Label(mainscreen, text="covid tracker", font="arial 24 bold").pack()
# data is given here
input_data = ttk.Combobox(
    mainscreen, values=example.list_continents_in_combo(), state="readonly")
input_data.current(1)
input_data.pack()

list1 = Listbox(mainscreen, width=28)
list1.pack()
Button(mainscreen, text="okay", foreground="blue",
       command=lambda: example.show_specific_continent(input_data.get())).pack()

mainscreen.mainloop()
