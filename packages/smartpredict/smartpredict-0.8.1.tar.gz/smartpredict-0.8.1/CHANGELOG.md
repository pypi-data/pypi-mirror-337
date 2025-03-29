# Changelog

## [0.8.1] - 2025-03-29
### Fixed
- Added missing logging import in feature_engineering.py
- Fixed function naming discrepancy in ensemble_methods.py
- Added missing logging import in ensemble_methods.py
- Enhanced hyperparameter_tuning.py to properly use the param_distributions parameter

## [0.8.0] - 2025-01-20
### Updated
- Updated setup.py for PyPI deployment

## [0.7.4] - 2024-05-24
### Added
- KernelExplainer in place of Explainer
- Added .shape_values in place of .values

## [0.6.13] - 2024-05-23
### Added
- Added comprehensive model assessment metrics to evaluate machine learning models.
  - Accuracy
  - Precision
  - Recall
  - F1 Score
  - Confusion Matrix
  - ROC AUC
  - Classification Report

## [0.6.12] - 2024-05-23
### Updated
- Updated Github release.

## [0.6.11] - 2024-05-23
### Updated
- Updated dependencies to latest versions:
  - scikit-learn
  - numpy
  - pandas
  - shap
  - optuna
  - xgboost
  - lightgbm
  - catboost
  - tensorflow
  - torch

## [0.6.10] - 2024-05-22
### Added
- Initial release of SmartPredict.

## [0.6.0] - 2024-05-01
### Added
- Core functionalities for model training, evaluation, and selection.
- Support for scikit-learn, numpy, pandas, shap, optuna, xgboost, lightgbm, catboost, tensorflow, and torch.