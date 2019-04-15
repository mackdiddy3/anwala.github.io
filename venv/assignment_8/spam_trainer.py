import docclass as dc
import os

training_path_spam = "training/spam/"
training_path_not_spam = "training/not_spam/"
testing_path_spam = "testing/spam/"
testing_path_not_spam = "testing/not_spam/"

train_set = dc.naivebayes(dc.getwords)
try:
    os.remove('mack.db') # deletes old database
except:
    pass # don't freak out if there's not already a database to delete
train_set.setdb('mack.db') #creates fresh database

def train(filepath, desig): #desig is 'spam' or 'not spam'
    file_list = os.listdir(filepath)
    for each in file_list:
        test_string = ""
        for line in open(filepath+each, 'r'):
            if line != '\n':
                train_set.train(line, desig)


def test(filepath):
    file_list = os.listdir(filepath)
    for each in file_list:
        test_string = ""
        for line in open(filepath+each, 'r'):
            if line != '\n':
                test_string += line
        print train_set.classify(test_string)


print "training with spam"
train(training_path_spam, 'spam')

print "training with not spam"
train(training_path_not_spam, 'not_spam')

print "testing for spam-----"
test(testing_path_spam)

print "testing for not spam-----"
test(testing_path_not_spam)


'''
user_input = 0
while user_input != "end":
    user_input = raw_input('enter text to test for spam, or enter "end" to stop: ')
    print train_set.classify(user_input)
'''

