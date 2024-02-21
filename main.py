import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, Dot, Flatten, Dense
from tensorflow.keras.models import Model
from scipy import sparse

# Carregar o conjunto de dados
data = pd.read_csv("./data/BR_youtube_trending_data.csv")

# Selecionar as colunas relevantes
data = data[['video_id', 'title', 'channelId', 'tags']]

# Remover linhas com valores ausentes
data = data.dropna()

# Dividir as tags em listas
data['tags'] = data['tags'].apply(lambda x: x.split('|'))

# Codificar os rótulos categóricos
label_encoder = LabelEncoder()
data['video_id'] = label_encoder.fit_transform(data['video_id'])
data['channelId'] = label_encoder.fit_transform(data['channelId'])

# Dividir os dados em conjuntos de treinamento e teste
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Transformar as listas de tags em texto
train_data['tags_str'] = train_data['tags'].apply(lambda x: ' '.join(x))
test_data['tags_str'] = test_data['tags'].apply(lambda x: ' '.join(x))

# Utilizar CountVectorizer para vetorizar as tags como matrizes esparsas
vectorizer = CountVectorizer(binary=True)
train_tags_encoded = vectorizer.fit_transform(train_data['tags_str'])
test_tags_encoded = vectorizer.transform(test_data['tags_str'])

# Dividir os dados de treinamento em conjuntos de treinamento e validação
train_tags_encoded, val_tags_encoded = train_test_split(train_tags_encoded, test_size=0.2, random_state=42)

# Definir as dimensões de embedding
embedding_dim = 50

# Definir o número de itens e usuários
num_videos = len(data['video_id'].unique())
num_channels = len(data['channelId'].unique())

# Criar a entrada para o vídeo e o canal
video_input = Input(shape=(1,))
channel_input = Input(shape=(1,))

# Criar as camadas de embedding
video_embedding = Embedding(num_videos, embedding_dim, input_length=1)(video_input)
channel_embedding = Embedding(num_channels, embedding_dim, input_length=1)(channel_input)

# Calcular o produto escalar entre os embeddings
dot_product = Dot(axes=2)([video_embedding, channel_embedding])
dot_product = Flatten()(dot_product)

# Adicionar camadas densas para prever as tags
dense1 = Dense(64, activation='relu')(dot_product)
output = Dense(train_tags_encoded.shape[1], activation='softmax')(dense1)

# Construir o modelo
model = Model(inputs=[video_input, channel_input], outputs=output)

# Compilar o modelo
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Resumo do modelo
model.summary()

# Treinar o modelo
history = model.fit([train_data['video_id'], train_data['channelId']], train_tags_encoded.toarray(), epochs=10, batch_size=32, validation_data=([val_data['video_id'], val_data['channelId']], val_tags_encoded.toarray()))

# Avaliar o modelo
loss, accuracy = model.evaluate([test_data['video_id'], test_data['channelId']], test_tags_encoded.toarray())
print(f"Test Loss: {loss}, Test Accuracy: {accuracy}")