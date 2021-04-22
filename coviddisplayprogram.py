from tkinter import ttk
from tkinter import *
from scraper import Scraper
import time
import requests
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self):
        file = requests.get('https://www.worldometers.info/coronavirus/')
        # file = open('rename.html', 'r').read()
        self.soup = BeautifulSoup(file.text, 'html.parser')
        file.close()
        self.country_table = self.soup.find(
            'table',
            class_='table table-bordered table-hover main_table_countries',
            id='main_table_countries_today')

    def show_total_world_cases(self):
        self.total_world_cases = self.country_table.findAll(
            'div', class_='maincounter-number')
        for values in self.total_world_cases:
            print(values.text)

    def list_of_countries(self):
        """this function is used to get the values and countries
        in a form of list to store the data"""
        self.key_title = [
            value.text for value in self.country_table.thead.findAll('th')]
        self.total_country_rows = self.country_table.tbody.findAll('tr')
        self.country_list = []
        for i in range(8, len(self.total_country_rows)):
            self.country_list.append(
                self.total_country_rows[i].findAll('td')[1].text)
        return self.country_list

    def show_specific_continent(self, user_input):
        """this function fetches the list of continent math values
        to the user in a list"""
        total_data = self.total_country_rows[8 + self.country_list.index(
            user_input)].findAll('td')
        specific_country_data = []
        for j in range(1, 15):
            specific_country_data.append(
                f"{self.key_title[j]} - {total_data[j].text}")
        return specific_country_data


class Tk_Screen:
    def __init__(self, master):
        self.master = master
        self.master.geometry('600x600')
        self.master.title('covid tracker')
        self.master.config(bg='grey')

        Label(self.master, text='''An internet connection is required
              to run this script''', fg='red', bg='grey').pack()
        Label(self.master, text='click ok to start the script',
              bg='grey').pack()

        self.progress = ttk.Progressbar(self.master, orient='horizontal',
                                        length=200, mode='determinate')

        Button(self.master, text='ok', activebackground='green',
               command=lambda: Tk_Screen.start_progress(self)).pack()

        self.progress.pack()

    def start_progress(self):
        self.progress['value'] = 30
        self.master.update_idletasks()
        self.example = Scraper()
        self.progress['value'] = 65
        self.master.update_idletasks()
        time.sleep(1)
        self.progress['value'] = 100
        self.master.update_idletasks()
        time.sleep(1)
        self.progress.destroy()
        Tk_Screen.display_total_count(self)
        Tk_Screen.country_selector_function(self)
        Tk_Screen.show_numbers(self)

    def display_total_count(self):
        Label(self.master, text='total cases: ', bg='grey').pack()
        Label(self.master, text='deaths: ', bg='grey').pack()
        Label(self.master, text='recovered: ', bg='grey').pack()
        for _ in range(3):
            Label(self.master,
                  text=f'{self.example.show_total_world_cases()[_]}',
                  bg='grey').pack()

    def country_selector_function(self):
        self.cmbo = ttk.Combobox(
            self.master, values=self.example.list_of_countries(),
            state='readonly')
        self.cmbo.current(0)
        self.cmbo.pack()
        Button(self.master, text='select',
               command=lambda: Tk_Screen.show_numbers(self)).pack()
        for i in range(1, 18):
            Label(self.master, text=f'{self.example.key_title[i]}').pack()

    def show_numbers(self):
        for i in range(17):
            value = self.example.show_specific_continent(self.cmbo.get())[i]
            value_label = Label(self.master, text='{}'.format(value))
            value_label.pack(side='right')


if __name__ == '__main__':
    mainscreen = Tk()
    window_object = Tk_Screen(mainscreen)
    mainscreen.mainloop()
