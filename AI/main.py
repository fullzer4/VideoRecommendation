import os
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.metrics import recall_score

datasets = [
    "BR_youtube_trending_data.csv",
    "CA_youtube_trending_data.csv",
    "DE_youtube_trending_data.csv",
    "FR_youtube_trending_data.csv",
    "GB_youtube_trending_data.csv",
    "IN_youtube_trending_data.csv",
    "JP_youtube_trending_data.csv",
    "KR_youtube_trending_data.csv",
    "MX_youtube_trending_data.csv",
    "RU_youtube_trending_data.csv",
    "US_youtube_trending_data.csv"
]

for dataset in datasets:
    data = pd.read_csv(os.path.join("./data", dataset))
    
    recalls = []
    f1_scores = []

    label_encoder = LabelEncoder()
    data['tag_encoded'] = label_encoder.fit_transform(data['tags'])

    X = data[['view_count', 'likes', 'dislikes', 'comment_count']].values
    y = data['tag_encoded'].values

    X_tensor = torch.tensor(X, dtype=torch.float32)
    y_tensor = torch.tensor(y, dtype=torch.long)

    num_folds = 5
    kfold = KFold(n_splits=num_folds, shuffle=True, random_state=42)

    class VideoRecommendationModel(nn.Module):
        def __init__(self, input_size, output_size):
            super(VideoRecommendationModel, self).__init__()
            self.fc1 = nn.Linear(input_size, 64)
            self.dropout1 = nn.Dropout(0.2)  
            self.fc2 = nn.Linear(64, 32)
            self.dropout2 = nn.Dropout(0.2)  
            self.fc3 = nn.Linear(32, output_size)
            self.relu = nn.ReLU()

        def forward(self, x):
            x = self.relu(self.fc1(x))
            x = self.dropout1(x)
            x = self.relu(self.fc2(x))
            x = self.dropout2(x)
            x = self.fc3(x)
            return x

    criterion = nn.CrossEntropyLoss()

    train_losses = []
    test_losses = []

    for fold, (train_idx, test_idx) in enumerate(kfold.split(X)):
        print(f'Fold [{fold+1}/{num_folds}]')

        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
        y_train_tensor = torch.tensor(y_train, dtype=torch.long)

        X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
        y_test_tensor = torch.tensor(y_test, dtype=torch.long)

        input_size = X_train.shape[1]
        output_size = len(label_encoder.classes_)
        model = VideoRecommendationModel(input_size, output_size)

        optimizer = optim.Adam(model.parameters(), lr=0.001)

        num_epochs = 50
        batch_size = 2048
        for epoch in range(num_epochs):
            model.train()
            epoch_loss = 0
            for idx in range(0, len(X_train_tensor), batch_size):
                optimizer.zero_grad()
                batch_X = X_train_tensor[idx:idx+batch_size]
                batch_y = y_train_tensor[idx:idx+batch_size]
                outputs = model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item()

        model.eval()
        test_loss = 0
        with torch.no_grad():
            outputs = model(X_test_tensor)
            test_loss = criterion(outputs, y_test_tensor)
    
            _, predicted_labels = torch.max(outputs, 1)

            recall = recall_score(y_test, predicted_labels, average='macro')
            
            recalls.append(recall)
        
        print(f'Test Loss: {test_loss.item()}')
        print(f'Recall: {recall}')
        
        train_losses.append(epoch_loss)
        test_losses.append(test_loss.item())
    
        predicted_tags = label_encoder.inverse_transform(predicted_labels)

        country_code = dataset[:2]
        model_path = os.path.join("models", f"model_{country_code}.pth")
        torch.save(model.state_dict(), model_path)
    
    print('Average Train Loss:', sum(train_losses) / num_folds)
    print('Average Test Loss:', sum(test_losses) / num_folds)
    print('Average Recall:', np.mean(recalls))
    print('Average F1-score:', np.mean(f1_scores))
