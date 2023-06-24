import pandas as pd
import numpy as np
import pickle
import lightgbm as lgb
from tqdm import tqdm


def generate_model(train_path: str = 'training_data.csv'):
    df = pd.read_csv(f'trains/{train_path}')
  
    df['fenophase'] = df['fenophase'].astype('category')
    X= df.drop(columns = 'output')
    y = df['output']

    model_lgbm = lgb.LGBMRegressor()  
    model_lgbm.fit(X, y)

    with open('models/harvest_pred_model', 'wb') as f:
        pickle.dump(model_lgbm, f)


if __name__ == '__main__':
    generate_model()


    