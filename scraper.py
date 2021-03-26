import requests
from bs4 import BeautifulSoup
import re


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

    def graphical_data(self):
        # 377 html code line 7 or 10
        # data regex ""data: \[((\d+,?)+)\]""
        # categories regex ""categories: \[(\"(\w{3}\s\d{2}),(\s\d{4})+\",?)+\]""
        data_text = self.soup.findAll('script', type='text/javascript')
        # sphagetti code for x axis in graph
        re_data = re.compile(r"data: \[(.*)\]")
        throwaway_substring = re.search(re_data, data_text[7].string)

        x_data_matches = re.finditer(r"\d+", throwaway_substring.group(1))
        x_axis = []
        for match in x_data_matches:
            x_axis.append(int(match.group()))
        # for y axis
        re_dates = re.compile(
            r"categories: \[(.*)\]")
        throwaway_substring_y = re.search(re_dates, data_text[7].string)
        y_data_matches = re.finditer(
            r"(\"(\w{3}\s\d{2},\s\d{4})+\")+", throwaway_substring_y.group())
        y_axis = []
        for match in y_data_matches:
            y_axis.append(match.group(2))
        return x_axis, y_axis
