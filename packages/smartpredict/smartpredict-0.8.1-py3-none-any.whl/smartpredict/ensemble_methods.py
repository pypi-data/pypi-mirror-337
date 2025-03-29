# smartpredict/ensemble_methods.py
"""
Ensemble methods module for SmartPredict.
Provides functions to create ensemble models.
"""

import logging
from sklearn.ensemble import StackingClassifier, VotingClassifier, BaggingClassifier

def apply_ensembles(base_learners, meta_learner, n_jobs=-1):
    """
    Apply ensemble methods to combine base learners with a meta learner.

    Parameters:
    base_learners (list of tuples): List of base learner models.
    meta_learner (estimator): The meta learner model.
    n_jobs (int): Number of jobs to run in parallel.

    Returns:
    tuple: (stacking_model, voting_model, bagging_model) ensemble models
    """
    try:
        stacking_model = StackingClassifier(estimators=base_learners, final_estimator=meta_learner, n_jobs=n_jobs)
        voting_model = VotingClassifier(estimators=base_learners, n_jobs=n_jobs)
        bagging_model = BaggingClassifier(base_estimator=meta_learner, n_jobs=n_jobs)
        return stacking_model, voting_model, bagging_model
    except Exception as e:
        logging.error(f"Ensemble method application failed: {e}")
        return None, None, None