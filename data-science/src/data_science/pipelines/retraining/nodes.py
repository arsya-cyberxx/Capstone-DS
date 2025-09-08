"""
This is a boilerplate pipeline 'retraining'
generated using Kedro 1.0.0
"""
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

def model_selection(knn_model, lr_model, svm_model, dt_model):
    accuracies = {knn_model['accuracy'] : 'KNN', 
                  lr_model['accuracy'] : 'LR', 
                  svm_model['accuracy'] : 'SVM', 
                  dt_model['accuracy'] : 'DT'}
    
    params = {'KNN': knn_model['params'], 
              'LR': lr_model['params'], 
              'SVM': svm_model['params'], 
              'DT': dt_model['params']}
    
    best_model = max(accuracies.keys())
    best_model_name = accuracies[best_model]
    best_model_params = params[best_model_name]

    return {"best_model_name": best_model_name, "best_model_params": best_model_params}

def retraining_best_model():