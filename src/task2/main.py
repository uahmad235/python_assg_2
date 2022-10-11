from mongo.mongo_client import MongoDBClient
import requests

MONGO_CLIENT = MongoDBClient('clients')
ML_MODEL_URL = 'http://ml_model:8080/predict'


def start_session() -> None:
    result = MONGO_CLIENT.db.sessions.find_one({
        'session_id': 'b3aebc80-ff28-4569-bd18-2ace692f668e',
    })

    query_params = {
        'dropped_frames': result['dropped_frames'],
        'FPS': result['FPS']
    }
    print(query_params)

    prediction = requests.post(ML_MODEL_URL, json=query_params)
    print(f'Prediction: {prediction.text}')

    input('Enter the next command:')


if __name__ == '__main__':
    start_session()
