__author__ = 'susancollins'

import math
import os
import csv
import glob
from text.blob import TextBlob as tb

# create_textBlob: String -> TextBlob
#Given: A path to a text file
#Returns: A text blob representing the text
#inside the text document
def create_textBlob(fname):
    with open(fname) as file:
        #Create textBlob for file
        #text = file.read()
        text =' '.join(line.rstrip() for line in file)
    return tb(text.lower())

#tf: String TextBlob -> Float
#Get the term frequency based on a word and
def tf(word, blob):
    return blob.words.count(word) / float(len(blob.words))

#String ListOf<TextBlob> -> Number
def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)

#String ListOf<TextBlob> -> Number
def idf(word, bloblist):
    return math.log(len(bloblist) / (float(1 + n_containing(word, bloblist))))



def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

#String -> Dictionary<String, TextBlob>
def get_blobsDictionary(directory):
    dictionary={}
    #Read files in from a directory
    for fname in glob.glob(directory):
        #Create a textblob for each file
        text = create_textBlob(fname)
        filename = os.path.basename(fname)
        dictionary[filename] = text
    return dictionary

def get_filterblobsDictionary(directory, filenames):
    dictionary={}
    #Read files in from a directory
    for fname in glob.glob(directory):
        filename = os.path.basename(fname)
        if filename in filenames:
            with open(fname) as file:
                #Create textBlobs for each file
                text=''.join(str(line.split()) for line in file)
                dictionary[filename]= tb(str(text.lower()))
    return dictionary


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


def get_tfidf_filter(directory, outfile, top, fileNames):
    # Get files from directory to create textBlobs
    dictionary = get_filterblobsDictionary(directory,fileNames)
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

#Dictionary<String, TextBlob> String Integer -> Writes CSV File
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

def findWordsandKey(directory, wordList, threshold, keyword):
    #Make a blobsDictionary
    blobDictionary=get_blobsDictionary(directory)
    blobFile = blobDictionary.keys()
    resultDictionary={}

    #Check if the words in wordList
    #are in each blob
    for blobFile in blobDictionary:
        terroristWords = []
        for word in wordList:
            if word in blobDictionary[blobFile].words and keyword in blobDictionary[blobFile].words:
                terroristWords.append(word)
        if len(terroristWords)>= int(threshold):
            resultDictionary[blobFile] = str(terroristWords)

    return resultDictionary

def findWords(directory, wordList, threshold):
    #Make a blobsDictionary
    blobDictionary=get_blobsDictionary(directory)
    blobFile = blobDictionary.keys()
    resultDictionary ={}

    #Check if the the words in wordList
    #are in each blob
    for blobFile in blobDictionary:
        terroristWords = []
        for word in wordList:
            if word in blobDictionary[blobFile].words:
                terroristWords.append(word)
        if len(terroristWords)>= int(threshold):
            resultDictionary[blobFile] = str(terroristWords)

    return resultDictionary


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

def findWordListinDict(blobDictionary, wordList, threshold):
    blobFiles = blobDictionary.keys()
    resultDictionary ={}

    #Check if the the words in wordList
    #are in each blob
    for blobFile in blobFiles:
        foundWords = []
        for word in wordList:
            word= word.lower()
            if blobDictionary[blobFile].find(word) > -1:
                foundWords.append(word)
        if len(foundWords)>= int(threshold):
            resultDictionary[blobFile] = str(foundWords)
    return resultDictionary

#BlobDictionary<String, String> String[] String[] ->Writes CSV file
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

#Filters for particular keys in dictionary
def filterDictionary(dictionary, filteringKeys):
    resultDictionary ={}
    keys = dictionary.keys()

    for key in keys:
        if key in filteringKeys:
            resultDictionary[key] = dictionary[key]

    return resultDictionary

#Reads a csv file and returns the first column
#(the filenames) in a String[]
def get_fileNamesFromCSV(filename):
    fileNamesArray = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None) #skip the header
        for row in reader:
            fileNamesArray.append(row[0])
    return fileNamesArray





targetList = ["bioterrorism", "microbes", "microbe", "trespass","trespassering","trespasser","trespassers", "suspicious", "food"
              "farm", "patino", "paramurderers", "raid", "stolen", "laboratory"]

terrorCategory = [ "terrorism" ,  "terror" ,  "terrorist" ,  "bioterror" ,  "bioterrorism" ,  "anti-terrorism" ,
"terrorists" ,  "cyberterrroism" ,  "ecoterroism" ,  "narcoterrorism", "threat", "threats", "threatening"]


terrorWordBank = ["Aggression", "Aggressor", "Ambush", "Anarchy", "Anguish", "Annihilate", "Assassin", "Assassinate",
                  "Assault", "Atrocity", "Attack", "Bioterrorism", "Blindside", "Bomb", "Bombardment", "Booby trap",
                  "Breach", "Brutal", "Brutality", "Captive", "Capture", "Carnage", "Casualties", "Chaos", "Coalition",
                  "Conspiracy", "Conspire", "Dead", "Deadly", "Death", "Defiant", "Destroy", "Destruction", "Detonate",
                  "Devastation", "Die", "Disaster", "Disastrous", "Disease", "Escape", "Evacuate", "Execute", "Execution",
                  "Explode", "Explosion", "Explosive", "Extremism", "Fatal", "Fight", "Fighter", "Flee", "Fugitive",
"Genocide", "Germ warfare", "Grenade", "Grievous", "Guided bombs", "Guns", "Gunship", "Hijack", "Hijacker", "Holocaust",
"Horrific", "Hostile", "Hostility", "Infantry", "Infiltrate", "Informant", "Injuries", "Insurgent", "Interrogation",
"Invasion", "Investigate", "Investigations", "Kidnap", "Kill","Lamentation", "Land mines", "Laser-activated",
"Machine guns", "Maim", "Malevolent", "Malicious", "Maraud", "Massacre", "Mayhem", "Megalomania", "Menace", "Militancy",
"Militant", "Militaristic", "Military", "Militia", "Mines", "Missile", "Mission", "Mistreatment", "Mortars", "Munitions",
"Murder", "Notorious", "Outbreak", "Overrun", "Overthrow", "Penetration", "Persecute", "Petrify", "Post-traumatic",
"Premeditate", "Proliferation", "Provocation", "Pugnacious", "Radiation", "Radical", "Rage", "Ravage", "Ravish", "Rebel",
"Rebellion", "Reconnaissance", "Retaliation", "Retribution", "Revenge", "Rocket", "Sabotage", "Savage", "Secrecy", "Secret",
"Security", "Seize", "Siege", "Slaughter", "Smuggle", "Special-ops", "Spy", "Spy satellite", "Strangle", "Strategic",
"Strategist", "Strategy", "Submarine", "Suffering", "Surrender", "Suspect", "Tactics", "Tank", "Target", "Terror",
"Terrorism", "Terrorist", "Terrorize", "Threat", "Threaten", "Tragic", "Treachery", "Vendetta", "Vicious", "Vile", "Vilify",
"Violence", "Virulence", "Vitriol", "Vociferous", "War", "Warheads", "Warplane", "Weapon", "Weapons", "Wreckage"]

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
            'vast university', 'genetic', 'spore', 'flu season']




solutionFiles = ['02385.txt', '03212.txt', '03740.txt', '03040.txt',
                 '03622.txt', '04085.txt' '04080.txt' '01785.txt',
                 '03435.txt',  '01878.txt' '01030.txt' '01038.txt' '03295.txt']


header = ['files', 'words']


#terrorCatDict = findWordList('/Users/susancollins/Google Drive/Draper/Python/AllFiles/*.txt', terrorCategory, 1)
#blobDictionaryToCSV(terrorCatDict, header, 'terrorCategory.csv')

allFiles= get_blobsDictionary('/Users/susancollins/Google Drive/Draper/Python/AllFiles/*.txt')
#terrorCatFiles = get_fileNamesFromCSV('terrorCategory.csv')
#terrorCatv2Dict = filterDictionary(allFiles, terrorCatFiles)
#twbT3 = findWordListinDict(terrorCatv2Dict, terrorWordBank, 3)
#blobDictionaryToCSV(twbT3, header, 'terrorWordBankT3.csv')
filesTWBT3 = get_fileNamesFromCSV('terrorWordBankT3.csv')
twbT3dict = filterDictionary(allFiles, filesTWBT3)
blobDictionaryToCSV(twbT3dict, header, 'test2.csv')
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


