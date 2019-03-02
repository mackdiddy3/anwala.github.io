from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
import re
import requests
import twitter_cred

# import sys                     #
# reload(sys)                    #
# sys.setdefaultencoding('utf8') # some weird error with old formatting, fixed until i break it again

keepcount = int(1)  # how many tweets have been scrubbed through

# loads the url file into a list
initialUrlList = []  # this will hold all the links already in the list of links
infile = open("tweets.json", "r")
for line in infile:
    initialUrlList.append(line.strip())  # strip prevents extra unicode stuff, ex: /n for newline on each line


class TweetGrabber():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_twitter_api(self):
        return self.twitter_client

    def unshorten(self, link):  # no link.status with current method, set up working system later
        if link.status >= 300 or link.status <= 399:  # shortened link, recurse
            link = requests.get(link)
            TweetGrabber.unshorten(self, link)
        elif link.status >= 200 or link.status <= 299:  # good link
            return link
        elif link.status >= 400 or link.status <= 599:  # bad link
            return "bad link"  # bad format for error return, fix later

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweet_text = tweet.text
            link = re.findall("(?P<url>https?://[^\s'\"]+)", tweet_text)  # grabs links from tweet
            link = ','.join(link)  # i don't know how this was my best solution but here we are. turns single element list into a string

            global keepcount
            print keepcount
            keepcount += 1

            if link != [] and link != "" and link != '' and '\\u' not in link:  # disallows blanks added to link list
                try:
                    tempint = 0
                    fulllink = requests.get(link)  # note: this breaks when the url is already unshortened
                    while "t.co/" in fulllink.url and tempint < 15:
                        fulllink = requests.get(fulllink.url)
                        tempint += 1
                    print ("unshortened link: ", fulllink.url)

                    if "t.co" not in fulllink.url \
                            and "twitter.com/" not in fulllink.url \
                            and fulllink.url not in tweets \
                            and fulllink.url not in initialUrlList:
                        tweets.append(fulllink.url)
                    else:
                        print "bad link"
                except:
                    print "error in link tweet parsing--------------------------------"  # hyper-advanced error detection

        print "------------------------------------------------------------------------------------------"
        print tweets
        return tweets


class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_cred.CONSUMER_KEY, twitter_cred.CONSUMER_SECRET)
        auth.set_access_token(twitter_cred.ACCESS_TOKEN, twitter_cred.ACCESS_TOKEN_SECRET)
        return auth


if __name__ == '__main__':
    twitter_client = TweetGrabber()
    api = twitter_client.get_twitter_api()

twitter_client = TweetGrabber('MSNBC')  # this grabs from the 'tweets & replies' timeline
#twitter_client = TweetGrabber('NFL')  # this grabs from the 'tweets & replies' timeline
#twitter_client = TweetGrabber('FoxNews')  # this grabs from the 'tweets & replies' timeline

all_the_links = twitter_client.get_user_timeline_tweets(1000)

with open("tweets.json", "a") as outfile:
    for link in all_the_links:
        outfile.write('%s\n' % link)
