import pickle
from nltk import word_tokenize
import nltk
import torch
import sys
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def merge_two_lists(a,b): #merge two lists containing doc ids sorted lexicographically
  c=[]
  i=0
  j=0
  while True:
    if(i==len(a) or j==len(b)):
      break
    if(a[i]==b[j]):
      c.append(a[i])
      i=i+1
      j=j+1
      if (i==len(a) or j==len(b)):
        break
    elif (a[i]>b[j]):
      j=j+1
      if(j==len(b)):
        break
    else:
      i=i+1
      if (i==len(a)):
        break
  return c

def merge_postings(postings,word_list): #merging postings list
  lists=[]
  for i in range (len(word_list)):
    lists.append(postings[word_list[i]])
  if(len(lists)==0):
    return ("")
  
  lists.sort(key=len) #sorting relevant lists in increasing order of length
  a=lists[0]
  for i in range (1,len(lists)):
    a=merge_two_lists(a,lists[i])
  result=""
  for i in range(len(a)):
    result=result+" "+a[i]

  return result

def boolean_ret(path_list,path_query):  #retrieval using AND logic
  postings = torch.load(path_list)
  file1 = open(path_query, 'r')
  count = 0
  file2 = open('PAT1_12_results.txt', 'w')
  while True:
      line = file1.readline()
      if not line:
          break
      string_list = line.split(",")
      word_list=word_tokenize(string_list[1])
      doclist=merge_postings(postings,word_list)
      file2.write(string_list[0]+' : '+doclist+'\n')
  file2.close()

def main():
  path_list=sys.argv[1]
  path_query=sys.argv[2]
  boolean_ret(path_list,path_query)

if __name__=="__main__":
    main()

    

