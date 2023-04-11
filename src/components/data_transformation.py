import os
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
import pandas as pd
import sys
import numpy as np
from src.utils import save_object

@dataclass
class TransformationConfig:
    transformer_path=os.path.join('artifacts','transformer.pkl')
class DataTransformer:
    def __init__(self):
        self.transformer_path=TransformationConfig()
    def get_transform_object(self):
        logging.info("Data Transformation object fetch initiated")
        try:
            #Categorical Feature Encoding
            # Define the custom ranking for each ordinal variable
            cut_categories = ['Fair', 'Good', 'Very Good','Premium','Ideal']
            color_categories = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
            clarity_categories = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']
            categorical_cols = ['cut', 'color','clarity']
            numerical_cols = ['carat', 'depth','table', 'x', 'y', 'z']
            num_pipeline=Pipeline( 
                steps=[  
                ('imputer',SimpleImputer(strategy='median')),
                ('scaler',StandardScaler())
                ]
            )
            cat_pipeline=Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='most_frequent')),
                ('ordinal_encoder',OrdinalEncoder(categories=[cut_categories,color_categories,clarity_categories])),
                ('scaler',StandardScaler())
                ]
            )
            preprocessor=ColumnTransformer([
                ('num_pipeline',num_pipeline,numerical_cols),
                ('cat_pipeline',cat_pipeline,categorical_cols)
                ],verbose_feature_names_out=True)  
            return preprocessor
        except Exception as e:
            logging.info("Exception occured at Data Transformation step")
            raise CustomException(e,sys)
    def initiate_data_transformation(self,train_data_path,test_data_path):
        logging.info("Data Transformation initiated")
        try:
            train_data=pd.read_csv(train_data_path)
            test_data=pd.read_csv(test_data_path)
            X_train=train_data.drop('price',axis=1)
            y_train=train_data['price']

            X_test=test_data.drop('price',axis=1)
            y_test=test_data['price']

            preprocessor=self.get_transform_object()
            logging.info("Applying preprocessing")
            X_train_arr=preprocessor.fit_transform(X_train)
            X_test_arr=preprocessor.transform(X_test)
            train_arr=np.c_[X_train_arr,np.array(y_train)]
            test_arr=np.c_[X_test_arr,np.array(y_test)]

            save_object(file_path=self.transformer_path.transformer_path,obj=preprocessor)
            logging.info("Pickle file saved successfully")

            return train_arr,test_arr,self.transformer_path
        except Exception as e:
            logging.info("Exception occured at data transformation")
            raise CustomException(e,sys)
        
