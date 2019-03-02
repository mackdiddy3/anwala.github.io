import urllib2
import justext

import sys  # weird unicode stuff
reload(sys)
sys.setdefaultencoding('utf8')
"""
 IMPORTANT: I am using justext for this, which is not perfect, and sometimes gets html tags. 
            because of this, the hash values can vary between each running of the program.
            each file set must be rebuilt for each use because the hash's may not match
"""
# loads the uri from a file into a list
initialUrlList = []
infile = open("tweets.json", "r")
for line in infile:
    initialUrlList.append(line.strip())  # strip prevents extra unicode stuff, ex: /n for newline on each line

for link in initialUrlList:
    try:
        response = urllib2.urlopen(link)
        html = response.read()
        #print html
        hash_name = str(hash(html))  # hash as string to name each html download
        name = "C:\\Users\\Mack\\PycharmProjects\\anwala.github.io\\venv\\downloads\\" + hash_name
        print name
        with open(name, "w") as outfile:
            outfile.write('%s\n' % html)
        boilerplate_full = []
        boilerplate = justext.justext(html, justext.get_stoplist("English"))
        name = name + "~boilerplate"
        with open(name, 'w'):
            print ""  # do nothing, just clear any past entries into the files # replace with pass?
        for paragraph in boilerplate:
            if not paragraph.is_boilerplate:
                # check for empty files?
                with open(name, "a") as outfile:
                    outfile.write('%s\n' % paragraph.text)
    except:
        pass