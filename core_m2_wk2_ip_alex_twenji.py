# -*- coding: utf-8 -*-
"""Core_M2_Wk2_IP_Alex_Twenji.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sd9jjzuD4hyizEg76dxT4EihMxNw42qW

# DEFINING THE QUESTION

## a) Specifying the Question

As a Data Scientist, you work for Hass Consulting Company which is a real estate leader with over 25 years of experience. You have been tasked to study the factors that affect housing prices using the given information on real estate properties that was collected over the past few months. Later onwards, create a model that would allow the company to accurately predict the sale of prices upon being provided with the predictor variables. 

---

## b) Defining the Metric for Success

Being able to accurately predict house prices

---

## c) Understanding the context

Housing Prices differ depending on Location, Property Type and Square Footage of houses among other things. For a Real Estate Company, it would be good to know how to determine which properties do well in a market depending on the factors that affect these prices. This will enable them to price their properties at appropriate prices and could help them know how the value of the properties could appreciate in the future. Consumers would also be able to access this information if they wanted to.

---

## d) Experimental Design

1. Read and explore the given dataset.
2. Find and deal with outliers, anomalies, and missing data within the dataset.
3. Perform univariate and bivariate analysis recording your observations.
4. Perform Exploratory Data Analysis.
5. Performing regression analysis.
6. Provide a recommendation based on your analysis. 
7. Challenge your solution by providing insights on how you can make improvements in model improvement.  

---

# DATA PREPARATION
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp

# %matplotlib inline

house = pd.read_csv('/content/Independent Project Week 7 - house_data.csv')
house.head()

house.shape

house.info()

"""From the information given in the IP documentation, the column name definitions are:

Id 

price  - Price of the house

bedrooms - Number of Bedrooms

bathrooms - Number of Bathrooms

sqft_living - Square feet area of living area

sqft_lot  - Square feet area of parking Layout

floors - Number of Floors

waterfront - Whether waterfront is there or not

view - Number of Views

grade - Grades

sqft_above

sqft_basement - Square feet area of basement

yr_built - Year the house is built

yr_renovated - Year the house is renovated

zipcode - zipcode of the house

lat : Latitude of the house

lon : Longitude of the house

sqft_living15

sqft_lot15

# DATA CLEANING
"""

house.head()

house.isna().sum()

house.duplicated().sum()

house[house.duplicated()]

# The records look ok, rather than duplicated records. We'll keep all of them.

house.drop(columns = ['id'], inplace = True)

house.head()

"""The Dataset is relatively clean, we've drop the ID column for the following sections.

# DATA ANALYSIS

## UNIVARIATE ANALYSIS
"""

house.info()

col_names = ['price','bedrooms', 'bathrooms', 'sqft_living','sqft_lot']

fig, ax = plt.subplots(len(col_names), figsize= (8,40))

for i, col_val in enumerate(col_names):
  sns.boxplot(y = house[col_val], ax= ax[i])
  ax[i].set_title('Box plot - {}'.format(col_val), fontsize= 10)
  ax[i].set_xlabel(col_val, fontsize= 8)
plt.show()

col_names = ['floors','waterfront', 'view', 'condition','grade']

fig, ax = plt.subplots(len(col_names), figsize= (8,40))

for i, col_val in enumerate(col_names):
  sns.boxplot(y = house[col_val], ax= ax[i])
  ax[i].set_title('Box plot - {}'.format(col_val), fontsize= 10)
  ax[i].set_xlabel(col_val, fontsize= 8)
plt.show()

col_names = ['sqft_above','sqft_basement', 'yr_built', 'yr_renovated','zipcode']

fig, ax = plt.subplots(len(col_names), figsize= (8,40))

for i, col_val in enumerate(col_names):
  sns.boxplot(y = house[col_val], ax= ax[i])
  ax[i].set_title('Box plot - {}'.format(col_val), fontsize= 10)
  ax[i].set_xlabel(col_val, fontsize= 8)
plt.show()

col_names = ['lat','long', 'sqft_living15', 'sqft_lot15']

fig, ax = plt.subplots(len(col_names), figsize= (8,40))

for i, col_val in enumerate(col_names):
  sns.boxplot(y = house[col_val], ax= ax[i])
  ax[i].set_title('Box plot - {}'.format(col_val), fontsize= 10)
  ax[i].set_xlabel(col_val, fontsize= 8)
plt.show()

''' col_names = house.columns
Q1 = []
Q3 = []
IQR = []
for i, col_val in enumerate(col_names):
  Q1_value = house[col_val].quantile(.25)
  Q3_value = house[col_val].quantile(.75)
  IQR_value = Q3_value - Q1_value
  Q1.append(Q1_value)
  Q3.append(Q3_value)
  IQR.append(IQR_value)

IQR ''' #This method is ok, but there's a shorter method below since alll columns are numerical.

Quantile_1 = house.quantile(.25)
Quantile_3 = house.quantile(.75)
IQR_values = Quantile_3 - Quantile_1

anomalies = ((house < Quantile_1 - 1.5* IQR_values) | (house > Quantile_3 + 1.5 * IQR_values)).sum()
anomalies

percent_anomalies = (anomalies.sum() / house.shape[0])*100
percent_anomalies

"""The outliers seem like reasonable data that cannot be removed as this would affect the analysis, since the rows involved are roughly 67% of the data. Furthermore, the sqft_living column seems to have the same pattern of data as sqft_living15 (the same can be seen in sqft_lot15 and sqft_lot). This could mean that they are highly correlated.

### Summary Statistics
"""

house.describe()

# Central Tendancies

# mean
col_names = house.columns

for i, col_val in enumerate(col_names):
  print('The mean of ' + str(col_val) + ' is ' + str(house[col_val].mean()))

# mean of longitudes is negative, showing that the areas under review are in the Western hemisphere of the globe
# They are on the westside of the Prime Meridian and the co-ordinates relate to the 'Americas'

# median

for i, col_val in enumerate(col_names):
  print('The median of ' + str(col_val) + ' is ' + str(house[col_val].median()))

# The median of the longitudes show that the continent being observed is the American continent.

# mode

for i, col_val in enumerate(col_names):
  print('The mode of ' + str(col_val) + ' is ' + str(house[col_val].mode()))

# The modes are unimodal showing that the data was gathered from the same population.

# range

for i, col_val in enumerate(col_names):
  print('The range of ' + str(col_val) + ' is ' + str(house[col_val].max()-house[col_val].min()))

# standard deviation

for i, col_val in enumerate(col_names):
  print('The standard deviation of ' + str(col_val) + ' is ' + str(house[col_val].std()))

# variables with higher range showcase higher standard deviation from the mean.

# variance

for i, col_val in enumerate(col_names):
  print('The variance of ' + str(col_val) + ' is ' + str(house[col_val].var()))

# As expected, variables with higher standard deviation, also have higher variance.

# skewness

for i, col_val in enumerate(col_names):
  print('The skewness of ' + str(col_val) + ' is ' + str(house[col_val].skew()))
  
# Only year built and latitude have negative skewness

# kurtosis

for i, col_val in enumerate(col_names):
  print('The kurtosis of ' + str(col_val) + ' is ' + str(house[col_val].kurt()))

# Only floors, year built, zipcode and latitude have negative kurtosis

"""### Univariate Analysis Recommendation

Most of the skewness of the data is positive, indicating a mostly positively skewed dataset on most variables. This means that most distributions have longer tails to the right i.e. right-skewed / leptokurtic. Same goes for kurtosis as The data has mostly positive kurtosis indicating that most variables distributions have heavier tails and taller peaks than the normal distribution.

## BIVARIATE ANALYSIS
"""

house.info()

sns.pairplot(house, height=2)

# Thers's too many variables to see the pairplot properly, so lets use a heatmap.
plt.figure(figsize=(20,10))
sns.heatmap(house.corr(), annot= True)

"""### Bivariate Analysis Recommendation

As can be seen from the correlation heatmap, our target variable seems to have moderate to somewhat strong correlation with bathrooms, sqft_living, grade, sqft_above and sqft_living15, with all being above 0.5. These could be the variables that mostly affect the price of the house and will be investigated when designing our model and coming up with our predictions. Furthermore, as was discovered in the Univariate Analysis, it has been confirmed that the sqft_living and sqft_living15 are highly correlated (0.76) and sqft_lot and sqft_lot15 are also highly correlated(0.72)

## EXPLORATORY DATA ANALYSIS
"""

# In this section, we'll try discover some relationships between price and the columns we discovered to be moderately,
# to strongly correlated to it, i.e. bathrooms, sqft_living,grade,sqft_above and sqft_living15.

correlated = house[['price','bathrooms', 'sqft_living','grade','sqft_above', 'sqft_living15']]
sns.pairplot(correlated)

# From below we can see the positive linear correlation between the price and the said features.
# The features also have strong positive correlation with each other.

house['price'].hist(bins=100)

# Our target variable has been confirmed to be right tailed and not normally distributed.

fig, (ax1,ax2,ax3,ax4,ax5) = plt.subplots(5,1, figsize=(10, 10))
fig.suptitle('Price Relationships with variables')
sns.regplot(house.price, house.bathrooms, ax=ax1)
sns.regplot(house.price, house.sqft_living, ax=ax2)
sns.regplot(house.price, house.grade, ax=ax3)
sns.regplot(house.price, house.sqft_above, ax=ax4)
sns.regplot(house.price, house.sqft_living15, ax=ax5)

# The plots below show the positive linear relationship we had discovered.

"""# MODELING

## PREPARATION
"""

# Importing some of the libraries we might use

from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn import model_selection
from sklearn.model_selection import cross_validate
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.linear_model import ElasticNet


# Setting the warnings that may appear in our modelling off
import warnings
warnings.filterwarnings('ignore')

# Setting the pandas warning for chained assignments off, the default is usually on.
pd.options.mode.chained_assignment = None

# SPLITTING DATA INTO TEST AND TRAIN SETS INTO GLOBAL VARIABLES

X = house.drop(columns= ['price'])
y = house.price


X_train, X_test, y_train, y_test = train_test_split(X,y, test_size= 0.3, random_state= 10)

"""## MULTIPLE LINEAR REGRESSION

### Checking Multicolinearity
"""

house_correlation = house.corr()

# Let's use these correlations to compute the VIF score for each variable.

pd.DataFrame(np.linalg.inv(house_correlation.values), index = house_correlation.index, 
             columns=house_correlation.columns)

# VIF scores should start from 1 and anything beyond 5 shows high multicollinearity.
# sqft_living, sqft_above and sqft_basement have negative values, hence need to be removed from the test.

mlreg_house = house.drop(columns=['sqft_living', 'sqft_above', 'sqft_basement'])
new_house_corr = mlreg_house.corr()

pd.DataFrame(np.linalg.inv(new_house_corr.values), index = new_house_corr.index, 
             columns=new_house_corr.columns)

# We can notice that after removing those features, the VIF scores of the other features and
# especially our target variable decreased, approaching 1 (which is the point at which there is no correlation at all).

"""### Building the Model"""

# redefining the new features

X_new = mlreg_house.drop(columns= ['price'])
y_new = mlreg_house.price

X_train_new, X_test_new, y_train_new, y_test_new = train_test_split(X_new,y_new, test_size= 0.3, random_state= 10)

X_train_mlreg = X_train_new.copy(deep=True)
X_test_mlreg = X_test_new.copy(deep=True)
y_train_mlreg = y_train_new.copy(deep=True)
y_test_mlreg = y_test_new.copy(deep=True)

ml_regressor = LinearRegression()
ml_regressor.fit(X_train_mlreg,y_train_mlreg)

coeff_ml_regressor = pd.DataFrame(ml_regressor.coef_, X_new.columns, columns=['Coefficient'])
coeff_ml_regressor.plot(kind='barh', figsize=(20,7))
plt.title('Multiple Regression Base-line Model')
plt.axvline(x=0, color='.2')
plt.subplots_adjust(left=.5)

# The below means that a unit increase in waterfront leads to the highest increase in price
# and a unit increase in longitude leads to the highest decrease in price.

# Making Predictions

y_pred_mlreg = ml_regressor.predict(X_test_mlreg)

df_mlreg = pd.DataFrame({'Actual': y_test_mlreg, 'Predicted': y_pred_mlreg})

sns.regplot(df_mlreg.Actual, df_mlreg.Predicted)

# From the above, the predictions seem to be okay for most of the data, except the extreme outliers 
# of the most expensive houses.

# Evaluating the Algorithm

mae_mlreg = metrics.mean_absolute_error(y_test_mlreg, y_pred_mlreg)
mse_mlreg = metrics.mean_squared_error(y_test_mlreg, y_pred_mlreg)
rmse_mlreg = np.sqrt(metrics.mean_squared_error(y_test_mlreg, y_pred_mlreg))

ratio_mlreg = (rmse_mlreg / mlreg_house.price.mean()) * 100

r2_score_mlreg = r2_score(y_test_mlreg, y_pred_mlreg)

print('Mean Absolute Error:', mae_mlreg)
print('Mean Squared Error:', mse_mlreg)
print('Root Mean Squared Error:', rmse_mlreg)
print('Percentage of RMSE to mean is: ' +str(ratio_mlreg) + ' %')
print('R score:', r2_score_mlreg)

"""### Multiple Linear Regression Model Recommendation

This will be the basis to compare the baseline models of the other regression models. This model is not very accurate because the Percentage of RMSE to mean is 39%. It still made reasonably good predictions as can be seen in the plot above sice the R-score was not below the wildly used cut-off point of 0.60 for a bad model. This inaccuracy could have been caused by:
1. The factor that the data does not follow a normal distribution (as we had seen in the Analysis section)
2. Poor features, i.e., the features we used may not have had a high enough correlation to the values we were trying to predict.

## RIDGE REGRESSION

### Building Non-Normalized Model
"""

X_train_ridge = X_train.copy(deep=True)
X_test_ridge = X_test.copy(deep=True)
y_train_ridge = y_train.copy(deep=True)
y_test_ridge = y_test.copy(deep=True)

ridge_regressor = Ridge()
ridge_regressor.fit(X_train_ridge,y_train_ridge)

coeff_ridge = pd.DataFrame(ridge_regressor.coef_, X.columns, columns=['Coefficient'])
coeff_ridge.plot(kind='barh', figsize=(20,7))
plt.title('Ridge Regression Base-line Model')
plt.axvline(x=0, color='.2')
plt.subplots_adjust(left=.5)

# without normalization, the results are different to the Multiple Linear Regression Model
# latitude now seems to have more weight

# Making Predictions

y_pred_ridge = ridge_regressor.predict(X_test_ridge)

df_ridge = pd.DataFrame({'Actual': y_test_ridge, 'Predicted': y_pred_ridge})

sns.regplot(df_ridge.Actual, df_ridge.Predicted)

# From the above, the predictions seem to be similar to the Multiple Linear Regression Model.

# Evaluating the Algorithm

mae_ridge = metrics.mean_absolute_error(y_test_ridge, y_pred_ridge)
mse_ridge = metrics.mean_squared_error(y_test_ridge, y_pred_ridge)
rmse_ridge = np.sqrt(metrics.mean_squared_error(y_test_ridge, y_pred_ridge))

ratio_ridge = (rmse_ridge / house.price.mean()) * 100

r2_score_ridge = r2_score(y_test_ridge, y_pred_ridge)

print('Mean Absolute Error:', mae_ridge)
print('Mean Squared Error:', mse_ridge)
print('Root Mean Squared Error:', rmse_ridge)
print('Percentage of RMSE to mean is: ' +str(ratio_ridge) + ' %')
print('R score:', r2_score_ridge)

# This model is not very accurate because the Percentage of RMSE to mean is 37%, 
# but is better than the Multiple Linear Model
# R Score is also better than that of the Multiple Linear Regression Model.

"""### Building Normalized Model"""

X_train_Ridge = X_train.copy(deep=True)
X_test_Ridge = X_test.copy(deep=True)
y_train_Ridge = y_train.copy(deep=True)
y_test_Ridge = y_test.copy(deep=True)

Ridge_regressor = Ridge(normalize=True)
Ridge_regressor.fit(X_train_Ridge,y_train_Ridge)

coeff_Ridge = pd.DataFrame(Ridge_regressor.coef_, X.columns, columns=['Coefficient'])
coeff_Ridge.plot(kind='barh', figsize=(20,7))
plt.title('Ridge Regression Normalized Base-line Model')
plt.axvline(x=0, color='.2')
plt.subplots_adjust(left=.5)

# This model has some differences as can be seen in the bedrooms, bathrooms and floors coefficents
# as compared to the non-normalized model.
# Furthermore, the waterfront coefficient seems to now have a similar effect to the price as the
# latitude coefficient.

# Making Predictions

y_pred_Ridge = Ridge_regressor.predict(X_test_Ridge)

df_Ridge = pd.DataFrame({'Actual': y_test_Ridge, 'Predicted': y_pred_Ridge})

sns.regplot(df_Ridge.Actual, df_Ridge.Predicted)

# The predictions though, still seem to be similar to the previous 2 models.

# Evaluating the Algorithm

mae_Ridge = metrics.mean_absolute_error(y_test_Ridge, y_pred_Ridge)
mse_Ridge = metrics.mean_squared_error(y_test_Ridge, y_pred_Ridge)
rmse_Ridge = np.sqrt(metrics.mean_squared_error(y_test_Ridge, y_pred_Ridge))

ratio_Ridge = (rmse_Ridge / house.price.mean()) * 100

r2_score_Ridge = r2_score(y_test_Ridge, y_pred_Ridge)

print('Mean Absolute Error:', mae_Ridge)
print('Mean Squared Error:', mse_Ridge)
print('Root Mean Squared Error:', rmse_Ridge)
print('Percentage of RMSE to mean is: ' +str(ratio_Ridge) + ' %')
print('R score:', r2_score_Ridge)

# The RSME and The R score are worse than the first 2 models.

"""### Ridge Regression Recommendation

The non-normalized Ridge regression model performed the best so far, however, when normlizing the data, in order to carry out proper predictions, the results are the worst so far. In addition, RMSE tells you how concentrated the data is around the line of best fit, as it describe how far spread out the residuals are. A higher RMSE percentage compared to the mean (typically more than 10%) means the model is not very accurate. For Ridge, Lasso and Elastic Net Regression Models, since they do not assume data is normal, unlike Multiple Linear Regression, this high RMSE could be explained by possible poor features, i.e., the features we used may not have had a high enough correlation to the values we were trying to predict.

## LASSO REGRESSION

### Building Non-Normalized Model
"""

X_train_lasso = X_train.copy(deep=True)
X_test_lasso = X_test.copy(deep=True)
y_train_lasso = y_train.copy(deep=True)
y_test_lasso = y_test.copy(deep=True)

lasso_regressor = Lasso()
lasso_regressor.fit(X_train_lasso,y_train_lasso)

coeff_lasso = pd.DataFrame(lasso_regressor.coef_, X.columns, columns=['Coefficient'])
coeff_lasso.plot(kind='barh', figsize=(20,7))
plt.title('Lasso Regression Base-line Model')
plt.axvline(x=0, color='.2')
plt.subplots_adjust(left=.5)

# We can see differences in yr_built and bathrooms from the Ridge Models.

# Making Predictions

y_pred_lasso = lasso_regressor.predict(X_test_lasso)

df_lasso = pd.DataFrame({'Actual': y_test_lasso, 'Predicted': y_pred_lasso})

sns.regplot(df_lasso.Actual, df_lasso.Predicted)

# The predictions though, still seem to be similar to the previous 3 models.

# Evaluating the Algorithm

mae_lasso = metrics.mean_absolute_error(y_test_lasso, y_pred_lasso)
mse_lasso = metrics.mean_squared_error(y_test_lasso, y_pred_lasso)
rmse_lasso = np.sqrt(metrics.mean_squared_error(y_test_lasso, y_pred_lasso))

ratio_lasso = (rmse_lasso / house.price.mean()) * 100
r2_score_lasso = r2_score(y_test_lasso, y_pred_lasso)

print('Mean Absolute Error:', mae_lasso)
print('Mean Squared Error:', mse_lasso)
print('Root Mean Squared Error:', rmse_lasso)
print('Percentage of RMSE to mean is: ' +str(ratio_lasso) + ' %')
print('R score:', r2_score_lasso)

# The R score is similar to the normalized Ridge model.
# Furthermore, the RSME is the best yet

"""### Building Normalized Model"""

X_train_Lasso = X_train.copy(deep=True)
X_test_Lasso = X_test.copy(deep=True)
y_train_Lasso = y_train.copy(deep=True)
y_test_Lasso = y_test.copy(deep=True)

Lasso_regressor = Lasso(normalize= True)
Lasso_regressor.fit(X_train_Lasso,y_train_Lasso)

coeff_Lasso = pd.DataFrame(Lasso_regressor.coef_, X.columns, columns=['Coefficient'])
coeff_Lasso.plot(kind='barh', figsize=(20,7))
plt.title('Lasso Regression Normalized Base-line Model')
plt.axvline(x=0, color='.2')
plt.subplots_adjust(left=.5)

# Similar to the Lasso Non-normalized plot.

y_pred_Lasso = Lasso_regressor.predict(X_test_Lasso)

df_Lasso = pd.DataFrame({'Actual': y_test_Lasso, 'Predicted': y_pred_Lasso})

sns.regplot(df_Lasso.Actual, df_Lasso.Predicted)

# The predictions still seem to be similar to the previous 4 models.

# Evaluating the Algorithm

mae_Lasso = metrics.mean_absolute_error(y_test_Lasso, y_pred_Lasso)
mse_Lasso = metrics.mean_squared_error(y_test_Lasso, y_pred_Lasso)
rmse_Lasso = np.sqrt(metrics.mean_squared_error(y_test_Lasso, y_pred_Lasso))

ratio_Lasso = (rmse_Lasso / house.price.mean()) * 100
r2_score_Lasso = r2_score(y_test_Lasso, y_pred_Lasso)

print('Mean Absolute Error:', mae_Lasso)
print('Mean Squared Error:', mse_Lasso)
print('Root Mean Squared Error:', rmse_Lasso)
print('Percentage of RMSE to mean is: ' +str(ratio_Lasso) + ' %')
print('R score:', r2_score_Lasso)

# The RMSE and R-score is similar to the non-normalized Lasso models.

"""### Lasso Regression Recommendation

Lasso has the best results so far. It has the lowest RSME for both non-normalised and normalised models at 37% (similar to normalised Ridge model). However it performs better on the R-scores, for both models. R-score is a statistical measure of how close the data are to the fitted regression line. It is also known as the coefficient of determination, or the coefficient of multiple determination for multiple regression. 0% indicates that the model explains none of the variability of the response data around its mean.
100% indicates that the model explains all the variability of the response data around its mean. The Lasso Models show that 70% of the data's variance is explained by the models.

## ELASTIC NET REGRESSION

### Building Non-Normalized Model
"""

X_train_elastic = X_train.copy(deep=True)
X_test_elastic = X_test.copy(deep=True)
y_train_elastic = y_train.copy(deep=True)
y_test_elastic = y_test.copy(deep=True)

elastic_regressor = ElasticNet()
elastic_regressor.fit(X_train_elastic,y_train_elastic)

coeff_elastic = pd.DataFrame(elastic_regressor.coef_, X.columns, columns=['Coefficient'])
coeff_elastic.plot(kind='barh', figsize=(20,7))
plt.title('Elastic Net Regression Base-line Model')
plt.axvline(x=0, color='.2')
plt.subplots_adjust(left=.5)

# Differences can be seen in long, lat, yr_built, grade, condition, view, waterfront, sqft_living
# and bathrooms and bedrooms features, from the Multiple Linear Model.

# Making Predictions

y_pred_elastic = elastic_regressor.predict(X_test_elastic)

df_elastic = pd.DataFrame({'Actual': y_test_elastic, 'Predicted': y_pred_elastic})

sns.regplot(df_elastic.Actual, df_elastic.Predicted)

# The predictions still seem to be similar to the previous 5 models.

# Evaluating the Algorithm

mae_elastic = metrics.mean_absolute_error(y_test_elastic, y_pred_elastic)
mse_elastic = metrics.mean_squared_error(y_test_elastic, y_pred_elastic)
rmse_elastic = np.sqrt(metrics.mean_squared_error(y_test_elastic, y_pred_elastic))

ratio_elastic = (rmse_elastic / house.price.mean()) * 100
r2_score_elastic = r2_score(y_test_elastic, y_pred_elastic)

print('Mean Absolute Error:', mae_elastic)
print('Mean Squared Error:', mse_elastic)
print('Root Mean Squared Error:', rmse_elastic)
print('Percentage of RMSE to mean is: ' +str(ratio_elastic) + ' %')
print('R score:', r2_score_elastic)

# It's RMSE and R-score is one of the worst.

"""### Building Normalized Model"""

X_train_Elastic = X_train.copy(deep=True)
X_test_Elastic = X_test.copy(deep=True)
y_train_Elastic = y_train.copy(deep=True)
y_test_Elastic = y_test.copy(deep=True)

Elastic_regressor = ElasticNet(normalize= True)
Elastic_regressor.fit(X_train_Elastic,y_train_Elastic)

coeff_Elastic = pd.DataFrame(Elastic_regressor.coef_, X.columns, columns=['Coefficient'])
coeff_Elastic.plot(kind='barh', figsize=(20,7))
plt.title('Elastic Net Regression Normalized Base-line Model')
plt.axvline(x=0, color='.2')
plt.subplots_adjust(left=.5)

# So far, it is the most different plot from them all.

# Making Predictions

y_pred_Elastic = Elastic_regressor.predict(X_test_Elastic)

df_Elastic = pd.DataFrame({'Actual': y_test_Elastic, 'Predicted': y_pred_Elastic})

sns.regplot(df_Elastic.Actual, df_Elastic.Predicted)

# The predictions still seem to be similar to the previous 6 models.

# Evaluating the Algorithm

mae_Elastic = metrics.mean_absolute_error(y_test_Elastic, y_pred_Elastic)
mse_Elastic = metrics.mean_squared_error(y_test_Elastic, y_pred_Elastic)
rmse_Elastic = np.sqrt(metrics.mean_squared_error(y_test_Elastic, y_pred_Elastic))

ratio_Elastic = (rmse_Elastic / house.price.mean()) * 100
r2_score_Elastic = r2_score(y_test_Elastic, y_pred_Elastic)

print('Mean Absolute Error:', mae_Elastic)
print('Mean Squared Error:', mse_Elastic)
print('Root Mean Squared Error:', rmse_Elastic)
print('Percentage of RMSE to mean is: ' +str(ratio_Elastic) + ' %')
print('R score:', r2_score_Elastic)

# This model has the worst RMSE and R-Score values

"""### Elastic Net Regression Recommendation

Elastic Net performed the worst when compared to all the other models. The RMSEs indicate that the model is not accurate and the Rscore, especially of the normalized model shows that only 0.05% of the variance is explained by the model, which is horrible.

## RESIDUAL PLOTS AND HETEROSCEDASTICITY USING BARTLETT'S TEST

Since Lasso Regression Models have the best RMSES and R-scores, we'll check for heteroskedasticity to help determine which model to use, and perform hyperparameter tuning on it to achieve better results. This test will show why we chose this over the baseline  Multiple Linear Regression
"""

residuals = np.subtract(y_pred_mlreg, y_test_mlreg)
pd.DataFrame(residuals).describe()

plt.scatter(y_pred_mlreg, residuals, color='black')
plt.ylabel('residual')
plt.xlabel('fitted values')
plt.axhline(y= residuals.mean(), color='red', linewidth=1)
plt.show()

# The data seems to be cone-shaped showing possibility of heteroskedasticity

# Let's be thorough though, and perform a heteroskedasticity test.
# For this we will use bartlett's test. The test establishes as a null hypothesis that the variance is equal for all our datapoints,
# and the new hypothesis that the variance is different for at least one pair of datapoints.

test_result, p_value = sp.stats.bartlett(y_pred_mlreg, residuals)

# To interpret the results we must compare to a p_value of 0.05

print(p_value)

if (p_value < 0.05):
  print('the variances are unequal, and the model shows heteroskedasicity')
else:
  print('the variances are homogeneous!')

"""Since the model does not have homogenous variances, as expected since we already knew it was not normalized, we will use the Lasso Regression Model and Tune it accordingly.

## HYPERPARAMETER TUNING LASSO REGRESSION MODEL
"""

# MACHINE LEARNING PIPELINE

from sklearn.compose import TransformedTargetRegressor
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LassoCV

X_train_ = X_train.copy(deep=True)
X_test_ = X_test.copy(deep=True)
y_train_ = y_train.copy(deep=True)
y_test_ = y_test.copy(deep=True)
X_ = X.copy(deep=True)

preprocessor = StandardScaler()
preprocessor.fit(X_)

def func(x):
  return np.log(x)
def inverse_func(x):
  return np.exp(x)

model = make_pipeline(
    preprocessor,
    TransformedTargetRegressor(
        regressor=LassoCV(alphas=np.logspace(-10, 10, 21), max_iter=100000),
        func=func,
        inverse_func=inverse_func
    )
)

model.fit(X_train_, y_train_)

# First we verify which value of alpha has been selected.
model[-1].regressor_.alpha_

# Then we check the quality of the predictions.

coefs = pd.DataFrame(
    model.named_steps['transformedtargetregressor'].regressor_.coef_,
    columns=['Coefficients'], index=X.columns
)
coefs.plot(kind='barh', figsize=(9, 7))
plt.title('Lasso model, regularization, normalized variables')
plt.axvline(x=0, color='.5')
plt.subplots_adjust(left=.3)

y_pred_ = model.predict(X_test_)

df_ = pd.DataFrame({'Actual': y_test_, 'Predicted': y_pred_})

sns.regplot(df_.Actual, df_.Predicted)

# As can be seen, our prediction values now seem to be much closer to the Actual data.

# Evaluating the Algorithm

mae_ = metrics.mean_absolute_error(y_test_, y_pred_)
mse_ = metrics.mean_squared_error(y_test_, y_pred_)
rmse_ = np.sqrt(metrics.mean_squared_error(y_test_, y_pred_))

ratio_ = (rmse_ / house.price.mean()) * 100
r2_score_ = r2_score(y_test_, y_pred_)

print('Mean Absolute Error:', mae_)
print('Mean Squared Error:', mse_)
print('Root Mean Squared Error:', rmse_)
print('Percentage of RMSE to mean is: ' +str(ratio_) + ' %')
print('R score:', r2_score_)

# The RMSE value is the lowest we have found so far.
# And the R-score is the highest we have found so far

"""# CONCLUSION

The Model above is our chosen model as it has provided the best results after hyperparameter tuning. The Percentage of RMSE to mean is the lowest at 36% (meaning it is the most accurate model we've built) and the R-score is the best at 0.71 (meaning it explains 71% of the variance in the data).

# CHALLENGING THE SOLUTION

## QUANTILE REGRESSION
"""

# We'll compare our best model above with Quantile regression

from statsmodels.regression.quantile_regression import QuantReg
import statsmodels.formula.api as smf

X_train_quant = X_train.copy(deep=True)
X_test_quant = X_test.copy(deep=True)
y_train_quant = y_train.copy(deep=True)
y_test_quant = y_test.copy(deep=True)

scaler = StandardScaler()
X_train_quant = scaler.fit_transform(X_train_quant)
X_test_quant = scaler.transform(X_test_quant)

# DataFrame for Train data

df_1 = pd.DataFrame(X_train_quant, columns= X.columns)

target = pd.Series(y_train_quant, name="price")
df_2 =  target.to_frame()
df_2 = df_2.reset_index()
df_2.drop(columns=['index'], inplace=True)

train_data = pd.concat([df_1,df_2], axis=1)
train_data.head()

train_data.columns = ['bedrooms',	'bathrooms',	'sqft_living','sqft_lot',	'floors',	'waterfront',
                      'view',	'condition',	'grade',	'sqft_above',	'sqft_basement',	'yr_built',	
                      'yr_renovated',	'zipcode',	'lat',	'long',	'sqft_living15',	'sqft_lot15',	'price']
train_data.sqft_basement

# Summary report of dataset at 0.5 Quantile

mod = smf.quantreg('price ~ bedrooms+bathrooms+sqft_living+sqft_lot+floors+waterfront+view+condition+grade+sqft_above', train_data)
res = mod.fit(q=.5)
print(res.summary())

# We need to do PCA for feature reduction since the module doesn't seem to take more than 10 features

from sklearn.decomposition import PCA

y_train_quant = scaler.fit_transform(y_train_quant.values.reshape(-1,1))
y_test_quant = scaler.fit_transform(y_test_quant.values.reshape(-1,1))

pca = PCA(n_components=9)
X_train_quant = pca.fit_transform(X_train_quant)
X_test_quant = pca.transform(X_test_quant)

explained_variance = pca.explained_variance_ratio_
explained_variance 

# The components should explain at least 80% of the variance.
# With 9 Principal Components, it's 83%

columns = ['PC1','PC2','PC3','PC4','PC5','PC6','PC7','PC8','PC9']

principal_train = pd.DataFrame(X_train_quant, columns=columns)
principal_test = pd.DataFrame(X_test_quant, columns=columns)

principal_train['price'] = y_train_quant

mod = smf.quantreg('price ~ PC1+PC2+PC3+PC4+PC5+PC6+PC7+PC8+PC9', principal_train)
res = mod.fit(q=.5) 
print(res.summary())

# Evaluating the Model

y_pred_quant = res.predict(principal_test)

fig = plt.figure(figsize=(10, 5))
plt.plot(np.arange(0,len(y_test_quant),1), y_test_quant, 'b.', markersize=10, label='Actual')
plt.plot(np.arange(0,len(y_test_quant),1), y_pred_quant, 'r-', label='Prediction', alpha =0.8)
plt.xlabel('Price')
plt.ylabel('Observations')
plt.legend(loc='upper right')

# As can be seen, the higher price values are not being predicted accurately by the quantile(.5)

test_plot = pd.DataFrame({'y_test':y_test_quant.ravel(),'y_pred': y_pred_quant})
test_plot.sort_values(by=['y_test'],inplace=True)
plt.plot(np.arange(0,len(test_plot),1), test_plot['y_pred'])
plt.plot(np.arange(0,len(test_plot),1), test_plot['y_test'], alpha=0.5)
plt.ylabel('Yellow = y_test,  Blue = y_pred')
plt.xlabel('Index')
plt.title('Predicted vs. Real');


# Below are the Observations sorted by y_test values, i.e., the higher the index,
# the higher the Price

# We can see that as the price gets beyond 6000, the prediction becomes quite inaccurate.

plt.scatter(y_test_quant.ravel(), y_pred_quant)
plt.plot(y_test_quant.ravel(), y_test_quant.ravel(), "r")
plt.xlabel('y_actual')
plt.ylabel('y_predicted')

# The heteroskedasticity in the model can be seen below as the values veer off the red
# line that represents the predicted values.

# Evaluating the Algorithm

mae_quant = metrics.mean_absolute_error(y_test_quant, y_pred_quant)
mse_quant = metrics.mean_squared_error(y_test_quant, y_pred_quant)
rmse_quant = np.sqrt(metrics.mean_squared_error(y_test_quant, y_pred_quant))

ratio_quant = (rmse_quant / house.price.mean()) * 100
r2_score_quant = r2_score(y_test_quant, y_pred_quant)

print('Mean Absolute Error:', mae_quant)
print('Mean Squared Error:', mse_quant)
print('Root Mean Squared Error:', rmse_quant)
print('Percentage of RMSE to mean is: ' +str(ratio_quant) + ' %')
print('R score:', r2_score_quant)

# The RMSE is the best by far, however, the R-score is lower than our lasso model.
# To improve the prediction's R-score, the data could be grouped into quantiles 0.1 - 0.9

"""# RECOMMENDATION

The Lasso Model provided the best R score of 0.71, however, the Quantile Regression provided the best RMSE score of 0.00011%. This means that the Lasso model has the most variance explained by the model and Quantile has the most accurate results. However, from our plots it can be seen that this accuracy is only true for lower value houses as the most expensive ones are not accurately predicted. To determine if this accuracy score is good a suggestion could be using Root Mean Square Logarithmic Error due to the transformations we did and see if the score is any different. Another suggestion is to improve the prediction's R-score, by grouping the data into quantiles 0.1 - 0.9 and carrying out the prediction based on the quantile which the data falls in.

---

# FOLLOW UP QUESTIONS

## a.) Did we have the right data?

Yes we did as most of our R-scores were higher than the recommended minimum of 0.60

## b.) Do we need other data to answer our question?

Yes we do, our best model describes 71% of the variance in the data, meaning there's 29% not captured in the data. There's room to improve this by gathering more data that could describe some of this 29% variance that we have not captured in the model.

## c.) Did we have the right question?

Yes we did. Home prices are important since buying a home is the most expensive single purchase that most people make in their life, and home ownership is one of the top goals of people, especially families.
"""