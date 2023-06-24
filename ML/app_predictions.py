import pickle
import pandas as pd
import numpy as np


def get_prediction(prediction_data_dict: dict):
    with open('ML/models/harvest_pred_model', 'rb') as f:
        model_lgbm = pickle.load(f)

    np.random.seed(0)
    # Create a DataFrame with the desired structure
    data = pd.DataFrame(prediction_data_dict)

    data['fenophase'] = data['fenophase'].astype('category')

    # Drop the 'number_of_cars' column from the new data
    features = data

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

    with open('prediction_dict', 'rb') as f:
        prediction_dict = pickle.load(f)

  
    # print(get_prediction(prediction_dict))
