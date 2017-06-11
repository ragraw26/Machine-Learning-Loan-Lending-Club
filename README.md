# Machine-Learning-Loan-Lending-Club

We are working at a bank and we are considering investing in Lending club. Since there are no standard models, we are expected to build prediction models that will help you predict the interest rates based on various parameters users would input.

# Part 1: Data wrangling and exploratory data analysis

# Data Download and pre-processing
Our first challenge is to programmatically download the data from https://www.lendingclub.com/info/download-data.action
Our goal is to download the data programmatically from the website and create one dataset for the entire database.

# Exploratory Data analysis:
 Write a Jupyter notebook using R/Python to graphically represent different summaries of data.Summarize your findings in this notebook.
 Summarize your key insights about different user profiles, states, loan amounts etc.
 Create a Data scientist view of Power BI dashboards to illustrate your key insights

# Part II: Building and evaluating models

Our next goal is to build a model to predict interest rates. we will get leads from people with different profiles and you must decide if you will give loans or not and if you will give a loan, how much interest we would charge for those loans.

# Classification 
Use the “Loan Data” and the “Declined Loan Data” datasets to build classification models that will generate a flag whether to give a loan or not.
 Start with logistic regression using Jupyter and Python/R
 Compute ROC curve and Confusion matrices for training and testing datasets and comment on the results.
 Repeat this using Random Forest, Neural Network models and SVN algorithms.
 Choose one model you will deploy and implement this model on the Microsoft azure machinelearning studio and create a REST API
 You should be able to a new record (You can define what features you will use) and the result will be a flag whether you would give a loan or not.

# Clustering 
Once we have decided to give a loan, you should build models to decide what interest rate to give. We are debating whether to create one model for all customer prospects or segment data into clusters and then build prediction models specific to each cluster. You think of creating segments or clusters and build models one for each cluster. Your brainstorm with your team and come up with 3 possibilities
1. Segment data into clusters (you define how many) manually using categorical or numerical features.
For example, you can segment by state, by ownership of home, by average dti or a combination of
features.
2. You use a clustering algorithm (that can factor both numerical and categorical variables) and
segment data into k clusters. You will then build prediction models for each cluster.
3. No clusters; Just use data as is

# Prediction 
 Write a prediction script in a Jupyter notebook in R/Python that builds a Regression model for the
interest rate using data from the 3 clustering methodologies you worked
o Try variable selection and build the best model for each segment/cluster (
o Compute MAE, RMS, MAPE for training and testing datasets
o Repeat this using Random Forest, Neural Network models and KNN algorithms.
o Choose the best model amongst the 4 types of algorithms.
o Deploy the best algorithm/algorithms on Azure ML studio
