import pymongo, os, re, pandas as pd

def get_train_test(k=1,lemmatize=False,POS=False,language="es"):
    if language == "es":
        negids = []
        for file in os.listdir("data/es_neg/"):
            if file.endswith(".txt"):
                negids.append(os.path.join("data/es_neg/", file))
        posids = []
        for file in os.listdir("data/es_pos/"):
            if file.endswith(".txt"):
                posids.append(os.path.join("data/es_pos/", file))
        neuids = []
        for file in os.listdir("data/es_neu/"):
            if file.endswith(".txt"):
                neuids.append(os.path.join("data/es_neu/", file))
    if language == "cat":
        negids = []
        for file in os.listdir("data/ca_neg/"):
            if file.endswith(".txt"):
                negids.append(os.path.join("data/ca_neg/", file))
        posids = []
        for file in os.listdir("data/ca_pos/"):
            if file.endswith(".txt"):
                posids.append(os.path.join("data/ca_pos/", file))
        neuids = []
        for file in os.listdir("data/ca_neu/"):
            if file.endswith(".txt"):
                neuids.append(os.path.join("data/ca_neu/", file))
    # for cross-validation
    if k == 1:
        trainids = negids[:int(len(negids)*3/4)] + posids[:int(len(posids)*3/4)] + neuids[:int(len(neuids)*3/4)]
        testids = negids[int(len(negids)*3/4):] + posids[int(len(posids)*3/4):] + neuids[int(len(neuids)*3/4):]
    elif k == 2:
        trainids = negids[:int(len(negids)*2/4)] + negids[int(len(negids)*3/4):] + posids[:int(len(posids)*2/4)] + posids[int(len(posids)*3/4):] + neuids[:int(len(neuids)*2/4)] + neuids[int(len(neuids)*3/4):]
        testids = negids[int(len(negids)*2/4):int(len(negids)*3/4)] + posids[int(len(posids)*2/4):int(len(posids)*3/4)] + neuids[int(len(neuids)*2/4):int(len(neuids)*3/4)]
    elif k == 3:
        trainids = negids[:int(len(negids)*1/4)] + negids[int(len(negids)*2/4):] + posids[:int(len(posids)*1/4)] + posids[int(len(posids)*2/4):] + neuids[:int(len(neuids)*1/4)] + neuids[int(len(neuids)*2/4):]
        testids = negids[int(len(negids)*1/4):int(len(negids)*2/4)] + posids[int(len(posids)*1/4):int(len(posids)*2/4)] + neuids[int(len(neuids)*1/4):int(len(neuids)*2/4)]
    else:
        trainids = negids[int(len(negids)*1/4):] + posids[int(len(posids)*1/4):] + neuids[int(len(neuids)*1/4):]
        testids = negids[:int(len(negids)*1/4)] + posids[:int(len(posids)*1/4)] + neuids[:int(len(neuids)*1/4)]
    print('train on %d instances, test on %d instances' % (len(trainids), len(testids)))
    train = []
    for filename in trainids:
        if language == "es":
            pos_file="".join(('data/ESP_tagged/analyzed_',filename[7:]))
        if language == "cat":
            pos_file="".join(('data/CAT_tagged/analyzed_',filename[7:]))
        pos_file = re.sub('assignatures', 'assingatures', pos_file)
        polarity = filename[8:11]
        text = open(filename,"r").read()

        if lemmatize:
            if os.path.isfile(pos_file):
                try:
                    with open(pos_file) as f:
                        pos_content = f.readlines()
                except:
                    with open(pos_file,encoding='latin1') as f:
                        pos_content = f.readlines()
                pos_content = [x.strip() for x in pos_content]

                lemmas = []
                for line in pos_content:
                    if len(line.split())>0 :
                        lemmas.append(line.split()[1])
                lemmatized_text = " ".join(lemmas)
                train.append((lemmatized_text,polarity))
        elif POS:
            if os.path.isfile(pos_file):
                try:
                    with open(pos_file) as f:
                        pos_content = f.readlines()
                except:
                    with open(pos_file,encoding='latin1') as f:
                        pos_content = f.readlines()
                    pos_content = [x.strip() for x in pos_content]
                pos_tags = []
                #lemmas = []
                for line in pos_content:
                    if len(line.split())>0 :
                        #lemmas.append(line.split()[1])
                        pos_tags.append(line.split()[2][0])
                #text_POS = ""
                #for i in range(0,len(pos_tags)):
                    #text_POS = "".join((text_POS,lemmas[i],'_',pos_tags[i],' '))
                text_POS = " ".join(pos_tags)
                train.append((text_POS,polarity))
        else:
            train.append((text,polarity))
    test = []
    for filename in testids:
        if language == "es":
            pos_file="".join(('data/ESP_tagged/analyzed_',filename[7:]))
        if language == "cat":
            pos_file="".join(('data/CAT_tagged/analyzed_',filename[7:]))
        pos_file = re.sub('assignatures', 'assingatures', pos_file)
        polarity = filename[8:11]
        text = open(filename,"r").read()

        if lemmatize:
            if os.path.isfile(pos_file):
                try:
                    with open(pos_file) as f:
                        pos_content = f.readlines()
                except:
                    with open(pos_file,encoding='latin1') as f:
                        pos_content = f.readlines()
                pos_content = [x.strip() for x in pos_content]

                lemmas = []
                for line in pos_content:
                    if len(line.split())>0 :
                        lemmas.append(line.split()[1])
                lemmatized_text = " ".join(lemmas)
                test.append((lemmatized_text,polarity))
        elif POS:
            if os.path.isfile(pos_file):
                try:
                    with open(pos_file) as f:
                        pos_content = f.readlines()
                except:
                    with open(pos_file,encoding='latin1') as f:
                        pos_content = f.readlines()
                    pos_content = [x.strip() for x in pos_content]
                pos_tags = []
                #lemmas = []
                for line in pos_content:
                    if len(line.split())>0 :
                        #lemmas.append(line.split()[1])
                        pos_tags.append(line.split()[2][0])
                #text_POS = ""
                #for i in range(0,len(pos_tags)):
                    #text_POS = "".join((text_POS,lemmas[i],'_',pos_tags[i],' '))
                text_POS = " ".join(pos_tags)
                test.append((text_POS,polarity))
        else:
            test.append((text,polarity))
            
    return train,test

def get_train_test_comments(k=1,language="es"):
    negids = []
    neuids = []
    posids = []
    conn=pymongo.MongoClient()
    db = conn["db_comments_processed"]
    if language == "es":
        for elem in db.comments_processed.find({},no_cursor_timeout=True):
            if elem['language'] == 'es':
                if elem['sentiment_polarity'] == 'NEGATIVE':
                    negids.append(elem['_id'])
                if elem['sentiment_polarity'] == 'NEUTRAL':
                    neuids.append(elem['_id'])
                if elem['sentiment_polarity'] == 'POSITIVE':
                    posids.append(elem['_id'])
    if language == "cat":
        for elem in db.comments_processed.find({},no_cursor_timeout=True):
            if elem['language'] == 'ca':
                if elem['sentiment_polarity'] == 'NEGATIVE':
                    negids.append(elem['_id'])
                if elem['sentiment_polarity'] == 'NEUTRAL':
                    neuids.append(elem['_id'])
                if elem['sentiment_polarity'] == 'POSITIVE':
                    posids.append(elem['_id'])
    # for cross-validation
    if k == 1:
        trainids = negids[:int(len(negids)*3/4)] + posids[:int(len(posids)*3/4)] + neuids[:int(len(neuids)*3/4)]
        testids = negids[int(len(negids)*3/4):] + posids[int(len(posids)*3/4):] + neuids[int(len(neuids)*3/4):]
    elif k == 2:
        trainids = negids[:int(len(negids)*2/4)] + negids[int(len(negids)*3/4):] + posids[:int(len(posids)*2/4)] + posids[int(len(posids)*3/4):] + neuids[:int(len(neuids)*2/4)] + neuids[int(len(neuids)*3/4):]
        testids = negids[int(len(negids)*2/4):int(len(negids)*3/4)] + posids[int(len(posids)*2/4):int(len(posids)*3/4)] + neuids[int(len(neuids)*2/4):int(len(neuids)*3/4)]
    elif k == 3:
        trainids = negids[:int(len(negids)*1/4)] + negids[int(len(negids)*2/4):] + posids[:int(len(posids)*1/4)] + posids[int(len(posids)*2/4):] + neuids[:int(len(neuids)*1/4)] + neuids[int(len(neuids)*2/4):]
        testids = negids[int(len(negids)*1/4):int(len(negids)*2/4)] + posids[int(len(posids)*1/4):int(len(posids)*2/4)] + neuids[int(len(neuids)*1/4):int(len(neuids)*2/4)]
    else:
        trainids = negids[int(len(negids)*1/4):] + posids[int(len(posids)*1/4):] + neuids[int(len(neuids)*1/4):]
        testids = negids[:int(len(negids)*1/4)] + posids[:int(len(posids)*1/4)] + neuids[:int(len(neuids)*1/4)]
    print('train on %d instances, test on %d instances' % (len(trainids), len(testids)))
    
    train = []
    for filename in trainids:
        doc = db.comments_processed.find({"_id":filename},no_cursor_timeout=True)
        for elem in doc:
            text = " ".join((elem['sentences']))
            polarity = elem['sentiment_polarity']
        train.append((text,polarity))
    
    test = []
    for filename in testids:
        doc = db.comments_processed.find({"_id":filename},no_cursor_timeout=True)
        for elem in doc:
            text = " ".join((elem['sentences']))
            polarity = elem['sentiment_polarity']
        test.append((text,polarity))

    return train,test

### need to update for catalan!
def get_english_train_test(k=1,language="es"):
    if language == "es":
        df = pd.read_excel('data/ESP.xlsx', sheet_name='esp', header=None)
    if language == "cat":
        df1 = pd.read_excel('data/ca_enquestes_assignatures_ALL.xlsx', sheet_name='CAT_assignatures_all_polarity', header=None)
        df2 = pd.read_excel('data/ca_enquestes_professors_ALL.xlsx', sheet_name='cat 1000-final', header=None)
        frames = [df1, df2]
        df = pd.concat(frames)
    esp_data = df[[0,1,2]]
    esp_data = esp_data.rename(index=str, columns={0: "id", 1: "sentence", 2 : "polarity"})
    negids = []
    posids = []
    neuids = []
    for row in esp_data.values.tolist():
        file_id = re.sub('assignatures', 'assingatures', row[0])
        file_id = re.sub('assigantures', 'assingatures', file_id)
        polarity = row[2]
        if language == "es":
            name = "data/translated_files/es/"+file_id
        if language == "cat":
            name = "data/translated_files/ca/"+file_id
        if polarity == "NEGATIVE" and name not in negids and name not in posids and name not in neuids:
            negids.append(name)
        if polarity == "POSITIVE" and name not in negids and name not in posids and name not in neuids:
            neuids.append(name)
        if polarity == "NEUTRAL" and name not in negids and name not in posids and name not in neuids:
            posids.append(name)

    if k == 1:
        trainids = negids[:int(len(negids)*3/4)] + posids[:int(len(posids)*3/4)] + neuids[:int(len(neuids)*3/4)]
        testids = negids[int(len(negids)*3/4):] + posids[int(len(posids)*3/4):] + neuids[int(len(neuids)*3/4):]
    elif k == 2:
        trainids = negids[:int(len(negids)*2/4)] + negids[int(len(negids)*3/4):] + posids[:int(len(posids)*2/4)] + posids[int(len(posids)*3/4):] + neuids[:int(len(neuids)*2/4)] + neuids[int(len(neuids)*3/4):]
        testids = negids[int(len(negids)*2/4):int(len(negids)*3/4)] + posids[int(len(posids)*2/4):int(len(posids)*3/4)] + neuids[int(len(neuids)*2/4):int(len(neuids)*3/4)]
    elif k == 3:
        trainids = negids[:int(len(negids)*1/4)] + negids[int(len(negids)*2/4):] + posids[:int(len(posids)*1/4)] + posids[int(len(posids)*2/4):] + neuids[:int(len(neuids)*1/4)] + neuids[int(len(neuids)*2/4):]
        testids = negids[int(len(negids)*1/4):int(len(negids)*2/4)] + posids[int(len(posids)*1/4):int(len(posids)*2/4)] + neuids[int(len(neuids)*1/4):int(len(neuids)*2/4)]
    else:
        trainids = negids[int(len(negids)*1/4):] + posids[int(len(posids)*1/4):] + neuids[int(len(neuids)*1/4):]
        testids = negids[:int(len(negids)*1/4)] + posids[:int(len(posids)*1/4)] + neuids[:int(len(neuids)*1/4)]
    print('train on %d instances, test on %d instances' % (len(trainids), len(testids)))
    
    train = []
    test = []
    for filename in negids:
        polarity = "neg"
        if os.path.isfile(filename): 
            text = open(filename,"r").read()
            if filename in trainids and filename not in testids:
                train.append((text,polarity))
            if filename in testids and filename not in trainids:
                test.append((text,polarity))
    for filename in neuids:
        polarity = "neu"
        if os.path.isfile(filename):
            text = open(filename,"r").read()
            if filename in trainids and filename not in testids:
                train.append((text,polarity))
            if filename in testids and filename not in trainids:
                test.append((text,polarity))
    for filename in posids:
        polarity = "pos"
        if os.path.isfile(filename):
            text = open(filename,"r").read()
            if filename in trainids and filename not in testids:
                train.append((text,polarity))
            if filename in testids and filename not in trainids:
                test.append((text,polarity))
    return train,test