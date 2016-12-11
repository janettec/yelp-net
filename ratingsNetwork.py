import numpy as np
import collections
import random
import wordVectorHelpers

users = {}
friend_ratings = {}
trainingRatings = set()
testRatings = set()
crossValRatings = []

# cosSimThreshold = 0.93
# print "Cosine Simularity Threshold: ", cosSimThreshold

def parseUserFile():
  f = open('graphAttributesWaterloo.txt', 'r')
  numFriends, friendsPruned, numUsers = 0, 0, 0
  for line in f:
    u, r, f, w = line.split("|")
    ratings = set()
    ratingsVec = r.split(',')
    for i in range(0, len(ratingsVec), 2):
      # crossValRatings.append((u, ratingsVec[i], int(ratingsVec[i+1])))
      if random.random() > 0.8:
        testRatings.add((u, ratingsVec[i], int(ratingsVec[i+1])))
      else:
        trainingRatings.add((u, ratingsVec[i], int(ratingsVec[i+1])))
      ratings.add((ratingsVec[i], int(ratingsVec[i+1])))

    friends = set(f.split(','))
    # friendCandidates = set(f.split(','))
    # numFriends += len(friendCandidates)
    # friends = set()
    # for friend in friendCandidates:
    #   cosSim = wordVectorHelpers.getCosSim(u, friend)
    #   if cosSim is not None and cosSim >= cosSimThreshold:
    #     friends.add(friend)
    #   else:
    #     friendsPruned += 1
    # numUsers += 1
    # words = {}
    # wordsVec = w.split(',')
    # for i in range(0, len(wordsVec) - 1, 2):
    #   words[wordsVec[i]] = wordsVec[i+1]
    users[u] = {}
    users[u]['ratings'] = ratings
    users[u]['friends'] = friends
    # users[u]['words'] = words
  # print "Average prunes: %s" % (friendsPruned / float(numUsers))
  # print "Average friends: %s" % (numFriends / float(numUsers))

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
        if friend:# and wordVectorHelpers.getCosSim(user, friend) > threshold:
          for friend_item, friend_rating in users[friend]['ratings']:
            if item == friend_item:
              total += friend_rating #* wordVectorHelpers.getCosSim(user, friend)
              # num += wordVectorHelpers.getCosSim(user, friend) + 0.05
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

def crossValidate():
  global testRatings, trainingRatings
  random.shuffle(crossValRatings)
  numSamples = len(crossValRatings)
  sectionSize = numSamples / 10
  startIndices = range(0, numSamples, sectionSize)
  startIndices = startIndices[:10]
  print numSamples
  print startIndices
  for i in startIndices:
    print "Section %d:" % (i / sectionSize)
    endIndex = i + sectionSize if i != startIndices[-1] else numSamples
    testRatings = set(crossValRatings[i:endIndex])
    trainingRatings = set(crossValRatings[0:i] + crossValRatings[endIndex:])
    reset()
    getAlpha()
    print alpha
    getFriendRatings()
    gradientDescent()
    testError()
    trainingError()
    baselineTestError()
    baselineTrainingError()

if __name__ == '__main__':
  parseUserFile()
  # crossValidate()
  getAlpha()
  getFriendRatings(0.9)
  gradientDescent()
  testError()
  trainingError()
  baselineError()



