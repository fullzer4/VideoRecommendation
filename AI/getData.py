import os
from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()

dataset_name = 'rsrishav/youtube-trending-video-dataset'

dest_dir = 'data/'

os.makedirs(dest_dir, exist_ok=True)

api.dataset_download_files(dataset_name, path=dest_dir, unzip=True)
print("Dataset saved in ", dest_dir)
