"""
                            COVID TRACKER

    A Mini Project made on 10 April 2021 by Siva Kumar(212218104154).
    this project is used to observe the daily count of corona virus
    cases happening all around the world sorted by every country.
    this applicationreturns all the numerical count of cases,
    recovery, deaths and many more.


"""
from tkinter import ttk
from tkinter import *
import time
import requests
from bs4 import BeautifulSoup


class Scraper:

    def __init__(self):
        # scrape the webpage using request module of worldmeter website

        file = requests.get('https://www.worldometers.info/coronavirus/')
        self.soup = BeautifulSoup(file.text, 'html.parser')
        file.close()
        class_name = 'table table-bordered table-hover main_table_countries'
        id_name = 'main_table_countries_today'
        self.country_table = self.soup.find(
            'table', class_=class_name, id=id_name)

    def header_list(self):
        self.header_list = self.country_table.findAll('th')
        return (list(map(lambda a: a.text.replace('/xa0', ''), self.header_list)))

    def show_total_world_cases(self):
        # return the total world cases in numbers
        self.total_world_cases = self.soup.findAll(
            'div', class_='maincounter-number')
        total_covid_count = []
        for values in self.total_world_cases:
            total_covid_count.append((values.text).strip('\n'))
        return total_covid_count

    def list_of_countries(self):
        """this function is used to get the values and countries
        in a form of list to store the data"""

        self.total_country_rows = self.country_table.tbody.findAll('tr')
        self.country_list = []
        for i in range(8, len(self.total_country_rows)):
            self.country_list.append(
                self.total_country_rows[i].findAll('td')[1].text)
        return self.country_list

    def show_specific_continent(self, user_input):
        """this function fetches the list of continent math values
        to the user in a list"""
        total_data = self.total_country_rows[self.country_list.index(
            user_input)].findAll('td')
        specific_country_data = []
        for j in range(2, 19):
            specific_country_data.append(
                f"{total_data[j].string}")
        return specific_country_data


class Tk_Screen:
    def __init__(self, master):
        '''Creating an Application for visualising the processed data'''
        self.master = master
        self.master.geometry('600x600+400+100')
        self.master.title('covid tracker')
        self.master.config(bg='grey')
        self.master.resizable(False, False)

        # frame for mainscreen
        Label(self.master, text='CORONAVIRUS TRACKER',
              width='37', height='2',
              font=('timesnewroman bold', 20), bg='grey').place(x=0, y=0)

        self.frame1 = Frame(self.master, width=400, height=200, bg='grey',
                            relief='groove', bd='2')
        self.frame1.place(x=100, y=200)

        Label(self.frame1, text='An internet connection is required to run this script',
              bg='grey').place(x=60, y=10)
        Label(self.frame1, text='click ok to start the script',
              bg='grey', font='10').place(x=80, y=50)

        self.progress = ttk.Progressbar(self.frame1, orient='horizontal',
                                        length=240, mode='determinate')

        Button(self.frame1, text='ok', activebackground='green', width='10',
               command=lambda: Tk_Screen.start_progress(self)).place(x=150, y=100)

        self.progress.place(x=75, y=140)

    def start_progress(self):
        # function for webscraping progress
        self.progress['value'] = 30
        self.master.update_idletasks()
        self.example = Scraper()
        if self.example.__init__ is None:
            self.master.messagebox.showerror(
                'error', 'connect to the internet')
            self.master.destroy()
        else:
            self.progress['value'] = 65
            self.master.update_idletasks()
            time.sleep(1)
            self.progress['value'] = 100
            self.master.update_idletasks()
            time.sleep(1)
            self.frame1.destroy()
            Tk_Screen.display_total_count(self)
            Tk_Screen.create_display_components(self)

    def display_total_count(self):
        # display the total covid count
        self.frame2 = Frame(self.master, width=440, height=120,
                            bg='grey', bd='1', relief='raised')
        self.frame2.place(x=80, y=70)
        Label(self.frame2, text='Total cases: ', bg='grey').place(x=110, y=10)
        Label(self.frame2, text='Deaths: ', bg='grey').place(x=110, y=30)
        Label(self.frame2, text='Recovered: ', bg='grey').place(x=110, y=50)

        Label(self.frame2,
              text=f'{self.example.show_total_world_cases()[0]}',
              bg='grey').place(x=240, y=10)
        Label(self.frame2,
              text=f'{self.example.show_total_world_cases()[1]}',
              bg='grey').place(x=240, y=30)
        Label(self.frame2,
              text=f'{self.example.show_total_world_cases()[2]}',
              bg='grey').place(x=240, y=50)

    def create_display_components(self):
        # selection of various countries in the combobox
        self.frame3 = Frame(self.master, width=400, bg='grey',
                            height=380, bd=1, relief='groove')
        self.frame3.place(x=100, y=210)
        # creating combobox
        self.cmbo = ttk.Combobox(
            self.frame3, values=self.example.list_of_countries(),
            state='readonly')
        self.cmbo.current(0)
        self.cmbo.place(x=130, y=10)

        # creating select button
        Button(self.frame3, text='select',
               command=lambda: Tk_Screen.show_numbers(self)).place(x=170, y=40)

        # creating display labels
        self.label_listed_values = [Label(self.frame3, width='10', bg='grey')
                                    for i in range(11)]
        label_list = self.example.header_list()
        y_pos = 50
        for i in range(2, 13):
            y_pos += 25
            Label(self.frame3, text=f'{label_list[i]}', bg='grey').place(
                x=40, y=y_pos)
            self.label_listed_values[i - 2].place(x=280, y=y_pos)

    def show_numbers(self):
        # display the values for the selected country
        value = self.example.show_specific_continent(self.cmbo.get())
        for i in range(11):
            self.label_listed_values[i].config(text='{}'.format(value[i]))


if __name__ == '__main__':
    # running the main function
    mainscreen = Tk()
    window_object = Tk_Screen(mainscreen)
    mainscreen.mainloop()
