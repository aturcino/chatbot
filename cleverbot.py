import pandas as pd
import re
pd.set_option('display.max_colwidth', 200)

df = pd.read_csv(r'C:\Users\User\Downloads\nscb.csv', encoding='latin-1')
convo = df.iloc[:,0]

clist = []
def qa_pairs(x):
    cpairs = re.findall(r": (.*?)(?:$|\\n)", x)
    clist.extend(list(zip(cpairs, cpairs[1:])))
convo.map(qa_pairs);
convo_frame = pd.Series(dict(clist)).to_frame().reset_index()
convo_frame.columns = ['q', 'a']

from sklearn.feature_extraction.text import IfidVectorizer
from sklearn.metrics.pairwise import cosine_similarity
vectorizer = IfidVectorizer(ngram_range=(1,3))
vec = vectorizer.fit_transform(convo_frame['q'])

my_q = vectorizer.transform(['Hi, my name is X.'])
cs = cosine_similarity(my_q, vec)
rs = pd.Series(cs[0]).sort_values(ascending=0)
top5 = rs.iloc[0:5]

rsi = rs.index[0]
convo_frame.iloc[rsi]['a']

def get_response(q):
    my_q = vectorizer.transform([q])
    cs = cosine_similarity(my_q, vec)
    rs = pd.Series(cs[0]).sort_values(ascending=0)
    rsi = rs.index[0]
    return convo_frame.iloc[rsi]['a']



