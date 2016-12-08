import numpy as np
import collections
import random
import wordVectorHelpers

users = {}
friend_ratings = {}
trainingRatings = set()
testRatings = set()

def parseUserFile():
  f = open('graphAttributesEdinburgh.txt', 'r')
  for line in f:
    u, r, f, w = line.split("|")
    ratings = set()
    ratingsVec = r.split(',')
    for i in range(0, len(ratingsVec), 2):
      if random.random() > 0.8:
        testRatings.add((u, ratingsVec[i], int(ratingsVec[i+1])))
      else:
        trainingRatings.add((u, ratingsVec[i], int(ratingsVec[i+1])))
      ratings.add((ratingsVec[i], int(ratingsVec[i+1])))
    friends = set(f.split(','))
    words = {}
    wordsVec = w.split(',')
    for i in range(0, len(wordsVec), 2):
      words[wordsVec[i]] = wordsVec[i+1]
    users[u] = {}
    users[u]['ratings'] = ratings
    users[u]['friends'] = friends
    users[u]['words'] = words

eta = 0.05
l = 0.4
k = 20
alpha = 0
user_bias = collections.defaultdict(int)
item_bias = collections.defaultdict(int)
friend_bias = collections.defaultdict(int)
p = collections.defaultdict(lambda: [random.random() * (0.6) for _ in range(k)])
q = collections.defaultdict(lambda: [random.random() * (0.6) for _ in range(k)])


def getAlpha():
  total = 0
  for user, item, rating in trainingRatings:
    total += rating
  global alpha 
  alpha = float(total) / len(trainingRatings)

def getFriendRatings(threshold):
  for user in users:
    for item, rating in users[user]['ratings']:
      total = 0
      num = 0
      for friend in users[user]['friends']:
        if friend and wordVectorHelpers.getCosSim(user, friend) > threshold:
          for friend_item, friend_rating in users[friend]['ratings']:
            if item == friend_item:
              total += friend_rating
              num += 1
      friend_ratings[(user, item)] = 0 if total == 0 else total/float(num) - alpha


def predict(user, item):
  return alpha + user_bias[user] + item_bias[item] + np.dot(p[user], q[item]) \
    + friend_bias[user]*friend_ratings[(user, item)]

def gradientDescent():
  global p, q
  for x in range(100):
    for user, item, rating in trainingRatings:
      error = rating - predict(user, item)
      user_bias[user] += eta * (error - l * user_bias[user])
      user_bias[item] += eta * (error - l * user_bias[item])
      friend_bias[user] += eta * (error * friend_ratings[(user, item)] - l * friend_bias[user])
      for i in range(k):
        p[user][i] += eta * (error * q[item][i] - l * p[user][i])
        q[item][i] += eta * (error * p[user][i] - l * q[item][i])

def testError():
  error = 0
  for user, item, rating in testRatings:
    error += (rating - predict(user, item))**2
  print "TEST MSE: ", error/len(testRatings)

def trainingError():
  error = 0
  for user, item, rating in trainingRatings:
    error += (rating - predict(user, item))**2
  print "TRAINING MSE: ", error/len(trainingRatings)

def baselineError():
  error = 0
  for user, item, rating in trainingRatings:
    error += (rating - alpha)**2
  print "BASELINE MSE: ", error/len(trainingRatings)

if __name__ == '__main__':
  parseUserFile()
  getAlpha()
  getFriendRatings(threshold)
  gradientDescent()
  testError()
  trainingError()
  baselineError()



