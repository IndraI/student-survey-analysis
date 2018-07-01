from pathlib import Path

import pdfquery
import numpy as np
from pymongo import MongoClient


def getItems(pdf,inbox):
    items = pdf.pq('LTTextLineHorizontal:in_bbox("%s")' % inbox)
    items.sort(key=lambda i: i.attrib["x0"])
    try:
        res = [int(i.text.strip()) for i in items]
    except ValueError as err:
        res = []
        print(err)
    return res

def enquesta(path):
    pdf = pdfquery.PDFQuery(path,normalize_spaces=False,resort=False)
    pdf.load(0)

    dict = pdf.extract([#('with_parent','LTPage[pageid=1]'),
                 ('with_formatter', 'text'),
                 ('year',  'LTTextLineHorizontal:in_bbox("195,802,279,825")'),
                 ('semester',  'LTTextLineHorizontal:in_bbox("195,774,279,801")',lambda match: int(match.text()[0])),
                 ('professor', 'LTTextLineHorizontal:in_bbox("35,670,246,700")'),
                 ('assignatura', 'LTTextLineHorizontal:in_bbox("35,627,193,661")'),
                 ('grup', 'LTTextLineHorizontal:in_bbox("215,627,246,661")'),
                 ('grau', 'LTTextLineHorizontal:in_bbox("35,587,246,620")'),
                 ('matriculats', 'LTTextLineHorizontal:in_bbox("200,515,246,535")',lambda match: int(match.text())),
                 ('numenquestes', 'LTTextLineHorizontal:in_bbox("200,487,246,508")',lambda match: int(match.text())),
     ],as_dict=True)


    print(dict)
    dict["item1"] = getItems(pdf,"275,357,528,373")
    print(dict["item1"])
    assert(len(dict["item1"]) > 0)
    dict["item2"] = getItems(pdf,"275,325,528,342")
    assert(len(dict["item2"])> 0)
    print(dict["item2"])
    dict["item3"] = getItems(pdf,"275,300,528,320")
    if len(dict["item3"])== 0:
        dict["item3"] = getItems(pdf,"275,303,528,322")
    print(dict["item3"])
    dict["item4"] = getItems(pdf,"275,265,528,282")
    assert(len(dict["item4"])> 0)
    print(dict["item4"])

    dict["means"] = [sum((np.arange(0,11)*dict["item"+str(i+1)][1:])/sum(dict["item"+str(i+1)][1:])) for i in range(4)]
    dict["devs"] = [ np.std(np.concatenate([np.repeat(i,j) for i,j in zip(range(0,11),dict["item"+str(z+1)][1:])])) for z in range(4)]

    print(dict)
    collection.insert_one(dict)

client = MongoClient()

db = client["db_enquestes"]
global collection
collection = db.enquestes

p = Path('./professors')
for x in p.iterdir():
    print (x)
    if x.is_file():
        enquesta(str(x))
