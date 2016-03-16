__author__ = 'Eugene'
# -*- coding: utf-8 -*-

import urllib
from bs4 import BeautifulSoup
import csv

root = "http://www.asv.org.ru"
page = urllib.urlopen("http://www.asv.org.ru/liquidation/")
soup = BeautifulSoup(page)
table = soup.find("div", id="tabs_box")
links = table.find_all("a")


#получаем поля
fields = []
for link in links:
    bank = urllib.urlopen(root + link['href'])
    soup = BeautifulSoup(bank)
    bank_table = soup.find("table", class_="statTable f15 genTable")
    for tr in bank_table.find_all("tr"):
        if tr.contents[0].text not in fields:
            fields.append(tr.contents[0].text)


norm_fields = []
for field in fields:
    norm_fields.append(field[:-1].encode("utf-8"))
print norm_fields

#проходим по банкам
with open('database.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=norm_fields, delimiter=';')
    writer.writeheader()

    for link in links:
        row = {}
        bank = urllib.urlopen(root + link['href'])
        soup = BeautifulSoup(bank)
        bank_table = soup.find("table", class_="statTable f15 genTable")
        for tr in bank_table.find_all("tr"):

            row[tr.contents[0].text[:-1].encode("utf-8")] = tr.contents[1].text.encode("utf-8")

        try:
            writer.writerow(row)
        except ValueError:
            for key in row.keys():
                print key.decode("utf-8")



