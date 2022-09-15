import tarfile
import glob
import sys
import re
import nltk
from nltk import word_tokenize
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from collections import defaultdict
import pickle

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def query_process(path):
  name=path
  with open(name, 'r') as file:
        data=file.read().replace('\n', '')
  tag = "num"
  
  # regex to extract required strings
  reg_str = "<" + tag + ">(.*?)</" + tag + ">" #get query number
  res1 = re.findall(reg_str, data)

  tag = "title"
  
  # regex to extract required strings
  reg_str = "<" + tag + ">(.*?)</" + tag + ">" #get query by extracting text of title tag
  res2 = re.findall(reg_str, data)
  res=[]
  for i in range (len(res2)): #query preprocessing
    text = res2[i].lower() # lower case conversion
    text_p = "".join([char for char in text if char not in string.punctuation]) #punctuation removal
    words = word_tokenize(text_p)
    stop_words = stopwords.words('english')

    filtered_words = [word for word in words if word not in stop_words] #stop word removal
    # Init the Wordnet Lemmatizer
    lemmatizer = WordNetLemmatizer()
    lemmatized_output = ' '.join([lemmatizer.lemmatize(w) for w in filtered_words]) #lemmatization
    res.append(lemmatized_output)

  file1 = open('queries_12.txt', 'w')
  for i in range (len(res1)):
    file1.write(res1[i]+','+res[i]+'\n') #writing processed queries

  file1.close()

def main():
  path=sys.argv[1]
  query_process(path)

if __name__=="__main__":
    main()