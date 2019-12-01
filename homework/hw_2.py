#!/usr/bin/python
def generate_squares(numb: int)-> dict:
   mydict: dict={}
   for i in range(1,numb+1):
       mydict[i]=i*i
   return mydict
def count_letter(s:str)->dict:
    mydict: dict={}
    for x in s:
        if x in mydict:
            mydict[x]=mydict[x]+1
        else:
            mydict[x]=1
    return mydict            

def combine_dict(*args)->dict:
    mydict: dict={}
    for item in args:
        for x in item:
          if x in mydict:
            mydict[x]=mydict[x]+item[x]
          else:
            mydict[x]=item[x]
    return mydict        

def test_4(*strings)->set:
    import string
    myset=set()
    tmp=set()
    myset.update(string.ascii_lowercase)
    for x in strings:
        tmp=tmp | set(x)  
    myset=myset-tmp
    print(myset)
      
    return myset
def test_1(*strings)->set:

    tmp=set(strings[0])
    for x in strings[1::]:
        tmp=tmp & set(x)  
    print(tmp)
      
    return tmp
def test_2(*strings)->set:
    tmp=set()
    for x in strings:
        tmp=tmp | set(x) 
    print(tmp)
    return tmp 

def test_3(*strings)->set:
    tmp=set()
    myset=set()
  
    for i,x in enumerate(strings[:len(strings)-1:]):
        tmp=set(x)
        for t in strings[i+1::]:
            myset=myset|(tmp&set(t))    
    return myset

print(test_3("hello", "world","python",))
