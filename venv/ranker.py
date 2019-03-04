import os
import glob
from collections import Counter
import math

path = 'downloads'
keeptrack = 1
termIn = 0
secondpass = 0


# finds the idf for the query term
while termIn < 10:
    termIn = 0
    keyword = "democrat"
    # keyword = raw_input('please enter query term: ')
    if secondpass == 1:  # prevents an infinite loop on bad hardcoded keywords
        keyword = raw_input('please enter query term: ')

    totalDocs = 0

    for filename in glob.glob(os.path.join(path, '*~boilerplate')):
        with open(filename, 'r') as file:
            textbody = file.read().lower()  # extra step because obviously word and Word are different words
            wordcount = Counter(textbody.split())
            if len(textbody.split()) > 0:
                totalDocs += 1
                if wordcount[keyword] > 0:
                    termIn += 1
    # print "total documents: ", totalDocs
    # print "documents containing term: ", termIn
    if float(termIn) > 0:
        idf = round(totalDocs / float(termIn), 4)
    else:
        pass
    #print "test: ", float(totalDocs) / 3
    if termIn == 0:
        print "no documents with that term"
    elif termIn < 10:
        print "only", termIn, " documents with that term"
    elif termIn > float(totalDocs) / 3:  # warns you of oversaturated terms
        temp = raw_input('A large amount of documents contain this term, would you like to query a different term? ')
        if temp == "y" or temp == "yes":
            termIn = 0
    secondpass = 1

idf = round(math.log(idf, 2), 4)

print keyword, "appears in ", termIn, " out of ", totalDocs," documents"

print"TFIDF    TF       IDF      NAME"
print"------   ------   ------   ----------------"

# finds the tf and tfidf for each document containing the query term
for filename in glob.glob(os.path.join(path, '*~boilerplate')):
    with open(filename, 'r') as file:
        try:
            shortfilename = filename[10:-12] # filename without path
            htmlpath = filename[:-12] # path to full html file

            textbody = file.read().lower()  # extra step because obviously word and Word are different words
            wordcount = Counter(textbody.split())
            #print filename
            term = round(float(wordcount[keyword]), 4)
            total = len(textbody.split())
            tf = round(term / total, 4)
            #tf = round(tf, 4)
            tfidf = round(tf * idf, 4)
            if tfidf > 0:
                # absolutely disgusting method to format columns but it works for something this simple
                if tfidf % .001 == 0:
                    tfidf = str(tfidf)+"0"
                if tf % .001 == 0:
                    tf = str(tf)+"0"

                print tfidf, " ", tf, " ", idf, " ", shortfilename
                tfidf = float(tfidf)
                tf = float(tf)
                """
                # neater method but not working yet
                print ("{0:f}".format(tfidf),
                tf,
                idf,
                shortfilename)
                """
        except:
            pass    # weird errors
