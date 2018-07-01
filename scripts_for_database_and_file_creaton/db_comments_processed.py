# This script reads information from mongo db.enquetes colection enquestes_professors and enquestes_assignatures
# detects language
# replaces professor names with placeholder "PROFESSOR_NAME"
# splits comments by sentences
# saves this to mongo database db_comments_processed

from time import sleep

import pandas as pd
import pymongo

from polyglot.text import Text
from langdetect import detect
from googletrans import Translator
translator = Translator()

import re

conn=pymongo.MongoClient()
db=conn["db_enquestes"]

db2 = conn["db_comments_processed"]
global collection
collection = db2.comments_processed

teacher_names = db.enquestes_professors.distinct("professor")
teacher_names = [item.lower().split() for item in teacher_names]
teacher_names = [item for sublist in teacher_names for item in sublist]
teacher_names.append("anna")
teacher_names.append("vitriá")
while 'de' in teacher_names: teacher_names.remove('de')
while 'mas' in teacher_names: teacher_names.remove('mas')
n = []
for name in teacher_names:
    nn = 'l\''+name
    nc = name+','
    n.append(nn)
    n.append(nc)
teacher_names = teacher_names + n
#teacher_names

for elem in db.enquestes_professors.find({},no_cursor_timeout=True):
    pdf_id = elem['pdf_id']
    q1_answers = elem['q1_answers']
    for comment in q1_answers:
        dict = {}
        dict["form_type"] = "enquestes_professors"
        dict["pdf_id"] = pdf_id
        dict["question_nr"] = 1
        language = translator.detect(str(comment).replace('\0', '')).lang
        if comment == 'Cap.' or comment == 'Cap' or comment == 'cap' or comment == 'CAP':
            language = 'ca'
        if language == "haw" or language == "ptca":
            break
        if language == 'espt' or language == 'esca' or language == "gl":
            language = 'es'
        if language == 'nl' or language == 'fr':
            language = 'ca'
        dict["language"] = language
        
        ### REPLACE PROFESSOR NAMES WITH "PROFESSOR_NAME"
        c = comment.split()
        c_lower = [x.lower() for x in c]
        for name in teacher_names:
            if name in c_lower:
                ind = c_lower.index(name)
                c[ind] = "PROFESSOR_NAME"
        comment = " ".join(c)

        sents = Text(comment).sentences
        sentences = [str(item) for item in sents]
        dict["sentences"] = sentences
        
        collection.insert_one(dict)
        sleep(.4) 
    
    q2_answers = elem['q2_answers']
    for comment in q2_answers:
        dict = {}
        dict["form_type"] = "enquestes_professors"
        dict["pdf_id"] = pdf_id
        dict["question_nr"] = 2
        language = translator.detect(str(comment).replace('\0', '')).lang
        if comment == 'Cap.' or comment == 'Cap' or comment == 'cap' or comment == 'CAP':
            language = 'ca'
        if language == "haw" or language == "ptca":
            break
        if language == 'espt' or language == 'esca' or language == "gl":
            language = 'es'
        if language == 'nl' or language == 'fr':
            language = 'ca'
        dict["language"] = language
        
        ### REPLACE PROFESSOR NAMES WITH "PROFESSOR_NAME"
        c = comment.split()
        c_lower = [x.lower() for x in c]
        for name in teacher_names:
            if name in c_lower:
                ind = c_lower.index(name)
                c[ind] = "PROFESSOR_NAME"
        comment = " ".join(c)

        sents = Text(comment).sentences
        sentences = [str(item) for item in sents]
        dict["sentences"] = sentences
        
        collection.insert_one(dict)
        sleep(.4) 

# ASSINGATURES 
for elem in db.enquestes_assingatures.find({},no_cursor_timeout=True):
    pdf_id = elem['pdf_id']
    q3_answers = elem['q1_answers']
    for comment in q3_answers:
        dict = {}
        dict["form_type"] = "enquestes_assingatures"
        dict["pdf_id"] = pdf_id
        dict["question_nr"] = 3
        language = translator.detect(str(comment)).lang
        if comment == 'Cap.' or comment == 'Cap' or comment == 'cap' or comment == 'CAP':
            language = 'ca'
        if language == "haw" or language == "ptca":
            break
        if language == 'espt' or language == 'esca' or language == "gl":
            language = 'es'
        if language == 'nl' or language == 'fr':
            language = 'ca'
        dict["language"] = language
        
        ### REPLACE PROFESSOR NAMES WITH "PROFESSOR_NAME"
        c = comment.split()
        c_lower = [x.lower() for x in c]
        for name in teacher_names:
            if name in c_lower:
                ind = c_lower.index(name)
                c[ind] = "PROFESSOR_NAME"
        comment = " ".join(c)

        sents = Text(comment).sentences
        sentences = [str(item) for item in sents]
        dict["sentences"] = sentences
        
        collection.insert_one(dict)
        sleep(.4) 
    
