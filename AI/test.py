import torch
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Carregar o modelo treinado específico para o Brasil
model_path = "models/model_BR.pth"
model = YourModelClass()  # Substitua YourModelClass pelo nome da sua classe de modelo
model.load_state_dict(torch.load(model_path))
model.eval()

# Carregar os dados de teste
test_data = pd.read_csv("test_data_BR.csv")  # Substitua "test_data_BR.csv" pelo caminho do seu arquivo de dados de teste

# Codificar as tags usando o mesmo LabelEncoder usado durante o treinamento
label_encoder = LabelEncoder()
label_encoder.classes_ = torch.load("label_encoder_BR.pkl")  # Carregar o LabelEncoder específico para o Brasil

# Pré-processar os dados de teste
X_test = test_data[['view_count', 'likes', 'dislikes', 'comment_count']].values
X_test_tensor = torch.tensor(X_test, dtype=torch.float32)

# Fazer previsões
with torch.no_grad():
    outputs = model(X_test_tensor)
    _, predicted_labels = torch.max(outputs, 1)

# Converter os valores previstos de volta para as tags originais
predicted_tags = label_encoder.inverse_transform(predicted_labels)

# Imprimir ou salvar as previsões
print(predicted_tags)
