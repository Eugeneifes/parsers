__author__ = 'Eugene'
#-*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import re
import csv
import os


PROPERTY_ID = {"Высоколиквидные активы": "?PROPERTY_ID=110",
               "Выданные МБК": "?PROPERTY_ID=120",
               "Вложения в акции": "?PROPERTY_ID=130",
               "Вложения в облигации": "?PROPERTY_ID=140",
               "Вложения в векселя": "?PROPERTY_ID=150",
               "Вложения в капиталы других организаций": "?PROPERTY_ID=160",
               "Кредиты ФЛ 0-180": "?PROPERTY_ID=210",
               "Кредиты ФЛ 181-1": "?PROPERTY_ID=220",
               "Кредиты ФЛ 1-3": "?PROPERTY_ID=230",
               "Кредиты ФЛ 3-…": "?PROPERTY_ID=240",
               "Овердрафты и прочие средства, предоставленные ФЛ": "?PROPERTY_ID=250",
               "Кредиты ФЛ.Просроченная задолженность": "?PROPERTY_ID=260",
               "Кредиты ПиО  0-180": "?PROPERTY_ID=310",
               "Кредиты ПиО 181-1": "?PROPERTY_ID=320",
               "Кредиты ПиО 1-3": "?PROPERTY_ID=330",
               "Кредиты ПиО 3-…": "?PROPERTY_ID=340",
               "Овердрафты и прочие средства, предоставленные ИП": "?PROPERTY_ID=350",
               "Кредиты ПиО.Просроченная задолженность": "?PROPERTY_ID=360",
               "ОС и НА": "?PROPERTY_ID=170",
               "Прочие активы": "?PROPERTY_ID=180",
               "Вклады ФЛ. Счета": "?PROPERTY_ID=410",
               "Вклады ФЛ 0-90": "?PROPERTY_ID=420",
               "Вклады ФЛ 91-180": "?PROPERTY_ID=430",
               "Вклады ФЛ 181-1": "?PROPERTY_ID=440",
               "Вклады ФЛ 1-3": "?PROPERTY_ID=450",
               "Вклады ФЛ 3-..": "?PROPERTY_ID=460",
               "Средства ПиО.Счета": "?PROPERTY_ID=510",
               "Средства ПиО 0-90": "?PROPERTY_ID=520",
               "Средства ПиО 91-180": "?PROPERTY_ID=530",
               "Средства ПиО 181-1": "?PROPERTY_ID=540",
               "Средства ПиО 1-3": "?PROPERTY_ID=550",
               "Средства ПиО 3-..": "?PROPERTY_ID=560",
               "Привлеченные МБК": "?PROPERTY_ID=600",
               "Выпущенные облигации": "?PROPERTY_ID=710",
               "Выпущенные векселя": "?PROPERTY_ID=720",
               "Капитал (134ф.)": "?PROPERTY_ID=850"
               }


date1 = "2008-03-01"
#date2 = "2008-03-01"


def get_banks_data_by_date(date):

    if os.path.exists(date):
        os.rmdir(date)

    os.mkdir(date)

    #получаем информацию по каждому показателю
    for key in PROPERTY_ID.keys():

        url = "http://www.banki.ru/banks/ratings/"+PROPERTY_ID[key]+"&date1="+date
        print url
        page_count = 1
        Licenses = []
        flag = True

        with open(date+"/"+key.decode("utf-8")+".csv", "a") as csvfile:

            fieldnames = ["Наименование", "Лицензия", "Показатель"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            #Итерируем, пока не пошли те же самые банки (хз как обработать ответ сервера, эта падла возвращает 200ок)
            while(flag == True):
                print("Page number: %s" % page_count)
                url = url+"&PAGEN_1="+str(page_count)
                page = urllib2.urlopen(url)
                soup = BeautifulSoup(page)
                full_table = soup.find("table", class_="standard-table standard-table--row-highlight margin-bottom-small")
                table = full_table.tbody
                print("+ %d banks" % len(table.find_all("tr")))

                if len(table.find_all("tr")) == 0:
                    flag=False
                    break

                for tr in table.find_all("tr"):

                    bank = {}
                    td = tr.find_all("td")
                    License = re.sub("\D+", "", td[1].contents[3].text.encode("utf-8"))

                    #Признак конца итерации - пошли те же лицензии
                    if License in Licenses:
                        print("Banks in total: %s" % len(Licenses))
                        flag = False
                        print("\n")
                        break
                    else:
                        Licenses.append(License)


                    bank['Наименование'] = re.sub("^\s+|\s+$", "", td[1].contents[1].a.text.encode("utf-8"))
                    bank['Лицензия'] = re.sub("\D+", "", td[1].contents[3].text.encode("utf-8"))
                    bank['Показатель'] = re.sub("\s", "", td[2].text.encode("utf-8"))
                    writer.writerow(bank)

                page_count += 1


get_banks_data_by_date(date1)