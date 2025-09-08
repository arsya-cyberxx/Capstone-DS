"""
This is a boilerplate pipeline 'modelling'
generated using Kedro 1.0.0
"""

from kedro.pipeline import Node, Pipeline, node  # noqa
from .nodes import (data_preparation, logistic_regression_model, 
                    svm_model, decision_tree_model, knn_model)

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=data_preparation,
            inputs=["feature_engineered_data", "labeled_data"],
            outputs=["X_train", "X_test", "Y_train", "Y_test"],
            name="data_preparation",
            tags=["data_preparation"]
        ),
        node(
            func=logistic_regression_model,
            inputs=["X_train", "X_test", "Y_train", "Y_test"],
            outputs="LR_model",
            name="logistic_regression_training",
            tags=["logistic_regression_training"]
        ),
        node(
            func=svm_model,
            inputs=["X_train", "X_test", "Y_train", "Y_test"],
            outputs="SVM_model",
            name="SVM_training",
            tags=["SVM_training"]
        ),
        node(
            func=decision_tree_model,
            inputs=["X_train", "X_test", "Y_train", "Y_test"],
            outputs="DT_model",
            name="DT_training",
            tags=["DT_training"]
        ),
        node(
            func=knn_model,
            inputs=["X_train", "X_test", "Y_train", "Y_test"],
            outputs="KNN_model",
            name="KNN_training",
            tags=["KNN_training"]
        ),
    ])
