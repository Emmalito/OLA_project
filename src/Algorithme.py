"""
    It is the implementation of the greedy algorithm
    that we use to maximise the margin. To simplify,
    here we assume that the prices = margins to simplify 
"""

def result(index, margin, expectedSales):
    """Compute the objective function and return the result"""
    sum = 0
    for i in range(len(index)):
        sum += margin[i][index[i]]*expectedSales[i][index[i]]
    return sum


def reachWebPage(graphWeights, alphas):
    """Define the probability to reach the web pages"""
    probas = []
    for index in range(5):
        proba = alphas[index]
        probas.append(proba)
    
    return probas


def optimization(margin, convRates, alphas, nbItemSold, nbUsers, graphWeights):
    """Run the optimisation algorithm"""

    probas = reachWebPage(graphWeights, alphas)
    expectedSales = [[convRates[e][i]*margin[e][i]*nbUsers*nbItemSold[i] for i in range (len(convRates[e]))] for e in range(len(convRates))]
    for product in expectedSales:
        index = 0
        for sale in product:
            sale = sale * alphas[index]
            index += 1
    
    index = [0 for _ in range(len(margin))]

    valueObjectifFunc = result(index, margin, expectedSales)
    max = valueObjectifFunc # to enter
    cmp =0
    while max!=0: #while the marginal increase doesn't move
        best_index = index.copy() # buffer to re init from the current compositions
        max = 0   # first marginal is 0
        best_res = 0 # to update the valueObjectifFunc
        for i in range(len(index)):
            
            current = best_index.copy() # take the current disposition
            if(current[i]<len(margin[i])-1): # (under 3 because 4 possible choice)
                current[i]+=1     # shift i price if possible 
            else:
                pass
            cmp+=1
            tmp = result(current, margin, expectedSales) # compute result with this composition
            if tmp-valueObjectifFunc > max:  # if result is better than the current best result
                max = tmp - valueObjectifFunc #  we update the marginal increase
                best_res = tmp
                index = current.copy()  # we change the best choice of index
        valueObjectifFunc = best_res # update the result for the next iteration

    return index, result(index, margin, expectedSales), cmp


if __name__ == "__main__":
    margin = [[1, 2, 4, 8], [2, 3, 5, 13],
              [2, 5, 8, 10], [3, 5, 6, 9], [4, 7, 9, 13]]
    priceReservation = 5
    convRates = [[max((1-i/priceReservation), 0) for i in margin[e]] for e in range(len(margin))]
    alphas = [0.2,0.3,0.2,0.3]
    nbItemSold = [50, 47, 30, 20, 1]
    nbUsers = 15
    graphWeights = [0.2,0.3,0.2,0.3]

    optimalIndex, result, nbStep = optimization(margin, convRates, alphas, nbItemSold, nbUsers, graphWeights)
    print(optimalIndex)
