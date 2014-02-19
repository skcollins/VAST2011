__author__ = 'susancollins'

import math
import os
import csv
import glob
from text.blob import TextBlob as tb

#create_textBlob: String -> TextBlob
#Given: A path to a text file
#Returns: A text blob representing the text
#inside the text document
def create_textBlob(fname):
    with open(fname) as file:
        #Remove \n from file and create one string
        text = file.read()
        #text =' '.join(str(line.split()) for line in file)
    #Return the text as lowecase textBlob
    return tb(str(text.lower()))

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

#get_blobsDictionary: String -> Dictionary<String, TextBlob>
#Given: The a string that represent a directory containing *.txt
#files
#Returns a dictionary of filename -> text
def get_blobsDictionary(directory):
    dictionary={}
    #Read files in from a directory
    for fname in glob.glob(directory):
        #Create a textblob for each file
        text = create_textBlob(fname)
        filename = os.path.basename(fname)
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
                text = create_textBlob(file)
                #text=' '.join(str(line.split()) for line in file)
                dictionary[filename]= text
    return dictionary

#get_idf: String String String[] -> Write CSV
#Given: A directory path containing *.txt files, an out-file name (in csv), and a list of words
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
            scores = {word: tfidf(word,dictionary[blob],bloblist) for word in dictionary[blob].words}
            sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)

            #Write TF-IDF to CSV
            for word, score in sorted_words[:int(top)]:
                        row = [word, str(round(score,20)), blob]
                        csv_out.writerow(row)

#get_tfidfForDict: Dictionary<String, TextBlob> String Integer -> Writes CSV File
#Given: A textBlob dictionary of filename->textBlob
#       outfile name in csv
#       integer representing the number of top scoring tf-idf words
#Writes the tf-idf for the top words in each text file
def get_tfidfForDict(dictionary, outfile, top):
    # Get filenames
    fileNames = dictionary.keys()

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
            scores = {word: tfidf(word,dictionary[file],bloblist) for word in dictionary[file].words}
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

#blobDictionaryToCSV: dictionary<String, String> String[] String[] ->Writes CSV file
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





targetList = ["bioterrorism", "microbes", "microbe", "trespass","trespassering","trespasser","trespassers", "suspicious", "food"
              "farm", "patino", "paramurderers", "raid", "stolen", "laboratory"]

terrorCategoryBank = create_textBlob('/Users/susancollins/Google Drive/Draper/Python/wordLists/terrorCategory.txt').words
terrorWordBank = create_textBlob('/Users/susancollins/Google Drive/Draper/Python/wordLists/terroristWords.txt').words
bioTerrorBank = create_textBlob('/Users/susancollins/Google Drive/Draper/Python/wordLists/bioTerrorism.txt').words

#word bank from 3295 3040 4085 3212
wordBank_4files = ['nicole barns', 'barns', 'cdc', 'center for disease control', 'bioterrorism', 'bryant mcfarlane', 'food supply',
            'department of agriculture', 'farm animals', 'death of animals', 'death of farm animals', 'animal deaths', 'spore-forming'
            'microbe', 'microbes', 'roxanne farson', 'edward patino', 'patino', 'biologist', 'biological', 'biological hazard', 'biological hazards'
            'citizens for ethical treatment of lab mice', 'chemical corp', 'fertilizer', 'hoechst ag', 'chemical industry',
            'vast university', 'genetic', 'spore', 'flu season']

#word bank removed fertilizer and chemical industry
wordBank_4filesv2 = ['nicole barns', 'barns', 'cdc', 'center for disease control', 'bioterrorism', 'bryant mcfarlane', 'food supply',
            'department of agriculture', 'farm animals', 'death of animals', 'death of farm animals', 'animal deaths', 'spore-forming'
            'microbe', 'microbes', 'roxanne farson', 'edward patino', 'patino', 'biologist', 'biological', 'biological hazard', 'biological hazards'
            'citizens for ethical treatment of lab mice', 'chemical corp', 'hoechst ag',
            'vast university', 'genetic', 'spore', 'flu season', 'food']

wordBank_2385_1785 = ['contamination', 'farmers', 'livestock', 'food storage', 'soil', 'livestock deaths', 'livestock'
                        'vast university', 'uptown', 'stolen equipment', 'tony grenier', 'grenier', 'lab equipment']


wordBank_3740 = ['trespasser', 'trespassers', 'trespassing', 'suspicious individuals', 'beatrice brothers', 'carnage']

solutionFiles = ['02385.txt', '03212.txt', '03740.txt', '03040.txt',
                 '03622.txt', '04085.txt', '04080.txt', '01785.txt',
                 '03435.txt',  '01878.txt', '01030.txt', '01038.txt', '03295.txt']

patino = ['patino', 'edward patino']


header = ['files', 'words']

banks = wordBank_4filesv2 + wordBank_2385_1785 

#terrorCatDict = findWordList('/Users/susancollins/Google Drive/Draper/Python/AllFiles/*.txt', terrorCategory, 1)
#blobDictionaryToCSV(terrorCatDict, header, 'terrorCategory.csv')

allFilesDict= get_blobsDictionary('/Users/susancollins/Google Drive/Draper/Python/AllFiles/*.txt')
solutionDict = get_blobsDictionary('/Users/susancollins/Google Drive/Draper/Python/SolutionFiles/*.txt')

print len(findWordListinDict(allFilesDict, banks, 3))
print findWordListinDict(allFilesDict, patino, 1)
#print findWordListinDict(solutionDict, banks, 1)
#blobDictionaryToCSV(findWordListinDict(allFilesDict, banks, 3), header, "workBank_6Files_T3.csv")


#blobDictionaryToCSV(findWordListinDict(allFilesDict, wordBank_4filesv2, 2),header, "wordBank_4Files_t2.csv")

#print findWordListinDict(solutionDict, wordBank_4filesv2, 2)
#print len(findWordListinDict(solutionDict, wordBank_4filesv2, 2))

#allFiles= get_blobsDictionary('/Users/susancollins/Google Drive/Draper/Python/AllFiles/*.txt')
#terrorCatFiles = get_columnFromCSV('terrorCategory.csv', 0)
#terrorCatv2Dict = filterDictionary(allFiles, terrorCatFiles)
#twbT3 = findWordListinDict(terrorCatv2Dict, terrorWordBank, 3)
#twbT3filesNames = get_columnFromCSV('terrorWordBankT3.csv', 0)
#twbT3Dict = get_filterblobsDictionary('/Users/susancollins/Google Drive/Draper/Python/AllFiles/*.txt', twbT3filesNames)
#get_tfidfForDict(twbT3Dict, "twbT3_tfidf.csv", 3)

#blobDictionaryToCSV(twbT3, header, 'terrorWordBankT3.csv')


#twbT3dict = filterDictionary(allFiles, filesTWBT3)
#blobDictionaryToCSV(twbT3dict, header, 'test2.csv')
#get_tfidfForDict(twbT3dict, "twbT3_tfidf_top3.csv", 3)
#get_tfidf('/Users/susancollins/Google Drive/Draper/Python/SolutionFiles/*.txt', 'test2.csv', 3)


#terrorCatv2Files=get_fileNamesFromCSV('/Users/susancollins/Google Drive/Draper/Python/9 Dec/terrorCatv2.csv')

#allFiles= get_blobsDictionary('/Users/susancollins/Google Drive/Draper/Python/SolutionFiles/*.txt')

#blobDictionaryToCSV(allFiles, header, "test2.csv")
#terrorCatv2Dict = filterDictionary(allFiles, terrorCatv2Files)
#print allFiles['00001.txt']

#blobDictionaryToCSV(terrorCatv2Dict,header ,"test.csv")
#twb=findWordListinDict(terrorCatv2Dict, terrorWordBank, 3)
#solFiles = get_blobsDictionary('/Users/susancollins/Google Drive/Draper/Python/SolutionFiles/*.txt')
#get_tfidfForDict(solFiles, 'test2.csv', 3)
#get_tfidf('/Users/susancollins/Google Drive/Draper/Python/SolutionFiles/*.txt','terrorCatv2_tfidf.csv', 3)


