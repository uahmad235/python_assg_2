import uvicorn
from fastapi import FastAPI

app = FastAPI()


# TODO: train regressor, get a prediction with data and return the result
@app.post('/predict')
async def get_prediction(data: dict[str, float]) -> float:
    prediction = 35.5
    return prediction


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)
