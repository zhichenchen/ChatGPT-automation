import json
import time

import pandas as pd
import requests
from tqdm import tqdm

# data = pd.read_csv('merged.csv',header=0).values
data = pd.read_csv('merged.csv',header=0).values
url = "https://openai-openai-detector.hf.space/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

all_result = []
for d in tqdm(data):
    try:
        text = d[1]
        result  = requests.get(f'{url}?{text}',headers=headers)
        result = json.loads(result.text)
        real_probability=result['real_probability']
        fake_probability=result['fake_probability']
        all_result.append([d[0],text,real_probability,fake_probability])
        time.sleep(0)
    except Exception as e:
        print(e)
    #if len(all_result)>10:
    #    break

data_frame = pd.DataFrame(
    columns=['PostId', 'Text', 'real', 'fake'],
    data=all_result)
data_frame.to_csv('resulted.csv')