import tarfile
import glob
import re
import nltk
from nltk import word_tokenize
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from collections import defaultdict
import pickle
import torch
import sys

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def unique(list1):
     
    list_set = set(list1)
    unique_list = (list(list_set))
    return unique_list

def sort_postings(Postings):
  for key in Postings:
    Postings[key].sort()

  return Postings

def inverted_index_text(path):
  Postings = defaultdict(list)
  for name in glob.glob(path+'/*/*'):
      with open(name, 'r') as file:
        data=file.read().replace('\n', '')
      pattern=r"<TEXT>(.*?)</TEXT>"  
      text=re.findall(pattern, data,re.DOTALL)  #extract text in TEXT tags
      pattern=r"<DOCNO>(.*?)</DOCNO>" 
      filename=re.findall(pattern, data,re.DOTALL)[0] #extract doc ID
      #print(text)
      text = text[0].lower() #to lower case
      text_p = "".join([char for char in text if char not in string.punctuation]) #punctuation removal
      words = word_tokenize(text_p)
      stop_words = stopwords.words('english') #get stops words in english

      filtered_words = [word for word in words if word not in stop_words] #remove stop words
      # Init the Wordnet Lemmatizer
      lemmatizer = WordNetLemmatizer()
      lemmatized_output = ' '.join([lemmatizer.lemmatize(w) for w in filtered_words])
      final_words=word_tokenize(lemmatized_output)
      final_words=unique(final_words) #get unique words in the doc
      for i in range (len(final_words)):
        Postings[final_words[i]].append(filename) #append file names to postings list
  
  Postings=sort_postings(Postings) #sort postings list docs lexicographically to help merging of lists
  torch.save(Postings, 'model_queries.pth')

def main():
  path=sys.argv[1]
  inverted_index_text(path)

if __name__=="__main__":
    main()

  
    



