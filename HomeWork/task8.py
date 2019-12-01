
# Python3 code to demonstrate  
# pair iteration in list  
# using list comprehension 
from itertools import compress 
  
# initializing list   
test_list = [0, 1, 2, 3, 4, 5] 
  
# printing original list 
print ("The original list is : " + str(test_list)) 
  
# using list comprehension 
# to perform pair iteration in list  
res = [((i), (i + 1) % len(test_list))  
         for i in range(len(test_list))] 
  
# printing result 
print ("The pair list is : " + str(res)) 


