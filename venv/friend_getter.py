from tweepy import OAuthHandler
import tweepy
import time
import twitter_cred


auth = OAuthHandler(twitter_cred.CONSUMER_KEY, twitter_cred.CONSUMER_SECRET)
auth.set_access_token(twitter_cred.ACCESS_TOKEN, twitter_cred.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

#get rid of main?

primary_friend_count = 0
friend_list = []
filename = "followerlist.csv"
screenName = "acnwala"
with open(filename, 'w'):
    pass  # clear past entries into file
for friend in tweepy.Cursor(api.followers, screen_name=screenName, count = 200).items():
    try:
        primary_friend_count += 1
        output = friend.screen_name + "," + str(friend.followers_count)
        print output
        with open(filename, "a") as outfile:
            outfile.write('%s\n' % output)
    except tweepy.TweepError:
        print "rate limit reached----------------------"
        time.sleep(901)  # limit is 5000 requests per 15 minutes
    except:
        print "unknown error"
output = screenName + "," + str(primary_friend_count)
print output
with open(filename, "a") as outfile:
    outfile.write('%s\n' % output)

