import os
import pickle
from src.exception import CustomException
import sys
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
import numpy as np
import pandas as pd
from src.logger import logging
from src.exception import CustomException
import sys

def save_object(file_path,obj): 
     try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
     except Exception as e:
        raise CustomException(e, sys)
     
def train_evaluate_model(models_dict,train_arr,test_arr):
    X_train,X_test,y_train,y_test=train_arr[:,:-1],test_arr[:,:-1],train_arr[:,-1],test_arr[:,-1]
    metrics=['r2 score','Root Mean Squared Error','Mean Absolute Error']
    cols=pd.MultiIndex.from_product([['Training Dataset','Test Dataset'],metrics])
    report=pd.DataFrame(index=models_dict.keys(),columns=cols)
    try:
      logging.info("Model Training Started")
      for model in models_dict:
         trainer=models_dict[model]
         trainer.fit(X_train,y_train)
        
         y_pred_train=trainer.predict(X_train)
         y_pred_test=trainer.predict(X_test)

         mse_train=mean_squared_error(y_train,y_pred_train)
         mse_test=mean_squared_error(y_test,y_pred_test)

         mae_train=mean_absolute_error(y_train,y_pred_train)
         mae_test=mean_absolute_error(y_test,y_pred_test)

         report.loc[model,('Training Dataset','Mean Absolute Error')]=mae_train
         report.loc[model,('Test Dataset','Mean Absolute Error')]=mae_test

         rmse_train=np.sqrt(mse_train)
         rmse_test=np.sqrt(mse_test)

         report.loc[model,('Training Dataset','Root Mean Squared Error')]=rmse_train
         report.loc[model,('Test Dataset','Root Mean Squared Error')]=rmse_test

         r2_score_train=r2_score(y_train,y_pred_train)
         r2_score_test=r2_score(y_test,y_pred_test)

         report.loc[model,('Training Dataset','r2 score')]=r2_score_train
         report.loc[model,('Test Dataset','r2 score')]=r2_score_test
    
      return report
    except Exception as e:
       logging.info("Error occured while training the model")
       raise CustomException(e,sys)      

# def style_df(df):
#      styles = [
#         {'selector': 'th',
#          'props': [('border', '1px solid black'),
#                    ('background-color', 'lightgrey'),
#                    ('text-align', 'center'),
#                    ('padding', '5px')]},
#         {'selector': 'td',
#          'props': [('border', '1px solid black'),
#                    ('padding', '5px')]}
#     ]
#      return df.style.format('{:.2f}').set_table_styles(styles)

        

        