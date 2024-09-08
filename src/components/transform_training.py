import os
import sys
import pandas as pd
import numpy as np
import pickle

from dataclasses import dataclass
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

from sklearn.linear_model import LinearRegression, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import r2_score
from catboost import CatBoostRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_model



@dataclass
class DataTransformationConfig:
    final_pipeline = os.path.join('data', 'final_model_pipeline.pkl')
    

class ModelDevelopment:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        

    def transform_train(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Read train and test data completed")
            
            # Preprocessor for Encoding and Standardize the data
            numerical_features = ['carat', 'depth', 'table', 'x', 'y', 'z']
            categorical_features = ['cut', 'color', 'clarity']
            target_column = 'price'
            
            numeric_transformer = StandardScaler()
            oh_transformer = OneHotEncoder(drop='first')

            preprocessor = ColumnTransformer(
                [
                    ("OneHotEncoder", oh_transformer, categorical_features),
                    ("StandardScaler", numeric_transformer, numerical_features),
                ]
            )

            
            ## Input and Target for data train
            train_input_feature = train_df.drop(columns=[target_column], axis=1)
            train_target_feature = train_df[target_column]
            
            ## Input and Target for data test
            test_input_feature = test_df.drop(columns=[target_column], axis=1)
            test_target_feature = test_df[target_column]
            
            # apply the transform into the input feature 
            logging.info("Applying Preprocessing object on training and testing data")
            
            
            # Dictionaries of the Model
            models = {
                "Linear Regression": {
                    "model": LinearRegression(),
                    "params": {
                        "model__fit_intercept": [True, False]
                    }
                 },
                 "Lasso": {
                     "model": Lasso(),
                     "params": {
                         "model__alpha": [0.1, 1.0, 10.0]
                     }
                 },
                 "K-Neighbors Regressor": {
                     "model": KNeighborsRegressor(),
                     "params": {
                         "model__n_neighbors": [3, 5, 7]
                     }
                 },
                 "Random Forest Regressor": {
                     "model": RandomForestRegressor(),
                     "params": {
                         "model__n_estimators": [50, 100],
                         "model__max_depth": [None, 5, 10],
                         "model__max_features": ["auto", 5, 7, 8],
                     }
                 },
                 "XGBRegressor": {
                     "model": XGBRegressor(),
                     "params": {
                         "model__n_estimators": [50, 100],
                         "model__learning_rate": [0.01, 0.1, 0.3]
                     }
                 },
                 "CatBoost": {
                     "model": CatBoostRegressor(verbose=False),
                     "params": {
                         "model__depth": [6, 8],
                         "model__learning_rate": [0.01, 0.1],
                         "model__iterations": [100, 200]
                     }
                }
            }
            
            X_train, y_train, X_test, y_test = (
                train_input_feature,
                train_target_feature,
                test_input_feature,
                test_target_feature
            )            
            
            # Run the models
            for model_name, model_dict in models.items():
                model = model_dict['model']
                param_grid = model_dict['params']

                # Create pipeline
                pipeline = Pipeline(steps=[
                    ('preprocessor', preprocessor),  # Add your ColumnTransformer here for preprocessing
                    ('model', model)
                ])
                
                # Setup GridSearchCV
                grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='r2', n_jobs=-1)

                # Fit model
                grid_search.fit(X_train, y_train)

                # Get the best model
                best_model = grid_search.best_estimator_
                
                # Evaluate on training set
                y_train_pred = best_model.predict(X_train)
                train_mae, train_rmse, train_r2 = evaluate_model(y_train, y_train_pred)

                # Evaluate on test set
                y_test_pred = best_model.predict(X_test)
                test_mae, test_rmse, test_r2 = evaluate_model(y_test, y_test_pred)

                # Print results
                print(f"{model_name} Best Hyperparameters: {grid_search.best_params_}")
                print(f"Training set performance:\n - MAE: {train_mae:.4f}\n - RMSE: {train_rmse:.4f}\n - R2: {train_r2:.4f}")
                print(f"Test set performance:\n - MAE: {test_mae:.4f}\n - RMSE: {test_rmse:.4f}\n - R2: {test_r2:.4f}")
                print('=' * 50)
                
            # Save the model
            # Based on Best Hyperparameter
            final_pipeline = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('model', XGBRegressor(learning_rate=0.3, n_estimators=100))  # Best hyperparameters
            ])
            
            
            save_object(
                file_path=self.data_transformation_config.final_pipeline,
                obj=final_pipeline.fit(X_train, y_train)
            )
            
            
        except Exception as e:
            raise CustomException(e, sys)