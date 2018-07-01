import os, re, nltk, numpy as np
from nltk import bigrams, trigrams, ngrams
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer
import get_train_test
from gensim.models.word2vec import Word2Vec

ca_word2vec = Word2Vec.load('TMF/scrapingReports/ca_word2vec_model')

def get_word_list(text,remove_stopwords=False,repeat=False):
    if remove_stopwords == True:
        #with open("es_stopwords.txt") as f:
        #    es_stopwords = f.readlines()
        #es_stopwords = [x.strip() for x in es_stopwords] 
        with open("ca_stopwords.txt") as f:
            ca_stopwords = f.readlines()
        ca_stopwords = [x.strip() for x in ca_stopwords] 
        es_stopwords = set(stopwords.words("spanish"))
        for stopword in es_stopwords:
            text = re.sub(stopword, '', text)
        for stopword in ca_stopwords:
            text = re.sub(stopword, '', text)
    text = re.sub(r'\d+', '', text)
    text = text.lower()
    punctuation = ['.',',','%','&','\'','/','+','!']
    rx = '[' + re.escape(''.join(punctuation)) + ']'
    text = re.sub(rx, '', text)
    if repeat:
        tokens = nltk.wordpunct_tokenize(text)
    else:
        tokens = sorted(set(nltk.wordpunct_tokenize(text)))
    remove_from_vocabulary = ['-',')','(','(?)','1','=','[',']','][',':','<','>',';',':)','?']
    for i in remove_from_vocabulary:
        if i in tokens:
            tokens.remove(i)
    return tokens

def BOW(sentence, vocabulary,remove_stopwords=False,repeat=False):
    sentence_words = get_word_list(sentence,remove_stopwords,repeat)
    bag = np.zeros(len(vocabulary))
    for w in sentence_words:
        for i,word in enumerate(vocabulary):
            if word == w: 
                bag[i] += 1
    return np.array(bag)

# LP - lemmatized or POS tagges
def get_LP_BOW_train_test_features(language="es",POS=False,tf_idf=False,remove_stopwords=False,repeat=False,k=1):
    if POS==True:
        train,test = get_train_test.get_train_test(k,POS=True,language=language)
    else:
        train,test = get_train_test.get_train_test(k,lemmatize=True,language=language)
    train_corpus = " ".join([i[0] for i in train])
    vocabulary = get_word_list(train_corpus)
    X_train = []
    y_train = []
    for sentence in train:
        bow = BOW(sentence[0],vocabulary,remove_stopwords,repeat)
        X_train.append(bow)
        y_train.append(sentence[1])
    X_test = []
    y_test = []
    for sentence in test:
        bow = BOW(sentence[0],vocabulary,remove_stopwords,repeat)
        X_test.append(bow)
        y_test.append(sentence[1])
    if tf_idf == True:
        transformer = TfidfTransformer(smooth_idf=False)
        X_train = transformer.fit_transform(X_train).toarray()
        X_test = transformer.transform(X_test).toarray() 
    return X_train,y_train,X_test,y_test

def tokenize(text):
    tokens = get_word_list(text,remove_stopwords=False,repeat=True)
    return tokens

def get_2grams_vocab(tokens):
    bigr = list(bigrams(tokens))
    fdist = nltk.FreqDist(bigr)
    bi_grams = [x[0] for x in list(fdist.items()) if x[1] >= 1]
    return bi_grams

def get_3grams_vocab(tokens):
    trigr = list(trigrams(tokens))
    fdist = nltk.FreqDist(trigr)
    tri_grams = [x[0] for x in list(fdist.items()) if x[1] >= 1]
    return tri_grams

def ngrams_to_features(sentence, ngramlist, n=2):
    tokens = tokenize(sentence)
    if n==3:
        sentence_ngrams = list(trigrams(tokens))
    elif n == 4 or n==5:
        sentence_ngrams = list(ngrams(tokens, n))
    else:
        sentence_ngrams = list(bigrams(tokens))
    bag = np.zeros(len(ngramlist))
    for w in sentence_ngrams:
        for i,word in enumerate(ngramlist):
            if word == w: 
                bag[i] += 1
                
    return np.array(bag)

def get_LP_ngram_train_test_features(language="es",POS=False,n=2,tf_idf=False,full_comments=False,k=1):
    if POS==True:
        train,test = get_train_test.get_train_test(k,POS=True,language=language)
    else:
        train,test = get_train_test.get_train_test(k,lemmatize=True,language=language)
    train_corpus = " ".join([i[0] for i in train])
    tokens = tokenize(train_corpus)
    if n==3:
        ngramlist = get_3grams_vocab(tokens)
    elif n > 3:
        ngramlist = list(ngrams(tokens, n))
    else:
        ngramlist = get_2grams_vocab(tokens)
    X_train = []
    y_train = []
    for sentence in train:
        f = ngrams_to_features(sentence[0],ngramlist,n)
        X_train.append(f)
        y_train.append(sentence[1])
    X_test = []
    y_test = []
    for sentence in test:
        f = ngrams_to_features(sentence[0],ngramlist,n)
        X_test.append(f)
        y_test.append(sentence[1])
    if tf_idf == True:
        transformer = TfidfTransformer()
        X_train = transformer.fit_transform(X_train).toarray()
        X_test = transformer.transform(X_test).toarray() 
    
    return X_train,y_train,X_test,y_test

def get_BOW_train_test_features(language="es",tf_idf=False,remove_stopwords=False,repeat=False,full_comments=False,english=False,k=1):
    if full_comments:
        train,test = get_train_test.get_train_test_comments(k=k,language=language)
    elif english:
        train,test = get_train_test.get_english_train_test(k=k)
    else:
        train,test = get_train_test.get_train_test(k=k,language=language)
    train_corpus = " ".join([i[0] for i in train])
    vocabulary = get_word_list(train_corpus)
    X_train = []
    y_train = []
    for sentence in train:
        bow = BOW(sentence[0],vocabulary,remove_stopwords,repeat)
        X_train.append(bow)
        y_train.append(sentence[1])
    X_test = []
    y_test = []
    for sentence in test:
        bow = BOW(sentence[0],vocabulary,remove_stopwords,repeat)
        X_test.append(bow)
        y_test.append(sentence[1])
    if tf_idf == True:
        transformer = TfidfTransformer(smooth_idf=False)
        X_train = transformer.fit_transform(X_train).toarray()
        X_test = transformer.transform(X_test).toarray() 
    return X_train,y_train,X_test,y_test

def get_ngram_train_test_features(language="es",n=2,tf_idf=False,full_comments=False,english=False,k=1):
    if full_comments:
        train,test = get_train_test.get_train_test_comments(k,language=language)
    elif english:
        train,test = get_train_test.get_english_train_test(k)
    else:
        train,test = get_train_test.get_train_test(k,language=language)
    train_corpus = " ".join([i[0] for i in train])
    tokens = tokenize(train_corpus)
    if n==3:
        ngramlist = get_3grams_vocab(tokens)
    elif n > 3:
        ngramlist = list(ngrams(tokens, n))
    else:
        ngramlist = get_2grams_vocab(tokens)
    X_train = []
    y_train = []
    for sentence in train:
        f = ngrams_to_features(sentence[0],ngramlist,n)
        X_train.append(f)
        y_train.append(sentence[1])
    X_test = []
    y_test = []
    for sentence in test:
        f = ngrams_to_features(sentence[0],ngramlist,n)
        X_test.append(f)
        y_test.append(sentence[1])
    if tf_idf == True:
        transformer = TfidfTransformer()
        X_train = transformer.fit_transform(X_train).toarray()
        X_test = transformer.transform(X_test).toarray() 
    
    return X_train,y_train,X_test,y_test

def w2v_ca(sentence):
    sentence_words = tokenize(sentence)
    words = []
    for word in sentence_words:
        if word in ca_word2vec.wv.vocab:
            v = ca_word2vec.wv[word]
            words.append(v)
        else:
        	words.append(np.zeros(100))
    vect = np.mean(words,axis=0)
    return vect

def get_w2v_train_test_features(language="cat",tf_idf=False,full_comments=False,k=1):
    #if full_comments:
    #    train,test = get_train_test.get_train_test_comments(k=k,language=language)
    #else:
    #    train,test = get_train_test.get_train_test(k=k,language=language)
    train,test = get_train_test.get_train_test(k,lemmatize=True,language=language)
    X_train = []
    y_train = []
    for sentence in train:
        vect = w2v_ca(sentence[0])
        if not np.isnan(np.sum(vect)): ## check that it is not nan
            X_train.append(vect)
        else:
        	X_train.append(np.zeros(100))
        y_train.append(sentence[1])
    X_test = []
    y_test = []
    for sentence in test:
        vect = w2v_ca(sentence[0])
        if not np.isnan(np.sum(vect)): ## check that it is not nan
            X_test.append(vect)
        else:
        	X_test.append(np.zeros(100))
        y_test.append(sentence[1])
    if tf_idf == True:
        transformer = TfidfTransformer(smooth_idf=False)
        X_train = transformer.fit_transform(X_train).toarray()
        X_test = transformer.transform(X_test).toarray()
    return X_train,y_train,X_test,y_test


