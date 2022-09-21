# %%
#import modules
import pandas as pd
from xgboost import XGBRegressor
import sklearn

import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)



#load data 
energy_data = pd.read_csv("recs2015_public_v4.csv", index_col = "DOEID")
energy_data.head()

#add new column to dataset based on US national energy prices as of July 2022.
def price_convertor(row):
    """calculates yearly energy cost in dollars"""
    current_cost = row * 0.166 #multiplies kilowatthours used between 01/01/2015-31/12/2015 by US energy prices in July 2022
    return current_cost

energy_data["2022_price"] = energy_data["KWH"].apply(price_convertor)




# %%
from sklearn.model_selection import train_test_split
#check if any rows are missing target data. Other columns assessed later to avoid data leakage.  
missing_target = energy_data["KWH"].isnull().sum()
print(missing_target) #no issue -> therefore no need to remove any 

#seperate target data column from dataset
y = energy_data["KWH"]


#break off predictor columns of interest
X = energy_data.loc[:,"REGIONC":"TOTSQFT_EN"] #selects all possible predictor columns 
print(X)



# %%

#check if any columns contain characters
s = (X.dtypes == "object")
object_cols = list(s[s].index)
print(object_cols) 


# # %%
# """
# Found 4 columns contain characters. These columns will be one-hot encoded to convert them into a number. 

# Note that dataset had already been imputed, therefore this step was skipped. 
# """

# # %%
# #preprocessing for categorical data
# categorical_transformer = sklearn.pipeline.Pipeline(steps = [
#     ("imputer", sklearn.impute.SimpleImputer(strategy = "most_frequent")),
#     ("onehot", sklearn.preprocessing.OneHotEncoder(handle_unknown="ignore"))])



# # %%
# """
# # Original Model 
# Uses full set of variables to predict energy usage
# """

# # %%
# from sklearn.model_selection import cross_val_score



# #create values to alternate through to check for best parameters
# N_VALUES = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
# LEARNING_VALUES = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

# #create dictionary to assign results to 
# model_dict = {}
# replace = []
# #create function for comparing lots of models

# def get_score(n_value, learning_value):

#     model = XGBRegressor(n_estimators = n_value, early_stopping_rounds = 5, learning_rate = learning_value, n_jobs = 4)

#     #create pipeline 
#     my_pipeline = sklearn.pipeline.Pipeline(steps =[
#         ("categorical_transformer", categorical_transformer),
#         ("model", model)
#     ])

#     #assess model using cross-validation
#     scores = -1* cross_val_score(my_pipeline, X, y, cv = 5, scoring = "neg_mean_absolute_error")

#     return(scores.mean())

# for n_value in N_VALUES:
#     for learning_value in LEARNING_VALUES: 
#         score = get_score(n_value, learning_value)



    








