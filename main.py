import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from tensorflow.keras.layers import Input, Embedding, Dot, Flatten, Dense
from tensorflow.keras.models import Model
from scipy import sparse

data = pd.read_csv("./data/BR_youtube_trending_data.csv")

data = data[['video_id', 'title', 'channelId', 'tags']]

data = data.dropna()

data['tags'] = data['tags'].apply(lambda x: x.split('|'))

label_encoder = LabelEncoder()
data['video_id'] = label_encoder.fit_transform(data['video_id'])
data['channelId'] = label_encoder.fit_transform(data['channelId'])

train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

train_data['tags_str'] = train_data['tags'].apply(lambda x: ' '.join(x))
test_data['tags_str'] = test_data['tags'].apply(lambda x: ' '.join(x))

vectorizer = CountVectorizer(binary=True)
train_tags_encoded = vectorizer.fit_transform(train_data['tags_str'])
test_tags_encoded = vectorizer.transform(test_data['tags_str'])

train_tags_encoded, val_tags_encoded = train_test_split(train_tags_encoded, test_size=0.2, random_state=42)

embedding_dim = 100

num_videos = len(data['video_id'].unique())
num_channels = len(data['channelId'].unique())

video_input = Input(shape=(1,))
channel_input = Input(shape=(1,))

video_embedding = Embedding(num_videos, embedding_dim, input_length=1)(video_input)
channel_embedding = Embedding(num_channels, embedding_dim, input_length=1)(channel_input)

dot_product = Dot(axes=2)([video_embedding, channel_embedding])
dot_product = Flatten()(dot_product)

dense1 = Dense(128, activation='relu')(dot_product)
output = Dense(train_tags_encoded.shape[1], activation='softmax')(dense1)

model = Model(inputs=[video_input, channel_input], outputs=output)

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.summary()

train_data, val_data = train_test_split(train_data, test_size=0.2, random_state=42)

train_data['tags_str'] = train_data['tags'].apply(lambda x: ' '.join(x))
val_data['tags_str'] = val_data['tags'].apply(lambda x: ' '.join(x))

history = model.fit(
    [train_data['video_id'], train_data['channelId']], 
    train_tags_encoded.toarray(), 
    epochs=20,
    batch_size=64,
    validation_data=(
        [val_data['video_id'], val_data['channelId']],
        val_tags_encoded.toarray() 
    )
)

loss, accuracy = model.evaluate(
    [test_data['video_id'], test_data['channelId']],
    test_tags_encoded.toarray()
)
print(f"Test Loss: {loss}, Test Accuracy: {accuracy}")