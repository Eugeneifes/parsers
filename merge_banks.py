__author__ = 'Eugene'
#-*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import re
import csv
import os
import pandas
from multiprocessing import Pool, Process



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


def merge_files(date):
    files = os.listdir(date)
    df1 = pandas.read_csv(date+"/"+files[0], dtype={"Лицензия": str})
    df2 = pandas.read_csv(date+"/"+files[1], dtype={"Лицензия": str}, usecols=[1, 3])
    merged = pandas.merge(df1, df2, on="Лицензия", how="inner")
    merged.to_csv(date+".csv", index=False)

    for file in files[2:]:
         df1 = pandas.read_csv(date+".csv", dtype={"Лицензия": str})
         df2 = pandas.read_csv(date+"/"+file, dtype={"Лицензия": str}, usecols=[1, 3])
         merged = pandas.merge(df1, df2, on="Лицензия", how="inner")
         merged.to_csv(date+".csv", index=False)


for date in dates:
    merge_files(date)
