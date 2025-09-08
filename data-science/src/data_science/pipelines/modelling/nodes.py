"""
This is a boilerplate pipeline 'modelling'
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

def data_preparation(feature_engineered_data: pd.DataFrame, labeled_data: pd.DataFrame) -> tuple:
    """
    Data preparation function
    """
    Y = labeled_data['Class'].to_numpy()
    
    transform = preprocessing.StandardScaler()
    X = transform.fit_transform(feature_engineered_data)

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)
    return X_train, X_test, Y_train, Y_test

def logistic_regression_model(X_train: np.ndarray, X_test: np.ndarray, Y_train: np.ndarray, Y_test: np.ndarray) -> dict:
    """
    Logistic Regression model
    """
    # define hyperparameters to tune 
    parameters_lr ={"C":[0.01,0.1,1],
                'penalty':['l2'], 
                'solver':['lbfgs']}# l1 lasso l2 ridge

    # define the model
    lr = LogisticRegression(random_state = 12345)

    # define the grid search object
    grid_search_lr = GridSearchCV(
        estimator = lr,
        param_grid = parameters_lr,
        scoring = 'accuracy',
        cv = 10
    )
    # execute search
    logreg_cv = grid_search_lr.fit(X_train,Y_train)
    accuracy = logreg_cv.score(X_test, Y_test)
    return {"accuracy": accuracy, "parameters": logreg_cv.best_params_}

def svm_model(X_train: np.ndarray, X_test: np.ndarray, Y_train: np.ndarray, Y_test: np.ndarray) -> dict:
    # define hyperparameters to tune 
    parameters_svm = {'kernel':('linear', 'rbf','poly','rbf', 'sigmoid'),
                'C': np.logspace(-3, 3, 5),
                'gamma':np.logspace(-3, 3, 5)}

    # define the model
    svm = SVC(random_state = 12345)

    # define the grid search object
    grid_search_svm = GridSearchCV(
        estimator = svm,
        param_grid = parameters_svm,
        scoring = 'accuracy',
        cv = 10
    )
    # execute search
    svm_cv = grid_search_svm.fit(X_train,Y_train)
    accuracy = svm_cv.score(X_test, Y_test)
    return {"accuracy": accuracy, "parameters": svm_cv.best_params_}

def decision_tree_model(X_train: np.ndarray, X_test: np.ndarray, Y_train: np.ndarray, Y_test: np.ndarray) -> dict:
    # define hyperparameters to tune 
    parameters_tree = {'criterion': ['gini', 'entropy'],
        'splitter': ['best', 'random'],
        'max_depth': [2*n for n in range(1,10)],
        'max_features': ['auto', 'sqrt'],
        'min_samples_leaf': [1, 2, 4],
        'min_samples_split': [2, 5, 10]}

    # define the model
    tree = DecisionTreeClassifier(random_state = 12345)

    # define the grid search object
    grid_search_tree = GridSearchCV(
        estimator = tree,
        param_grid = parameters_tree,
        scoring = 'accuracy',
        cv = 10
    )
    # execute search
    tree_cv = grid_search_tree.fit(X_train, Y_train)
    accuracy = tree_cv.score(X_test, Y_test)
    return {"accuracy": accuracy, "parameters": tree_cv.best_params_}

def knn_model(X_train: np.ndarray, X_test: np.ndarray, Y_train: np.ndarray, Y_test: np.ndarray) -> dict:
    # define hyperparameters to tune
    parameters_knn = {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
                'p': [1,2]}

    # define the model
    knn = KNeighborsClassifier()

    # define the grid search object
    grid_search_knn = GridSearchCV(
        estimator = knn,
        param_grid = parameters_knn,
        scoring = 'accuracy',
        cv = 10
    )
    # execute search
    knn_cv = grid_search_knn.fit(X_train, Y_train)
    accuracy = knn_cv.score(X_test, Y_test)
    return {"accuracy": accuracy, "parameters": knn_cv.best_params_}
