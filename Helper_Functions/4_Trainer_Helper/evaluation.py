from typing import Dict

import numpy as np
import pandas as pd
from sklearn.metrics import log_loss, roc_auc_score, mean_squared_error, mean_absolute_error, r2_score, 
from sklearn.metrics import precision_score, recall_score, f1_score


def evaluate(y: pd.Series,
             w: pd.Series,
             y_pred: pd.Series) -> Dict[str, any]:
    """calculate evaluation metrics for classification"""
    metrics = {'records': str(len(y)), 'weights': str(sum(w))}
    y_actual_ungroup = np.repeat(y, w)
    y_predict_upgroup = np.repeat(y_pred, w)
    metrics['log_loss'] = log_loss(y_actual_ungroup, y_predict_upgroup)
    metrics['roc_auc_score'] = roc_auc_score(y_actual_ungroup, y_predict_upgroup)

    metrics['precision_score'] = precision_score(y_actual_ungroup, y_predict_upgroup)
    metrics['recall_score'] =recall_score(y_actual_ungroup, y_predict_upgroup)
    metrics['f1_score'] = f1_score(y_actual_ungroup, y_predict_upgroup)
    metrics['roc_auc_score'] = roc_auc_score(y_actual_ungroup, y_predict_upgroup)
    return metrics


def evaluate_timeseries(y: pd.Series,
             y_pred: pd.Series) -> Dict[str, any]:
    """calculate evaluation metrics for time series prediction"""
    metrics = {'records': str(len(y))}
    metrics['mse'] = mean_squared_error(y, y_pred)
    metrics['mae'] = mean_absolute_error(y, y_pred)
    metrics['r2'] = r2_score(y, y_pred)
    return metrics

