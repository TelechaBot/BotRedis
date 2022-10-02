# -*- coding: utf-8 -*-
# @Time    : 10/1/22 10:41 PM
# @FileName: moondgb.py
# @Software: PyCharm
# @Github    ：sudoskys
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["runoobdb"]
mycol = mydb["sites"]

for x in mycol.find():
    print(x)
