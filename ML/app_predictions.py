import pickle
import pandas as pd
import numpy as np


def get_prediction(prediction_list_of_dicts):
    with open('models/harvest_pred_model', 'rb') as f:
        model_lgbm = pickle.load(f)

    np.random.seed(0)
    # Create a DataFrame with the desired structure
    data = pd.DataFrame(prediction_list_of_dicts)

    

    data['fenophase'] = data['fenophase'].astype('category')

    # Drop the 'number_of_cars' column from the new data
    features = data.drop(columns='id')

    # Make predictions using your trained model
    predictions = model_lgbm.predict(features)
    # Add the predictions to the data DataFrame
    data['output'] = predictions
    data = data[['latitude', 'longitude', 'output']]
    data = data.to_dict(orient="records")
    # Display the generated dataset

    return data


if __name__ == '__main__':
    # Этот моковые данные со словарем входных данных
    #dict_=[{'humidity_4': 0, 'sugar_percent': 0, 'temperature_forecast_3': 0, 'rain_5': False, 'place': 1, 'humidity_5': 0, 'acid_percent': 0, 'temperature_forecast_4': 0, 'density': 0, 'temperature_1': 0, 'fenols_percent': 0, 'temperature_forecast_5': 0, 'id': 1, 'latitude': 44.54073, 'temperature_2': 0, 'alkans_percent': 0, 'longitude': 38.08294, 'temperature_3': 0, 'evi': 0.0, 'rain_1': False, 'humidity_1': 0, 'temperature_4': 0, 'previous_stage_success': 0.0, 'rain_2': False, 'humidity_2': 0, 'temperature_5': 0, 'temperature_forecast_1': 0, 'rain_3': False, 'humidity_3': 0, 'fenophase': '0', 'temperature_forecast_2': 0, 'rain_4': False}]
    with open('prediction_dict', 'rb') as f:
        prediction_dict = pickle.load(f)

    # print(prediction_dict)
    print(get_prediction(dict_))
