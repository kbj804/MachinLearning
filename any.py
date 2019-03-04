import urllib.request
from collections import Counter

import numpy as np

from nltk import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer

# Our sample textfile.
url = 'http://amsterdamsexxx.com'
response = urllib.request.urlopen(url)
data = response.read().decode('utf8')


# Note that `ngram_range=(1, 1)` means we want to extract Unigrams, i.e. tokens.
ngram_vectorizer = CountVectorizer(analyzer='word', tokenizer=word_tokenize, ngram_range=(1, 1), min_df=1)
# X matrix where the row represents sentences and column is our one-hot vector for each token in our vocabulary
X = ngram_vectorizer.fit_transform(data.split('\n'))

# Vocabulary
vocab = list(ngram_vectorizer.get_feature_names())

# Column-wise sum of the X matrix.
# It's some crazy numpy syntax that looks horribly unpythonic
# For details, see http://stackoverflow.com/questions/3337301/numpy-matrix-to-array
# and http://stackoverflow.com/questions/13567345/how-to-calculate-the-sum-of-all-columns-of-a-2d-numpy-array-efficiently
counts = X.sum(axis=0).A1

freq_distribution = Counter(dict(zip(vocab, counts)))
print (freq_distribution.most_common(10))