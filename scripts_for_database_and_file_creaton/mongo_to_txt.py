# This script reads data from db_comments_processed
# creates number ids and a dictionary file
# creates txt files with sentences

import pymongo

conn=pymongo.MongoClient()
db = conn["db_comments_processed"]

#f = open("dict.json","w",encoding='utf-8')
f = open("dict_en.json","w",encoding='utf-8')

i=0
for elem in db.comments_processed.find({},no_cursor_timeout=True):
	i += 1
	
	# dictionary file
	pdf_id = elem['pdf_id']
	f.write('"' + pdf_id + '"')
	f.write(" : ")
	f.write(str(i))
	f.write("\n")
	
	question_nr = elem['question_nr']
	language = elem['language']
	form_type = elem['form_type']	

	# file name
	#sentences = elem['sentences']
	sentences = elem['sentences_english']
	j=0
	for s in sentences:
		j += 1 # sentence number in commenr
		filename = "translated_files" + "/" + language + "/" + language + "_" + str(i) + "_" + form_type + "_" + str(question_nr) + "_" + str(j)
		f_sent = open(filename,"w",encoding='utf-8')
		f_sent.write(s)


f.close()
