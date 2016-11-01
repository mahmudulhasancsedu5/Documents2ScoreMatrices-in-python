import preprocessor as p
tweet="32 2 285 228156838519128064	The United States leads the world in gun ownership per capita. Yemen comes in a distant second. #USA! #USA! http://t.co/YuSnP1Gn"
x=p.clean(tweet)

print str(x)
#-------------------stopword removing-----------

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from nltk.stem.porter import PorterStemmer
porter = PorterStemmer()

stop_words=set(stopwords.words("english"))
example_sent="The cockpit voice recorder and the flight-data recorder were each recovered hours after the crash and flown to Washington, D,walking,talking,formally"
example_sent=example_sent.lower()
print example_sent 
'''
example_words = word_tokenize(example_sent)
print example_words
example_words = filter(lambda x: x not in string.punctuation, example_words)

print example_words
cleaned_text = filter(lambda x: x not in stop_words, example_words)

print cleaned_text
'''
#ii="228156838519128064	The United States leads the world in gun ownership per capita. Yemen comes in a distant second. #USA! #USA! http://t.co/YuSnP1Gn"
cleaned_all=[str(porter.stem(i.lower())) for i in word_tokenize(x) if i not in string.punctuation and  i.lower() not in stop_words ]

print cleaned_all
