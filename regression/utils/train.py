from utils.features import process
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.metrics import mean_squared_error
import numpy as np
import os
import pickle
import json
import pandas as pd

def train(feature,
          model,
          dataset_path,
          dataset_reader, run_id):

    # Step 1: Get dataset.
    mol_strings, properties, folds = dataset_reader.read(dataset_path)
    Xs, Ys = process(feature, mol_strings, properties)
    
    outlier_indices = []

    trues = []
    preds = []

    for i in range(5):  # Assuming 5 folds
        train_indices = [j for j, fold in enumerate(folds[i]) if fold == 'train']
        test_indices = [j for j, fold in enumerate(folds[i]) if fold == 'val']
        
        Xs_train, Xs_test = Xs[train_indices], Xs[test_indices]
        Ys_train, Ys_test = Ys[train_indices], Ys[test_indices]
        
        # Learn.
        model.fit(Xs_train, Ys_train)

        # Test
        Ys_test_pred = model.predict(Xs_test)
        error = mean_squared_error(Ys_test, Ys_test_pred)
        
        outlier_indices.extend([idx for idx, pred in enumerate(Ys_test_pred.tolist()) if pred < -200])

        trues.extend(Ys_test.tolist())
        preds.extend(Ys_test_pred.tolist())

        print(f'Mean Squared Error for fold {i} = {error}')
        
        os.makedirs(f'models/{run_id}/fold_{i}', exist_ok=True)
        # Save model
        with open(f'models/{run_id}/fold_{i}/model.pkl', 'wb') as f:
            pickle.dump(model, f)
        
        # Save metrics and predictions
        results = {
            'mse': error,
            'predictions': Ys_test_pred.tolist(),
            'true_values': Ys_test.tolist()
        }
        with open(f'models/{run_id}/fold_{i}/results.json', 'w') as f:
            json.dump(results, f)
    
    outlier_trues = [trues[idx] for idx in outlier_indices]
    print(outlier_trues)
    return trues, preds