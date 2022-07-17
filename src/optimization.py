def result(index, margin, estim):
    sum = 0
    for i in range(len(index)):
        sum += margin[i][index[i]]*estim[i][index[i]]
    return sum

def main():

    margin = [[1,2,3,4],
              [1,2,3,4],
              [1,2,3,4],
              [1,2,3,4],
              [1,2,3,4]]
    estim  = [[40,30,10,50], # ne doit pas aller jusquau 500
              [40,30,22,20],
              [40,30,20,10],
              [40,30,21,10],
              [40,12,20,10]]

    index = [0,0,0,0,0]

    res = result(index, margin, estim)
    max = res # to enter
    cmp =0
    while max!=0: #while the marginal increase doesn't move
        best_index = index.copy() # buffer to re init from the current compositions
        max = 0   # first marginal is 0
        best_res = 0 # to update the res
        for i in range(len(index)):
            
            current = best_index.copy() # take the current disposition
            if(current[i]<len(margin[i])-1): # (under 3 because 4 possible choice)
                current[i]+=1     # shift i price if possible 
            else:
                pass
            cmp+=1
            tmp = result(current, margin, estim) # compute result with this composition
            if tmp-res > max:  # if result is better than the current best result
                max = tmp - res #  we update the marginal increase
                best_res = tmp
                index = current.copy()  # we change the best choice of index
        res = best_res # update the result for the next iteration

    print(index, result(index, margin, estim), cmp)


if __name__ == "__main__":
	main()




# marche aussi, premier mais prends pas forcement le meilleur a chaque step, juste le dernier meilleur
""" while max!=0:
  max=0
  best = index.copy()
  for i in range(len(index)):
      current = best.copy() # take the current disposition
      if(current[i]<len(margin[i])-1): # (under 3 because 4 possible choice)
          current[i]+=1     # shift i price if possible 
      tmp = result(current, margin, estim) # compute result with this composition
      if tmp>res:  # if result is better than the current best result
          max = tmp # we update
          index = current  #
  res = max"""