import re
import os
from nltk import sent_tokenize
from nltk.corpus import stopwords
stopwords = set(stopwords.words('english'))
from gensim.models.phrases import Phrases, Phraser
from gensim.models import Word2Vec
#from gensim.models import FastText
import psutil
import logging
logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)

def get_sentences(input_file_pointer):
    while True:
        line = input_file_pointer.readline()
        if line == '\n':
            continue
        yield line
        
def clean_sentence(sentence):
    sentence = sentence.lower().strip()
    sentence = re.sub(r'[^a-z0-9\s]', '', sentence)
    return re.sub(r'\s{2,}', ' ', sentence)

def tokenize(sentence):
    return [token for token in sentence.split() if token not in stopwords]

def build_phrases(sentences):
    phrases = Phrases(sentences,
                      min_count=5,
                      threshold=7,
                      progress_per=1000)
    return Phraser(phrases)

def build_n_gram_phraser(path):
    """
    return the tokenized processed sentences 
    """
    sentences = []
    c = 0
    for i, file in enumerate(os.listdir(path)):
        file = path + file
        with open(file, 'r', encoding = 'utf-8') as infile:
            for sent_list in infile:
                sent = sent_list.split('.')
                for s in sent:
                    s = tokenize(clean_sentence(s))
                    c += len(s)
                    sentences.append(s)
   
        print(i, psutil.virtual_memory()[2], c)
        if i == 150:
            break
    print("Documents loaded.\n")
        
    phrases_model = build_phrases(sentences)
    sentences = [phrases_model[line] for line in sentences]
    print('Bigrams created.\n')
    
    phrases_model = build_phrases(sentences)
    sentences = [phrases_model[line] for line in sentences]
    print('Trigrams created.\n')
    
    phrases_model = build_phrases(sentences)
    sentences = [phrases_model[line] for line in sentences]
    print('Quadgrams created.\n')

    savefile = 'phrases_model_150.txt'
    phrases_model.save(savefile)
    print('Phrase model saved to file.\n')    
    return sentences
    
    
def sentence_to_n_grams(phrases_model, sentence):
    return ' '.join(phrases_model[sentence])

def sentences_to_n_grams(phrases_model, sentences):
    """
    return the parsed n-gram containing sentences
    """
    parsed = []
    for i, sentence in enumerate(sentences):
        sent = phrases_model[sentence]
        parsed.append(sent)
        #print(i)
    print('Phrases made.\n')
    return parsed

if __name__ == "__main__":
    path = 'batch_data/'
    sentences = build_n_gram_phraser(path)
    phrases_model = Phraser.load('phrases_model_150.txt')
    parsed = sentences_to_n_grams(phrases_model, sentences)
    
    model = Word2Vec(parsed, size=300, window=3, workers=10, alpha=0.01, negative=5)
    model.train(parsed, total_examples=len(parsed), epochs=50)
    model.save('word2vec_2.model')
    print('Word2Vec is created.\n')
    
    """    
    fast = FastText(size=300, window=5, workers=10, alpha=0.01, negative=10)
    fast.build_vocab(sentences=parsed)
    fast.train(sentences=parsed, total_examples=len(parsed), epochs=10)
    fast.save('fasttext_1.model')
    """
    
#words = list(model.wv.vocab)
"""
model.most_similar('hypertension')
model.similarity('hypertension','blood_pressure')
model.wv.save_word2vec_format('model.bin')
model.save('word2vec.model')
test = Word2Vec.load('word2vec.model')
test.most_similar('hypertension')

import re
def generate_ngrams(s, n):
    s = s.lower()
    s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)
    tokens = [token for token in s.split(" ") if token != ""]
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]

generate_ngrams()

phrasefile = 'E:/SIH/pubmed-phrases/all_dictionary.txt'
tagged_phrases = open('E:/SIH/pubmed-phrases/tagged_phrases', 'w')
with open(phrasefile, 'r') as phrases:
    for line in phrases:
        line = line.replace(' ', '_')
        tagged_phrases.write(line)
        
phrases = []
tagged = 'E:/SIH/pubmed-phrases/tagged_phrases'
with open(tagged, 'r') as tmp:
    for line in tmp:
        phrases.append(line.strip())
        


    
phrases = Phrases(sentences, min_count=1)
bigram = Phraser(phrases)
sent = [u'coke', u'combustion']
bigram[sent]
for key in phrases.vocab.keys():
    print(key)
"""
