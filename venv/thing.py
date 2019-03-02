import requests
import urllib2
from BeautifulSoup import BeautifulSoup #just html processing instead of everything

good_link = False #trashy setup but it works
while good_link != True:
    #user_designated_page = "https://www.cs.odu.edu/~mln/teaching/cs532-s17/test/pdfs.html" #not typing this every time
    #user_designated_page = "https://www.cs.odu.edu/~mln/pubs/all.html" #similar page
    #user_designated_page = "http://www2.hawaii.edu/~kinzie/documents/CV%20&%20pubs/list%20of%20pdfs.htm" #random list of pdfs
    user_designated_page = raw_input('please enter webpage: ')#when inputting link, DO NOT ADD SPACE AFTER LINK

    test = requests.head(user_designated_page, allow_redirects=True) #poor error checking, redo in a more robust fashion
    if test.status_code == 200:
        good_link = True
    else:
        print "bad link", test.status_code

page = urllib2.urlopen(user_designated_page)#opens page in html
soup = BeautifulSoup(page) #now usable by BeautifulSoup

for link in soup.findAll('a'):#parse http to get all links
    check = requests.head(link.get('href'), allow_redirects=True) #makes thing for requests to use, I cant get BS to do it
    if check.status_code ==200:
        if check.headers['content-type'] == 'application/pdf': #grabs links that lead to a pdf
            print link, "is", check.headers['content-length'], "bytes large."