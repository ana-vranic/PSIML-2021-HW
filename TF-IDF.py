from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
import glob
import os
import math as mt
import sys
import time
sys.stdout.reconfigure(encoding='utf-8')

def read_file(fname):
    with open(fname, "r", encoding='utf-8') as f:
        data = f.read()
    return data

def calculate_stems_document(document, snow_stemmer):
    words = word_tokenize(document)
    stem_words = [ snow_stemmer.stem(w) for w in words if w.isalnum() ]
    return stem_words

def calculate_Tf_Idf(term_freq, docum_freq, N):
    Tf_Idf = {}
    for t in term_freq:
        tf = term_freq[t]
        idf_tf = mt.log(N/docum_freq[t])*tf
        Tf_Idf[t] = idf_tf
    return Tf_Idf

def calculate_sentence_scores(document, Tf_Idf, snow_stemmer):
    sentences = sent_tokenize(document)
    scores = []
    i = 0
    for sent in sentences:
        stem_words = calculate_stems_document(sent, snow_stemmer)
        sent_df = []
        for w in stem_words: #set
            sent_df.append(Tf_Idf[w])
        scores.append(( sent, i, (sum(sorted(sent_df,  reverse=True)[:10]))))
        i+=1
    return scores

if __name__ == "__main__":

    corpus_path =  input()
    file_input = input()

    snow_stemmer = SnowballStemmer('english')
    document = read_file(file_input)
    stem_words = calculate_stems_document(document, snow_stemmer)
    term_freq = Counter(stem_words)
    corpus_file_paths = glob.glob(os.path.join(corpus_path, '**/*.txt'), recursive=True)
    
    corpus_data = []
    for f in corpus_file_paths:
        corpus_data.append(read_file(f))
    corpus_stems = []
    for file in corpus_data:
        sw = calculate_stems_document(file, snow_stemmer)
        corpus_stems.extend(set(sw))
    docum_freq = Counter(corpus_stems)
    N = len(corpus_file_paths)
    Tf_Idf = calculate_Tf_Idf(term_freq, docum_freq, N)
    sorted_tf = sorted(Tf_Idf.items(), key=lambda x: (-x[1], x[0]))[:10]
    p = [x[0] for x in sorted_tf]
    scores  =  calculate_sentence_scores(document, Tf_Idf, snow_stemmer)
    sort1 = (sorted(scores, key = lambda x:(-x[2])))[:5]
    sort2 = sorted(sort1, key = lambda x: x[1])
    p2 = [x[0] for x in sort2]
    print(*p, sep = ", ")
    print(*p2, sep = " ")