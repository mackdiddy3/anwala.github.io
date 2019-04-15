import feedparser
import cluster
import re
import time
import urllib2
import justext as jt
from collections import Counter as counter
import plotly as py
import plotly.figure_factory as ff
#import matplotlib # might work for dendograms
import numpy as np
#import scipy # required for plotly? don't delete


#import sys  # weird unicode stuff
#reload(sys)
#sys.setdefaultencoding('utf-8')




'''
#dendrogram and array testing
X=np.array( [ [1,2,3],[4,5,6],[7,8,9],[10,11,12] ] ) # must be np.array
print X
dendro = ff.create_dendrogram(X, color_threshold=1.5)
dendro['layout'].update({'width':800, 'height':500})
py.offline.plot(dendro, filename='simple_dendrogram.html')

test =np.array([1,2,3])
test2=np.array([4,5,6])
test3=np.array([7,8,9])
test4=np.array([10,11,12])
test = np.vstack([test,test2])
test3 = np.vstack([test3,test4])
test=np.vstack([test,test3])
print test
dendro = ff.create_dendrogram(test, color_threshold=1.5)
dendro['layout'].update ({'width':800, 'height':500})
py.offline.plot(dendro,filename='test_dendrogram.html')
'''

'''
#test=np.array([None,None])
test=np.empty(2)
print test
#test = np.vstack([test, [1,2]])
print test

#it is possible to stack normal arrays to numpy arrays
'''


#'''
total_word_list = []
final_word_list = []
temp_word_list = []

with open("uri_list.txt", "r") as blog_uri_list:
    for link in blog_uri_list:
        try:
            #grab title somehow
            response = urllib2.urlopen(link)
            html = response.read()
            boilerplate = jt.justext(html, jt.get_stoplist("English"))
            for paragraph in boilerplate:
                if not paragraph.is_boilerplate:
                    #paragraph.text is words
                    #print paragraph.text # prints blog content to console
                    temp_word_list = re.sub("[^\w]", " ", paragraph.text).split()
                    total_word_list += temp_word_list
                    #print temp_word_list # u shows up isn't actuall in the string, just displayed for list
            #print total_word_list # word list of each blog

        except:
            print "error in opening getting text from link--------------------------------------"
            time.sleep(1)
        #print "finished with a link"
    #all text has been pulled out
    print "complete word list:"
    print total_word_list
    counts = counter(total_word_list).most_common(20)
    print "most common words:"
    print counts
    print "-----------------------------------------------------------------------------------------------------------------------------------"
#'''

just_words = [] # this list is much easier to iterate through later
for word in counts:
    just_words.append(word[0])

#'''
with open("blog_data.txt", "w") as outfile:
    #outfile.write('%s\n' % output)
    for word in just_words:
        outfile.write(word)
        if word != just_words[-1]:
            outfile.write("|")
    outfile.write("\n")
    with open("uri_list.txt", "r") as blog_uri_list:
        for link in blog_uri_list:
            blog_word_list = []
            print "i should be empty:", blog_word_list
            #try:
            to_add_list = []
            response = urllib2.urlopen(link)
            html = response.read()
            boilerplate = jt.justext(html, jt.get_stoplist("English"))
            for paragraph in boilerplate:
                if not paragraph.is_boilerplate:
                        temp_word_list = re.sub("[^\w]", " ", paragraph.text).split()
                        for word in temp_word_list:
                            if word in just_words:
                                to_add_list.append(word)
                            else:
                                #print "didnt find:", word
                                pass
                        #print to_add_list
                        blog_word_list += to_add_list
            print "blog_word_list:"
            print blog_word_list
            time.sleep(10)
            counts = counter(blog_word_list).most_common(1000) # can access [0] and [1] this way
            print "new counts:"
            print counts
            time.sleep(2)

            for each in just_words:
                not_in = 1
                for word in counts:
                    #print "what the fuck am i accessing"
                    #print word[0]
                    if word[0] == each:
                        outfile.write(str(word[1]))
                        not_in = 0
                if not_in == 1:
                    #print 0
                    outfile.write("0")
                if each != just_words[-1]: # all but last entry
                    outfile.write("|")
                    #print "|"
                #if each == just_words[-1] :
                    #outfile.write("\n")
            outfile.write("\n")

            #iterate through just_words, if not in: 0, else print the count
            #except:
            #    print "error in opening getting text from link--------------------------------------"
            #    time.sleep(1)
            #print final_word_list

    #'''








