__author__ = 'susancollins'

import pickle
from collections import Counter
import codecs
import math
import os
import csv
import glob
from text.blob import TextBlob as tb
from gensim import *
#import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#create_textBlob: String -> TextBlob
#Given: A path to a text file
#Returns: A text blob representing the text
#inside the text document (there is no change to the casing)
def create_TextBlob(fname):
    with codecs.open(fname, encoding='ascii', errors='ignore') as file:
        #Read file in
        text= file.read()
    #Return the text as textBlob
    return tb(str(text))

def create_Doc(fname):
    with codecs.open(fname, encoding='ascii', errors='ignore') as file:
        #Read file in
        text= file.read()
     #Return the text as textBlob
    return str(text)

#tf: String TextBlob -> Float
#Get the term frequency based on a word and
def tf(word, blob):
    return blob.words.count(word) / float(len(blob.words))

#n_containing: String ListOf<TextBlob> -> Number
#Given: A word and a list of textBlobs
#Returns: the number of files that the word appears
#in
def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)

#idf: String ListOf<TextBlob> -> Number
#Given: A word a list of textBlobs
#Returns: the inverse document frequency for the word
def idf(word, bloblist):
    return math.log(len(bloblist) / (float(1 + n_containing(word, bloblist))))


#tfidf : String TextBlob ListOf<TextBlob> -> Number
# Given: a word, a document that contains the word, and a collection of documents
# Returns the tf-idf for the word
def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

#tfidf_fromWL : String[] TextBlob ListOf<TextBlob> Integer-> Number
# Given: a wordlist, a document that contains the word, and a collection of documents
# and an integer indicating the top scoring tf_idf
# Returns the a dictionary of word->tf-idf score
def tfidf_fromWL(wordlist, blob, bloblist, top):

    tfidf_dict = {}
    scores = {word: tfidf(word,blob,bloblist) for word in wordlist}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    #Write TF-IDF to dictionary
    for word, score in sorted_words[:int(top)]:
        tfidf_dict [word] = str(round(score,20))

    return tfidf_dict

#get_blobsDictionary: String -> Dictionary<String, TextBlob>
#Given: The a string that represent a directory containing *.txt
#files
#Returns a dictionary of filename -> text
def get_blobsDictionary(directory):
    dictionary={}
    #Read files in from a directory
    for fname in glob.glob(directory):
        #Create a textblob for each file
        text = create_TextBlob(fname)
        filename = os.path.basename(fname)
        dictionary[filename] = text
    return dictionary

def get_docDictionary(directory):
    dictionary={}
    #Read files in from a directory
    for fname in glob.glob(directory):
        #Create a textblob for each file
        text = create_Doc(fname)
        filename = os.path.basename(fname)
        dictionary[filename] = text
    return dictionary


def get_blobsDictionaryfromList(directory, fileNameList):
    dictionary={}
    #Read files in from a directory
    for fname in glob.glob(directory):
        filename = os.path.basename(fname)
        if filename in fileNameList:
            #Create a textblob for each file
             text = create_TextBlob(fname)
             dictionary[filename] = text
    return dictionary

#get_filterblobsDictionary: String String[] -> Dictionary<String, TextBlob>
#Given: A path to a directory containing *.txt files and list of filenames
#Return a dictionary for the specified filenames
def get_filterblobsDictionary(directory, filenames):
    dictionary={}
    #Read files in from a directory
    for fname in glob.glob(directory):
        filename = os.path.basename(fname)
        if filename in filenames:
            with open(fname) as file:
                #Create textBlobs for each file
                text = create_TextBlob(file).lower()
                dictionary[filename] = text
    return dictionary

#get_idf: String String String[] -> Write CSV
#Given: A directory path containing *.txt files
#       Out-file name (in csv)
#       List of words
#Returns: the idf for the list of words and prints them to the outfile
def get_idf(directory, outfile, words):
    # Get files from directory to create textBlobs
    dictionary = get_blobsDictionary(directory)
    bloblist = dictionary.values()

    #Create CSV file for output
    with open(outfile, 'w') as out_file:
        header = ['word', 'idf']
        csv_out = csv.writer(out_file)
        csv_out.writerow(header)

        #Get IDF for words in bloblist
        scores = {word: idf(word,bloblist) for word in words}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        #Write IDF to CSV
        for word, score in sorted_words:
                    row = [word, str(round(score,20))]
                    csv_out.writerow(row)

#get_tfidf: String String Integer -> Write CSV
#Given: A directory path containing *.txt files
#       outfile name in csv
#       integer representing the number of top scoring tf-idf words
#Writes the tf-idf for the top words in each text file
def get_tfidf(directory, outfile, top):
    # Get files from directory to create textBlobs
    dictionary = get_blobsDictionary(directory)
    keys = dictionary.keys()
    bloblist = dictionary.values()

    #Create CSV file for output
    with open(outfile, 'w') as out_file:
        header = ['word', 'tf-idf', 'document']
        csv_out = csv.writer(out_file)
        csv_out.writerow(header)

        #Get TF-IDF for words in textBlobs
        for blob in keys:
            print("Top words in document {}".format(blob))
            scores = {word: tfidf(word.encode('ascii', 'ignore'),dictionary[blob],bloblist)
                      for word in dictionary[blob].words}
            sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)

            #Write TF-IDF to CSV
            for word, score in sorted_words[:int(top)]:
                        row = [word, str(round(score,20)), blob]
                        csv_out.writerow(row)

#get_tfidfForDict: String[] Dictionary<String, TextBlob> String Integer -> Writes CSV File
#Given: A list of file names or the String 'collection'
#       A textBlob dictionary of filename->textBlob
#       outfile name in csv
#       integer representing the number of top scoring tf-idf words
# If tfidf_files = 'collection' then a list of the top scoring tf-idf words
# for every file in the collection is written to outfile.
# Else list of the top scoring tf-idf words
# for every file in tfidf_files is written to outfile.
def get_tfidfForDict(tfidf_files, dictionary, outfile, top):

    if tfidf_files == 'collection':
        # Get all filenames from collection
        # to perform tf_idf
        fileNames = dictionary.keys()
    else: fileNames = tfidf_files

    #Get text blobs associated with file names
    bloblist = dictionary.values()

    #Create CSV file for output
    with open(outfile, 'w') as out_file:
        header = ['word', 'tf-idf', 'document']
        csv_out = csv.writer(out_file)
        csv_out.writerow(header)

        #Get TF-IDF for words in textBlobs
        for file in fileNames:
            print("Top words in document {}".format(file))
            scores = {word: tfidf(word.encode('ascii', 'ignore'),dictionary[file],bloblist)
                      for word in dictionary[file].words}

            sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)

            #Write TF-IDF to CSV
            for word, score in sorted_words[:int(top)]:
                row = [word, str(round(score,20)), file]
                csv_out.writerow(row)




#findWordList: String String[] Integer ->Dictionary<String, String[]>
#Given: A directory path containing *.txt files
#       a word list
#       integer representing the number of words from wordList that must appear
#       in a file
#Returns: A dictionary of filename -> words that appeared in file
def findWordList(directory, wordList, threshold):
    #Make a blobsDictionary
    blobDictionary=get_blobsDictionary(directory)
    blobFile = blobDictionary.keys()
    resultDictionary ={}

    #Check if the the words in wordList
    #are in each blob
    for blobFile in blobDictionary:
        foundWords = []
        for word in wordList:
            if blobDictionary[blobFile].find(word) > -1:
                foundWords.append(word)
        if len(foundWords)>= int(threshold):
            resultDictionary[blobFile] = str(foundWords)

    return resultDictionary


#findWordListinDict: Dictionary<String, textBlob> String[] Integer ->Dictionary<String, String[]>
#Given: A dictionary that contains fileName -> text in file
#       a word list
#       integer representing the number of words from wordList that must appear
#       in a file
#Returns: A dictionary of filename -> words that appeared in file
def findWordListinDict(blobDictionary, wordList, threshold):
    blobFiles = blobDictionary.keys()
    resultDictionary ={}

    #Check if the the words in wordList
    #are in each blob
    for blobFile in blobFiles:
        foundWords = []
        for word in wordList:
            word = word.lower()
            if blobDictionary[blobFile].find(word) > -1:
                foundWords.append(word)
        if len(foundWords)>= int(threshold):
            resultDictionary[blobFile] = str(foundWords)
    return resultDictionary

#blobDictionaryToCSV: dictionary<String, String> String[] String ->Writes CSV file
#Given: A dictionary
#       a String[] of header names
#       an outfile name in csv
#Returns: Writes a CSV file that contains the key as the first column
# and the values as the second column. The first row will be written
# using the headers.
def blobDictionaryToCSV(dictionary, headers, outfile):
    #Get the filenames in the dictionary
    files = dictionary.keys()

    #Create CSV file for output
    with open(outfile, 'w') as out_file:
        csv_out = csv.writer(out_file)
        csv_out.writerow(headers)

        #write filename with value
        for file in files:
            row = [file, dictionary[file]]
            csv_out.writerow(row)

#filterDictionary: Dictionary<String, ANYVALUE> String[] -> Dictionary<String, ANYVALUE>
#Given: A dictinoary of string->value
#       an String[]
#Returns: A dictionary like given, but filtered to only have entries that have a filteringKey
def filterDictionary(dictionary, filteringKeys):
    resultDictionary ={}
    keys = dictionary.keys()

    for key in keys:
        if key in filteringKeys:
            resultDictionary[key] = dictionary[key]

    return resultDictionary

#get_columnFromCSV: String Integer ->String[]
#Given: A filename for a csv file
#       the column that you want to select
# Reads a csv file and returns the column specified.
# This is zero indexed so the first column is 0
# This also skips the first row assuming that it is a header
def get_columnFromCSV(filename, column):
    strings = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None) #skip the header
        for row in reader:
            strings.append(row[column])
    return strings

#get_matchingWord: String String[] Integer Integer ->String[]
#Given: A filename for a csv file
#       the column that you want to select
def get_matchingWord(filename, wordList, colOfWord, numCols):
    allStrings = []
    with open(filename, 'rU') as csvfile:
        reader = csv.reader(csvfile, dialect=csv.excel_tab)
        next(reader, None) #skip the header
        for row in reader:
            #Split each row by the comma
            cols = row[0].split(",")

            #if the word is a word in the wordlist
            if cols[colOfWord] in wordList:
                strings=[]
                for colNum in range(0,numCols):
                    strings.append(cols[colNum])
                    colNum+=1
                allStrings.append(strings)
    return allStrings

#wordBank_generator: ListOf<TextBlob> -> String[]
#Given: A list of TextBlob
#Returns: A set of Strings that contains proper nouns
# in lowercase
def wordBank_generator(blobList):
    wordBank = []
    for blob in blobList:
        proper_nouns = get_ProperNouns(blob)
        for word in blob.noun_phrases:
            word = word.lower().encode('ascii','ignore')
            if word not in wordBank:
                wordBank.append(word)
        for noun in proper_nouns:
            noun = noun.lower().encode('ascii','ignore')
            if noun not in wordBank:
                wordBank.append(noun)
    return wordBank

#get_ProperNouns: TextBlob -> String[]
#Given: A TextBlob
#Returns: A wordBank that contains proper nouns and noun phrases
def get_ProperNouns(blob):
    proper_nouns = []
    pos_tags = blob.tags
    for word_pair in pos_tags:
        if word_pair[1]==u'NNP' or word_pair[1]==u'NNPS':
            proper_nouns.append(word_pair[0].encode('ascii','ignore'))

    return proper_nouns

#get_ProperNounsWL: ListOf<TextBlob> -> SetOf<String>
def get_ProperNounsWL(bloblist):
    proper_nouns = set()
    for blob in bloblist:
        proper_nouns.update(get_ProperNouns(blob))
    return proper_nouns

#remove_stopWords: String[] String[] -> String[]
def remove_stopWords(wordlist, stopWords):
    words = []
    for word in wordlist:
        if word not in stopWords:
            words.append(word)
    return words

#lower: WordList -> String[]
def lower(WordList):
    uni_words = WordList.lower()
    stringWords = [word.encode('ascii', 'ignore') for word in uni_words]
    return stringWords

#writeModel: String List<> -> File
def writeList(fileName, list):
    with open(fileName, 'a+') as file:
        for item in list:
            file.write(item)
            file.write('\n')

#removeUnique(): String[String[]] -> String[String[]]
def removeUniques(texts, occurrence):
    all_tokens = sum(texts, [])
    counter = Counter(all_tokens)
    tokensToRemove = set(word for word in set(all_tokens) if counter[word] <= occurrence)
    texts = [[word for word in text if word not in tokensToRemove]
               for text in texts]
    return texts

#fileToPickle: String (name.p) Object -> Write file
def objectToPickle(filename, object):
    outFile = open(filename, 'wb')
    pickle.dump(object, outFile)
    outFile.close()

#pickleToFile: String -> Object
def pickleToObject(filename):
    inFile = open(filename, 'rb')
    object = pickle.load(inFile)
    inFile.close()
    return object