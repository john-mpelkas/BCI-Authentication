#Example is from this video: https://www.youtube.com/watch?v=cuD-LXic2cE
import numpy as np

x1 = [1, 5, -8]
x2 = [3, 2, 1, 6, -7]

def lenOfCorrArr(l1, l2): #determine length of results matrix
  return (l1 + l2) - 1 

matLen = lenOfCorrArr(len(x1), len(x2))

results_matrix = np.zeros((matLen + 1, matLen)) #create results matrix

def popMat(l1, popRow):
  for count, i in enumerate(l1):
    results_matrix[popRow][count] = i

popMat(x1, 0)
popMat(x2, 1) #populate the matrix with the inital values 

def fillMat(array):
  for i in range(2, len(array)):
    for j in range(0, len(array[i])):
      print(i, j)
      if j+1 >= len(array[i]):
        array[i][j] = array[i-1][0]
      else: 
        array[i][j] = array[i-1][j+1]

fillMat(results_matrix)

def produceCorrValues(array): #this is where we compare everything to the 0th row
  #just multiply each j value with the j value in row 0 and then sum
  tempArr = []
  for i in range(1, len(array)):
    a = 0
    for j in range(0, len(array[0])):
      a += array[0][j] * array[i][j]
    tempArr.append(a)
  return tempArr


resultsArray = produceCorrValues(results_matrix)

print("MAXIMUM CORRELATION VALUE: ", max(resultsArray))
print("MAX CORRELATION VALUE INDEX: ", resultsArray.index(max(resultsArray)))
