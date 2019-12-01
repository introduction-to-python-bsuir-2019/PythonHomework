#!/usr/bin/python
def create_split(input_str: str,char: str) -> list:
  indexs: list=[]
  indexs.append(-1)
  indexs.extend(i for i, symbol in enumerate(input_str) if symbol==char)
  indexs.append(len(input_str))
  lst: list=[]
  for i in indexs[:len(indexs)-1:]:
     lst.append(input_str[i+1:indexs[indexs.index(i)+1]:])
  return lst

def split_by_index(s: str, indexs: list) -> list:
        res: list=[]
        res.append(s[:indexs[0]:])

        for i in indexs:
          if i>len(s):
            break
          if i==indexs[-1]:
            res.append(s[indexs[indexs.index(i)]::])
          else:
            res.append(s[i:indexs[indexs.index(i)+1]:])
        return res

def get_digits(num:int)-> tuple:
  lst: list=[]
  line=str(num)
  lst=list(line)
  lst=[int(i) for i in lst]
  res=tuple(lst)
  return res

def foo(old: list)-> list:
  from functools import reduce
  m=reduce(lambda x,y: x*y,old)
  res: list=[]
  for i in old:
    res.append(int(m/i))
  return

def get_pairs(old: list)-> list:
  if len(old)==1:
     return None
  res: list=[]   
  for i in range(0,len(old)-1):
    tmp:tuple=(old[i],old[i+1])
    res.append(tmp)
  print(res)
  return res

def ispolindrome(line:str)-> bool:
    return line[::]==line[::-1]
   
def replacing(line:str)->str:
  for i in line:
    if i=='\'':
      line=line[:line.index(i):]+'\"'+line[line.index(i)+1::]
    if i=='\"':
      line=line[:line.index(i):]+'\''+line[line.index(i)+1::]
      
  return line

def get_longest_word(s: str)-> str:
   return max(s.split(' '),key=len)
