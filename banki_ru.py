__author__ = 'Eugene'
#-*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import re
import csv
import os

from multiprocessing import Pool, Process



PROPERTY_ID = {"Высоколиквидные активы": "?PROPERTY_ID=110",
               "Выданные МБК": "?PROPERTY_ID=120",
               "Вложения в акции": "?PROPERTY_ID=130",
               "Вложения в облигации": "?PROPERTY_ID=140",
               "Вложения в векселя": "?PROPERTY_ID=150",
               "Вложения в капиталы других организаций": "?PROPERTY_ID=160",
               "Кредиты ФЛ 0-180": "?PROPERTY_ID=210",
               "Кредиты ФЛ 181-1": "?PROPERTY_ID=220",
               "Кредиты ФЛ 1-3": "?PROPERTY_ID=230",
               "Кредиты ФЛ 3+": "?PROPERTY_ID=240",
               "Овердрафты и прочие средства, предоставленные ФЛ": "?PROPERTY_ID=250",
               "Кредиты ФЛ.Просроченная задолженность": "?PROPERTY_ID=260",
               "Кредиты ПиО  0-180": "?PROPERTY_ID=310",
               "Кредиты ПиО 181-1": "?PROPERTY_ID=320",
               "Кредиты ПиО 1-3": "?PROPERTY_ID=330",
               "Кредиты ПиО 3+": "?PROPERTY_ID=340",
               "Овердрафты и прочие средства, предоставленные ИП": "?PROPERTY_ID=350",
               "Кредиты ПиО.Просроченная задолженность": "?PROPERTY_ID=360",
               "ОС и НА": "?PROPERTY_ID=170",
               "Прочие активы": "?PROPERTY_ID=180",
               "Вклады ФЛ. Счета": "?PROPERTY_ID=410",
               "Вклады ФЛ 0-90": "?PROPERTY_ID=420",
               "Вклады ФЛ 91-180": "?PROPERTY_ID=430",
               "Вклады ФЛ 181-1": "?PROPERTY_ID=440",
               "Вклады ФЛ 1-3": "?PROPERTY_ID=450",
               "Вклады ФЛ 3+": "?PROPERTY_ID=460",
               "Средства ПиО.Счета": "?PROPERTY_ID=510",
               "Средства ПиО 0-90": "?PROPERTY_ID=520",
               "Средства ПиО 91-180": "?PROPERTY_ID=530",
               "Средства ПиО 181-1": "?PROPERTY_ID=540",
               "Средства ПиО 1-3": "?PROPERTY_ID=550",
               "Средства ПиО 3+": "?PROPERTY_ID=560",
               "Привлеченные МБК": "?PROPERTY_ID=600",
               "Выпущенные облигации": "?PROPERTY_ID=710",
               "Выпущенные векселя": "?PROPERTY_ID=720",
               "Капитал (134ф.)": "?PROPERTY_ID=800"
               }


def get_banks_data_by_date(date):

    for property in PROPERTY_ID.keys():

        url = "http://www.banki.ru/banks/ratings/"+PROPERTY_ID[property]+"&date1="+date
        print url
        print("Property: %s" % property.decode("utf-8"))


        with open(date+"/"+property.decode("utf-8")+".csv", "a") as csvfile:

            fieldnames = ["Наименование", "Лицензия", "Регион регистрации", property]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            url = url+"&PAGEN_1=1"
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page)


            if (soup.find("div", class_="ui-pagination__description")) ==  None:
                print("Нет банков по этому показателю")
                pages = 0
                print("Pages: %d" % pages)
            else:
                total_items = int(soup.find("div", class_="ui-pagination__description").contents[5].text)
                print("%d banks" % total_items)

                if total_items%50 <> 0:
                    pages = (total_items//50)+1
                else:
                    pages = total_items//50
                print("Pages: %d" % pages)


            if pages == 0:
                break

            for i in range(pages):

                print("Page number: %d" % (i+1))
                url = url+"&PAGEN_1="+str(i+1)
                page = urllib2.urlopen(url)
                soup = BeautifulSoup(page)
                full_table = soup.find("table", class_="standard-table standard-table--row-highlight margin-bottom-small")
                table = full_table.tbody
                print("+ %d banks" % len(table.find_all("tr")))

                if len(table.find_all("tr")) == 0:
                    break

                for tr in table.find_all("tr"):

                    bank = {}
                    td = tr.find_all("td")
                    bank['Наименование'] = td[1].contents[1].a.text.strip().encode("utf-8")
                    bank['Лицензия'] = re.sub("\D+", "", td[1].contents[3].text).encode("utf-8")
                    bank['Регион регистрации'] = td[1].contents[3].text.split(",")[1].strip().encode("utf-8")
                    bank[property] = re.sub("\s", "", td[2].text).encode("utf-8")
                    writer.writerow(bank)



dates = ["2013-01-01",
       "2013-02-01",
       "2013-03-01",
       "2013-04-01",
       "2013-05-01",
       "2013-06-01",
       "2013-07-01",
       "2013-08-01",
       "2013-09-01",
       "2013-10-01",
       "2013-11-01",
       "2013-12-01",

       "2014-01-01",
       "2014-02-01",
       "2014-03-01",
       "2014-04-01",
       "2014-05-01",
       "2014-06-01",
       "2014-07-01",
       "2014-08-01",
       "2014-09-01",
       "2014-10-01",
       "2014-11-01",
       "2014-12-01",

       "2015-01-01",
       "2015-02-01",
       "2015-03-01",
       "2015-04-01",
       "2015-05-01",
       "2015-06-01",
       "2015-07-01",
       "2015-08-01",
       "2015-09-01",
       "2015-10-01",
       "2015-11-01",
       "2015-12-01"
       ]


if __name__ == '__main__':
    p = Pool()
    for date in dates:
        os.mkdir(date)

    for date in dates:
        p.map(get_banks_data_by_date, dates)
        p.close()
        p.join()

