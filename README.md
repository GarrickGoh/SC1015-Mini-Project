# SC1015-Mini-Project
This is a Mini Project for SC1015 (Introduction to Data Science and Artificial Intelligience), our group will be focusing on the lot availability of carpark. Based on the user input of time, find the best carpark for the user to go, based on the available lots. (For purposes of this project, we will be focusing on the selected 10 carparks in the Jurong Area)
1. Data extraction: Web Scraping from https://data.gov.sg/dataset/carpark-availability for carpark availibility
2. Data Cleaning
3. Exploratory Data Analysis
4. Machine Learning

# Groupmates
Group 10
1. Garrick Goh - @GarrickGoh
2. Ivan Lai - @IvanL010
3. Ee Chern - @Pistato

# Contributions
1. Garrick Goh - Exploratory Data Analysis
2. Ivan Lai - Data Cleaning, Machine Learning Model 1 & 2, Cross-Validation: K-Fold & Forward-Chaining
3. Kwek Ee Chern - Data Extraction, Machine Learning Model 3, Conclusion

# Problem Definition
* Are we able to predict the availability of the carpark based on previous year's analysis?
* Which model is the most appropriate for predicting the lots available at the carpark?

# Models Used
1. Decision Tree Regressor
2. Autoregressive Integrated Moving Average (ARIMA)
3. Random Forest Regression

# Codes
## Jupyter Notebook 1 Data Cleaning
After extracting the data from https://data.gov.sg/dataset/carpark-availability, we cleaned and standardized the data for Exploratory Data Analysis and Machine Learning.
Parameters required for Machine Learning were also added.
Hour_Delta: Hours Passed from start date. (2018-01-01)
## Jupyter Notebook 2 Exploratory Data Analysis
Here we will be touching on the analysis of the 10 carparks and show the availability of lots over the years. We will be taking a look at the average lots available as well as the space used, and there will be graphs to showcase the information. There is also a time series graph to show the information over the years and an analysis of a weekly time series graph to see in depth the lots availability.
## Jupyter Notebook 3 Machine Learning Model 1 & 2: Decision Tree Regressor & ARIMA
#### Decision Tree Regressor: (Using Predictors: Day, Hour, Hour_Delta)
* Split Data Evenly By Carpark, Hour and Day
* Train Separately By Carpark to reduce Predictors in Branches
* 10-Fold Accuracy: 0.0153
* Conclusion: Inaccurate due to varying values in Predictors, resulting values spanned hours which further increase inaccuracy
#### ARIMA: (Using Continuous Time)
* Splitting of Data into 5 Time Continous Sections for Forward Chaining
* Training Auto-ARIMA model using First Section
* Testing Using Forward Chaining
* Testing Model using the other 4 sections one at a time, addding each section to Model after testing to improve results
* Conclusion: Only able to forecast values for the next 2 days, with varying accuracy.
## Jupyter Notebook 4 Machine Learning Model 3: Random Forest Regression 
#### Random Forest Regression: (Using Predictors: Day, Hour, Hour_Delta)
* Split Data Evenly By Carpark, Hour and Day
* Training Separately by Carpark to reduce error caused by cateogorical data with multiple levels
* 10-Fold Accuracy: 0.3429
* Prediction of available lots at the 10 carparks on 5th January 2022.
* Conclusion: Most feasible model to use to predict the availability of parking.

# Conclusion 
* Easier to find lots at off-peak hour when people drive to work 
* Try to avoid the largest carpark. More lots, more people going to park there.
* Able to use a model to predict availability of parking lots and make decisions accordingly.

# Learning Points From The Project
* Working with huge time series dataset
* More unique ways to present EDA
* Time series Machine Learning Models
* Time series Cross-Validations

# References
* https://towardsdatascience.com/5-types-of-plots-that-will-help-you-with-time-series-analysis-b63747818705
* https://realpython.com/pandas-groupby/
* https://towardsdatascience.com/a-quick-and-dirty-guide-to-random-forest-regression-52ca0af157f8
* https://github.com/Teo-KJ/Machine-Learning-Model-for-Car-Park-Where
* https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html
* https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_score.html
* https://www.machinelearningplus.com/time-series/arima-model-time-series-forecasting-python/
* https://alkaline-ml.com/pmdarima/modules/generated/pmdarima.arima.auto_arima.html
