from functools import reduce
from nltk import FreqDist
from nltk.util import ngrams
from nltk.corpus import gutenberg, stopwords

def cleaner(text):
    import re    
    text = [t.lower() for t in text]
    text = [t for t in text if not re.fullmatch('\W+', t)]
    text = [t for t in text if t not in stopwords]
    return text

stopwords = set(stopwords.words('english'))
common_count = 100
max_n = 3

sentences = [cleaner(s) for s in gutenberg.sents('austen-emma.txt')]

join_item = lambda x: ' '.join(x)
common_items = {}
for n in range(1, max_n+1):
    all_text = []
    for sentence in [s for s in sentences if len(s)>1]:
        grams = ngrams(sentence, n)
        for gram in grams:
            all_text.append(gram)
    cur_common = [item[0] for item in FreqDist(all_text).most_common(common_count)]
    if n==1:
        common_items[n] = [join_item(item) for item in cur_common]
    else:
        common_items[n] = []
        for item in cur_common:
            tmp = {x : 0 for x in item}
            for x in range(1,n):
                for gram in ngrams(item, x):
                    if join_item(gram) in common_items[x]:
                        for word in gram:
                            tmp[word] = 1
            if not reduce(lambda x, y: x*y, tmp.values()):
                common_items[n].append(join_item(item))
    common_items[n] = sorted(common_items[n])
for n, val in enumerate(common_items.values()):
    if n==0:
        terms = val
    else:
        terms.extend(val)
terms = sorted(terms)
print(terms)
