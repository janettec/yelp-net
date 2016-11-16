import util, math, copy

# Checks if oldWeights and newWeights are the same to within 7 decimal points
def weightsAreSame(oldWeights, newWeights):
    for key in oldWeights:
        if round(oldWeights[key], 7) != round(newWeights[key], 7):
            return False
    return True

# def stochasticGradientDescent(split, data, sdF):
#     for p in range(3):  #try 1, 2, 3 days before as predictors 
#         numDays = p + 1
#         for j in range(10): # 10-fold data split to get error estimate
#             n = len(data) - numDays
#             w = getInitialWeights(numDays)
#             oldW = copy.deepcopy(w)
#             numIters = 1000
#             for t in range(numIters):
#                 eta = 0.00001
#                 util.debugPrint("iteration %d: w = %s" % (t, w))

#                 weightsHaveConverged = False

#                 for i in range(n): # loop through each example in the data
#                     if split[i] == j: continue # train model on 9/10 of data
#                     #value = sF(data, w, i)
#                     gradient = sdF(data, w, i, numDays)

#                     # gradient = gradient * eta
#                     util.scaleDict(gradient, eta)
#                     util.debugPrint("SCALED GRADIENT: ")
#                     util.debugPrint(gradient)

#                     # weights = weights - gradient
#                     util.subtractDict(w, gradient)
#                     util.debugPrint("WEIGHTS:")
#                     util.debugPrint(w)

#                     # stop if weights are not changing
#                     if weightsAreSame(oldW, w):
#                         #return w
#                         weightsHaveConverged = True # break out of 2 layers of for loops
#                         break
#                     else:
#                         oldW = copy.deepcopy(w)

#                 if weightsHaveConverged:
#                     break

#             print("FINAL WEIGHTS for D_train block %d:" % j)
#             print(w)

#             totalLoss = [0 for k in range(10)]
#             for i in range(n):
#                 if split[i] == j: # estimate error on remaining 1/10 of data
#                     totalLoss[j] += sF(data, w, i, numDays)
#             print("TOTAL LOSS for D_val block %d:" % j)
#             print(totalLoss[j])

#     return w

# allData: array of all data
# trainExamples: array of the indices of the training examples in allData
# key: weather metric that we are trying to predict
# numDays: # of days in the past to use to predict future weather
def stochasticGradientDescent(allData, trainExamples, key, numDays):
    # hyperparameters
    numIters = 200
    eta = 0.0001

    # initialize weights
    w = getInitialWeights(key, numDays)
    loss = trainLoss(allData, trainExamples, w, numDays, key)
    util.debugPrint("initial: w = %s, loss = %.4f" % (util.roundDictValues(w,4), loss))

    for t in range(1, numIters+1):
        oldW = copy.deepcopy(w)

        for i in trainExamples: # loop through each training example
            # loss = sF(allData, w, i)
            gradient = sdF(allData, w, i, key, numDays)

            # gradient = gradient * eta
            util.scaleDict(gradient, eta)

            # weights = weights - gradient
            util.subtractDict(w, gradient)
            # util.debugPrint("iteration %d | example %d: w = %s" % (t, i, w))

        # print weights and loss
        loss = trainLoss(allData, trainExamples, w, numDays, key)
        # util.debugPrint("iteration %d: w = %s, loss = %.4f" % (t, util.roundDictValues(w,4), loss))

        if weightsAreSame(oldW, w):
            break
    
    # util.debugPrint("iteration %d: w = %s, loss = %.4f" % (t, util.roundDictValues(w,4), loss))
    return w

# SQUARED LOSS FUNCTION
def sF(data, w, i, numDays, key):
    x = extractFeatures(data, i, numDays)
    y = data[i + numDays][key]
    return (util.dictDot(w,x) - y)**2

# average loss over all training data examples
def trainLoss(data, trainExamples, w, numDays, key):
    totalLoss = 0
    for i in trainExamples:
        totalLoss += sF(data, w, i, numDays, key)
    return totalLoss / float(len(trainExamples))

# LOSS FUNCTION DERIVATIVE
# Computes the stochastic gradient of the weight vector
# parameters
# - data    : array of all data
# - w       : weight vector
# - i       : index of day that we are predicting
# - key     : weather metric
# - numDays : number of days in the past the we are dealing with
# gradient_w = (w * x - y) * x
def sdF(data, w, i, key, numDays):
    # print "key:", key
    # print "Weights:", w
    x = extractFeatures(data, i, numDays)
    # print "Features:", x
    y = data[i + numDays][key]
    # print "Truth:", y
    z = copy.deepcopy(x)
    lam = 0 # set to 0 if you don't want parameter regularization
    util.scaleDict(z, 2 * (util.dictDot(w, x) - y) + lam*math.sqrt(util.dictDot(w,w)))
    # print "Prediction:", util.dictDot(w, x)
    # print "Gradient:", z
    return z

# data: array of dicts for each day
# i: the number of the first example that we want to extract features from
# numDays: the number of previous days we want to look at
def extractFeatures(data, i, numDays):
    features = {}
    for day in range(numDays):
        for key in util.keys:
            features[key + str(day)] = data[i + day][key]
    return features

# Initialize all weights to 0, except for the key that we want, which we set
# such that we take the average of the past numDays
def getInitialWeights(key, numDays):
    w = {}
    for day in range(numDays):
        for k in util.keys:
            w[k + str(day)] = 0 # ie. w['TempHigh0'] = 0

        w[key + str(day)] = 1.0 / numDays

    return w

def run(allData, train, test, numDays, std_dev, keys):
    # Train weights using stochastic gradient descent on training set
    print "=====Training Weights using SGD on Training Set====="
    weights = {}
    for key in keys:
        print "Learning", key, "weights"
        weights[key] = stochasticGradientDescent(allData, train, key, numDays)

    # Caculate root-mean-squared (RMS) errors (in std. deviations away from the expected value) on test set
    print "=====Final Errors====="
    print " - MS Error (std): mean squared error in std. deviations away from the expected value"

    for key in keys:
        print "--", key, "Weights:" # ie. -- TempHigh Weights
        print util.roundDictValues(weights[key], 4)
        print "  Train MSE (std):", trainLoss(allData, train, weights[key], numDays, key)
        print "  Test MSE (std):", trainLoss(allData, test, weights[key], numDays, key)
        print ""