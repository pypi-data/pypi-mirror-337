# smartpredict/hyperparameter_tuning.py
"""
Hyperparameter tuning module for SmartPredict.
Provides functions to perform hyperparameter optimization.
"""

import logging
import optuna
from sklearn.model_selection import cross_val_score

def tune_hyperparameters(model, param_distributions, X_train, y_train, n_trials=100):
    """
    Tune hyperparameters for a machine learning model using Optuna.
    
    Parameters:
    model (estimator): The machine learning model to tune.
    param_distributions (dict): Dictionary with parameters names as keys and distributions as values.
                               For example: {'n_estimators': [10, 50, 100], 'max_depth': [1, 5, 10]}
    X_train (array-like): Training features.
    y_train (array-like): Training labels.
    n_trials (int): Number of trials for optimization.
    
    Returns:
    estimator: Tuned model with best parameters.
    """
    try:
        def objective(trial):
            params = {}
            for param_name, param_values in param_distributions.items():
                if isinstance(param_values, list):
                    if all(isinstance(val, int) for val in param_values):
                        # Integer parameter
                        params[param_name] = trial.suggest_int(param_name, min(param_values), max(param_values))
                    elif all(isinstance(val, float) for val in param_values):
                        # Float parameter
                        params[param_name] = trial.suggest_float(param_name, min(param_values), max(param_values))
                    else:
                        # Categorical parameter
                        params[param_name] = trial.suggest_categorical(param_name, param_values)
                elif isinstance(param_values, tuple) and len(param_values) == 2:
                    # Range (min, max)
                    if all(isinstance(val, int) for val in param_values):
                        params[param_name] = trial.suggest_int(param_name, param_values[0], param_values[1])
                    else:
                        params[param_name] = trial.suggest_float(param_name, param_values[0], param_values[1])
            
            model.set_params(**params)
            score = cross_val_score(model, X_train, y_train, cv=5).mean()
            return score
        
        study = optuna.create_study(direction='maximize')
        study.optimize(objective, n_trials=n_trials)
        best_params = study.best_params
        model.set_params(**best_params)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        logging.error(f"Hyperparameter tuning failed: {e}")
        # Fall back to default model if tuning fails
        model.fit(X_train, y_train)
        return model