__author__ = 'Eugene'
# -*- coding: utf-8 -*-

import urllib
from bs4 import BeautifulSoup
import csv
import json
import xlwt


"""
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

"""

def get_list_banks_participants(root):

    #получаем поля
    fields = []
    start_page = urllib.urlopen(root)
    soup = BeautifulSoup(start_page)
    table = soup.find("div", class_="alphabetBlocks").find_all("a")
    for i, bank in enumerate(table):
        bank_page = urllib.urlopen("http://www.asv.org.ru/" + bank['href'])
        soup = BeautifulSoup(bank_page)
        bank_info = soup.find("table", class_="statTable f15 genTable").find_all("tr")
        for tr in bank_info:
            if tr.contents[0].text[:-1] not in fields:
                fields.append(tr.contents[0].text[:-1])
        print("Получены поля банка %d" % i)

    """
    for field in fields:
        print field
    """

    #пишем в базу
    wb = xlwt.Workbook()
    ws = wb.add_sheet('list_banks_participants')
    for i, field in enumerate(fields):
        ws.write(0, i, field)

    start_page = urllib.urlopen(root)
    soup = BeautifulSoup(start_page)
    table = soup.find("div", class_="alphabetBlocks").find_all("a")
    j = 1
    for i, bank in enumerate(table):
        bank_page = urllib.urlopen("http://www.asv.org.ru/" + bank['href'])
        soup = BeautifulSoup(bank_page)
        bank_info = soup.find("table", class_="statTable f15 genTable").find_all("tr")
        for tr in bank_info:
            ws.write(j, fields.index(tr.contents[0].text[:-1]),tr.contents[1].text)
        print("В базу записан банк %d" % i)
        j+=1

    wb.save("participants.xls")


list_banks_participants = get_list_banks_participants("http://www.asv.org.ru/insurance/banks_list/")



