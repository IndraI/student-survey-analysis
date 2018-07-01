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

def sortchildrenby(parent, attr):
    parent[:] = sorted(parent, key=lambda child: float(child.get(attr)),reverse=True)

def enquesta(path):
    pdf = pdfquery.PDFQuery(path,normalize_spaces=False,resort=False)
    pdf.load(0)

    pdf_id = path[16:]

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

    dict["pdf_id"] = pdf_id


    print(dict)
    dict["points1"] = getItems(pdf,"275,357,528,373")
    print(dict["points1"])
    assert(len(dict["points1"]) > 0)
    dict["points2"] = getItems(pdf,"275,325,528,342")
    assert(len(dict["points2"])> 0)
    print(dict["points2"])
    dict["points3"] = getItems(pdf,"275,300,528,320")
    if len(dict["points3"])== 0:
        dict["points3"] = getItems(pdf,"275,303,528,322")
    print(dict["points3"])
    dict["points4"] = getItems(pdf,"275,265,528,282")
    assert(len(dict["points4"])> 0)
    print(dict["points4"])

    dict["means"] = [sum((np.arange(0,11)*dict["points"+str(i+1)][1:])/sum(dict["points"+str(i+1)][1:])) for i in range(4)]
    dict["devs"] = [ np.std(np.concatenate([np.repeat(i,j) for i,j in zip(range(0,11),dict["points"+str(z+1)][1:])])) for z in range(4)]

    # load the rest of the pages
    num_pages = pdf.doc.catalog['Pages'].resolve()['Count']
    if num_pages>2:
        ran = [i for i in range(1,num_pages)]
    else:
        ran=1
    pdf.load(ran)
    xml = pdf.tree
    root = xml.getroot()

    if num_pages > 2:
        for child in root:
            for subchild in child:
                sortchildrenby(subchild, 'y0')
    else:
        for child in root:
            sortchildrenby(child, 'y0')

    question = 0
    q1_answers=[]
    q2_answers=[]
    for i in range(0,num_pages-1):
        for child in root[i]:
            if child.attrib['bbox'].startswith("[24.96"):
                print(child[0].text)
                question += 1
                if question == 1:
                    dict["q1_text"] = child[0].text.rstrip()
                if question == 2:
                    dict["q2_text"] = child[0].text.rstrip()
            if child.attrib['bbox'].startswith("[24.7") and question == 1 and child[0].text != " \n":
                text = ""
                for j in child:
                    text=text+j.text.rstrip()
                if len(text.strip())>1:
                    q1_answers.append(text.rstrip())
            if child.attrib['bbox'].startswith("[24.7") and question == 2 and child[0].text != " \n":
                text = ""
                for j in child:
                    text=text+j.text.rstrip()
                if len(text.strip())>1:
                    q2_answers.append(text.rstrip())

    dict["q1_answers"] = q1_answers
    dict["q2_answers"] = q2_answers

    print(dict)
    collection.insert_one(dict)

client = MongoClient()

db = client["db_enquestes"]
global collection
collection = db.enquestes_professors

p = Path('./professors15_16')
for x in p.iterdir():
    print (x)
    if x.is_file() and x.suffix == '.pdf':
        enquesta(str(x))

p = Path('./professors16_17')
for x in p.iterdir():
    print (x)
    if x.is_file() and x.suffix == '.pdf':
        enquesta(str(x))

p = Path('./professors17_18')
for x in p.iterdir():
    print (x)
    if x.is_file() and x.suffix == '.pdf':
        enquesta(str(x))