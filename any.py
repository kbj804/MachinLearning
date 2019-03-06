# 텍스트 사전 준비 작업(텍스트 전처리) - 텍스트 정규화
from nltk import word_tokenize, sent_tokenize
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import LancasterStemmer

text_sample = 'The Matrix is everywhere its all around us, here even in this room. \
               You can see it out your window or on your television. \
               You feel it when you go to work, or go to church or pay your taxes.'
stemmer = LancasterStemmer()
lemma = WordNetLemmatizer()


# 여러개의 문장으로 된 입력 데이터를 문장별로 단어 토큰화 만드는 함수 생성
def tokenize_text(text):
    # 문장별로 분리 토큰
    sentences = sent_tokenize(text)
    # 분리된 문장별 단어 토큰화
    word_tokens = [word_tokenize(sentence) for sentence in sentences]
    return word_tokens


# 여러 문장들에 대해 문장별 단어 토큰화 수행.
word_tokens = tokenize_text(text_sample)
#print(type(word_tokens), len(word_tokens))
#print(word_tokens)
stopwords = nltk.corpus.stopwords.words('english')
stopwords.append('\'s')
stopwords.append('n\'t')

print('영어 stop words 갯수:',len(stopwords))
print(stopwords[:len(stopwords)])

# Stop word 제거

all_tokens = []
# 위 예제의 3개의 문장별로 얻은 word_tokens list 에 대해 stop word 제거 Loop
for sentence in word_tokens:
    filtered_words = []
    # 개별 문장별로 tokenize된 sentence list에 대해 stop word 제거 Loop
    for word in sentence:
        # 소문자로 모두 변환합니다.
        word = word.lower()
        # tokenize 된 개별 word가 stop words 들의 단어에 포함되지 않으면 word_tokens에 추가
        if word not in stopwords:
            filtered_words.append(word)
    all_tokens.append(filtered_words)

#print(all_tokens)