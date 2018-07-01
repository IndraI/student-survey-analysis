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

    print(path)

    import re
    regex_master=re.compile('^assignatures[0-9][0-9]_[0-9][0-9]\/[0-9]*_[0-9]Sem_MD')
    if re.match(regex_master, path):
        degree_type = "master"
    regex_grau=re.compile('^assignatures[0-9][0-9]_[0-9][0-9]\/[0-9]*_[0-9]Sem_G')
    if re.match(regex_grau, path):
        degree_type = "grau"  

    print(degree_type)

    pdf_id = path[18:]

    if degree_type=="grau":
        dict = pdf.extract([#('with_parent','LTPage[pageid=1]'),
                     ('with_formatter', 'text'),
                     ('year',  'LTTextLineHorizontal:in_bbox("195,802,279,825")'),
                     ('semester',  'LTTextLineHorizontal:in_bbox("195,774,279,801")',lambda match: int(match.text()[0])),
                     #('assignatura', 'LTTextLineHorizontal:in_bbox("35,670,200,700")'),
                     ('assignatura', 'LTTextLineHorizontal:in_bbox("43,681,202,692")'),
                     ('grup', 'LTTextLineHorizontal:in_bbox("215,627,246,700")'),
                     ('grau', 'LTTextLineHorizontal:in_bbox("35,620,193,641")'),
                     ('matriculats', 'LTTextLineHorizontal:in_bbox("200,533,246,552")',lambda match: int(match.text())),
                     ('numenquestes', 'LTTextLineHorizontal:in_bbox("200,505,246,525")',lambda match: int(match.text())),
        ],as_dict=True)

        dict["pdf_id"] = pdf_id

        print(dict)
        dict["points1"] = getItems(pdf,"275,380,528,402")
        print(dict["points1"])
        assert(len(dict["points1"]) > 0)
        dict["points2"] = getItems(pdf,"275,357,528,373")
        print(dict["points2"])
        assert(len(dict["points2"]) > 0)
        dict["points3"] = getItems(pdf,"275,325,528,342")
        assert(len(dict["points3"])> 0)
        print(dict["points3"])
        dict["points4"] = getItems(pdf,"275,300,528,320")
        assert(len(dict["points4"])> 0)
        print(dict["points4"])
        dict["points5"] = getItems(pdf,"275,269,528,289")
        assert(len(dict["points5"])> 0)
        print(dict["points5"])

        dict["means"] = [sum((np.arange(0,11)*dict["points"+str(i+1)][1:])/sum(dict["points"+str(i+1)][1:])) for i in range(5)]
        dict["devs"] = [ np.std(np.concatenate([np.repeat(i,j) for i,j in zip(range(0,11),dict["points"+str(z+1)][1:])])) for z in range(5)]

        # load the rest of the pages
        num_pages = pdf.doc.catalog['Pages'].resolve()['Count']
        if num_pages>2:
            ran = [i for i in range(1,num_pages)]
        else:
            ran=1
        pdf.load(ran)
        xml = pdf.tree
        root = xml.getroot()

        q1_answers=[]
        for i in range(0,num_pages-1):
            for child in root[i]:
                if child.attrib['bbox'].startswith("[177.84"):
                    dict["q1_text"] = child[0].text.rstrip()
                if (child.attrib['bbox'].startswith("[43.4") or child.attrib['bbox'].startswith("[24.72"))  and child[0].text != " \n":
                    text = ""
                    for j in child:
                        text = text+j.text.rstrip()
                    if len(text.strip())>1:
                        q1_answers.append(text.rstrip())

        dict["q1_answers"] = q1_answers


    if degree_type=="master":
        dict = pdf.extract([#('with_parent','LTPage[pageid=1]'),
                 ('with_formatter', 'text'),
                 ('year',  'LTTextLineHorizontal:in_bbox("195,802,279,825")'),
                 ('semester',  'LTTextLineHorizontal:in_bbox("195,774,279,801")',lambda match: int(match.text()[0])),
                 ('assignatura', 'LTTextLineHorizontal:in_bbox("35,680,200,720")'),
                 ('grup', 'LTTextLineHorizontal:in_bbox("215,680,246,720")'),
                 ('grau', 'LTTextLineHorizontal:in_bbox("35,630,200,660")'),
                 ('matriculats', 'LTTextLineHorizontal:in_bbox("200,550,246,575")',lambda match: int(match.text())),
                 ('numenquestes', 'LTTextLineHorizontal:in_bbox("200,522,246,548")',lambda match: int(match.text())),
        ],as_dict=True)

        print(dict)
        dict["points1"] = getItems(pdf,"275,395,528,415")
        print(dict["points1"])
        assert(len(dict["points1"]) > 0)
        dict["points2"] = getItems(pdf,"275,370,528,392")
        print(dict["points2"])
        assert(len(dict["points2"]) > 0)
        dict["points3"] = getItems(pdf,"275,340,528,360")
        assert(len(dict["points3"])> 0)
        print(dict["points3"])
        dict["points4"] = getItems(pdf,"275,310,528,330")
        assert(len(dict["points4"])> 0)
        print(dict["points4"])
        dict["points5"] = getItems(pdf,"275,280,528,300")
        assert(len(dict["points5"])> 0)
        print(dict["points5"])
        dict["points6"] = getItems(pdf,"275,250,528,270")
        assert(len(dict["points6"])> 0)
        print(dict["points6"])

        dict["means"] = [sum((np.arange(0,11)*dict["points"+str(i+1)][1:])/sum(dict["points"+str(i+1)][1:])) for i in range(6)]
        dict["devs"] = [ np.std(np.concatenate([np.repeat(i,j) for i,j in zip(range(0,11),dict["points"+str(z+1)][1:])])) for z in range(6)]

        # load the rest of the pages
        # load the rest of the pages
        num_pages = pdf.doc.catalog['Pages'].resolve()['Count']
        if num_pages>2:
            ran = [i for i in range(1,num_pages)]
        else:
            ran=1
        pdf.load(ran)
        xml = pdf.tree
        root = xml.getroot()

        question = 0
        q2_answers=[]
        for i in range(0,num_pages-1):
                for child in root[i]:
                    if child.attrib['bbox'].startswith("[27.48"):
                        question += 1
                        if question == 2:
                            dict["q2_text"] = child[0].text.rstrip()
                    if child.attrib['bbox'].startswith("[27.36") and question == 2 and child[0].text != " \n":
                        text = ""
                        for j in child:
                            text=text+j.text.rstrip()
                        if len(text.strip())>1:
                            q2_answers.append(text.rstrip())

        dict["q2_answers"] = q2_answers

    dict["degree_type"] = degree_type

    print(dict)
    collection.insert_one(dict)

client = MongoClient()

db = client["db_enquestes"]
global collection
collection = db.enquestes_assingatures

p = Path('./assignatures15_16')
for x in p.iterdir():
    print(x)
    if x.is_file() and x.suffix == '.pdf':
        enquesta(str(x))

p = Path('./assignatures16_17')
for x in p.iterdir():
    print(x)
    if x.is_file() and x.suffix == '.pdf':
        enquesta(str(x))

p = Path('./assignatures17_18')
for x in p.iterdir():
    print(x)
    if x.is_file() and x.suffix == '.pdf':
        enquesta(str(x))
        

        