# Importando las Librerias
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction import text

df = pd.read_csv('./data/turismo_real.csv', delimiter=',', encoding="utf-8")
# Creamos una columna que contiene la combinacion de columnas productos y salas
df['content'] = df[['rooms', 'products']].astype(str).apply(lambda x: ' // '.join(x), axis = 1)
# Fillna
df['content'].fillna('Null', inplace = True)
# Entrenando el recomendador
my_stop_words = list(text.ENGLISH_STOP_WORDS.union(["spanish"]))
tf = TfidfVectorizer(analyzer = 'word', ngram_range = (1, 2), min_df = 0, stop_words = my_stop_words)
tfidf_matrix = tf.fit_transform(df['content'])
# Similitud de coseno
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

results = {}
for idx, row in df.iterrows():
    similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
    similar_items = [(cosine_similarities[idx][i], df['id'][i]) for i in similar_indices]
    results[row['id']] = similar_items[1:]

# Prediction
def item(id):
    name   = df.loc[df['id'] == id]['content'].tolist()[0].split(' // ')[0]
    desc   = ' \nProducts: ' + df.loc[df['id'] == id]['content'].tolist()[0].split(' // ')[1][0:165] + '...'
    prediction = name  + desc
    return prediction

def recommend(item_id, num) -> list:
    recommendations = []
    print('Recommending ' + str(num) + ' dwellings similar to DWELLING ID :' + str(item_id))
    print('---')
    recs = results[item_id][:num]
    for rec in recs:
        print('\nRecommended: Dwelling ' + str(rec[1]) + ' ' + item(rec[1]) + '\n(score:' + str(rec[0]) + ')')
        recommendations.append({'id' : rec[1] , 'score' : round(rec[0],2)})
    return recommendations

