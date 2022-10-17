import uvicorn
from fastapi import FastAPI
import _pickle as cPickle
import pandas as pd

app = FastAPI()

with open('classifier.pkl', 'rb') as f:
    classifier = cPickle.load(f)


@app.post('/predict')
async def get_prediction(data: dict) -> list:
    features_df = pd.DataFrame(data)
    prediction = classifier.predict(features_df)
    return [bool(el) for el in prediction]


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)
