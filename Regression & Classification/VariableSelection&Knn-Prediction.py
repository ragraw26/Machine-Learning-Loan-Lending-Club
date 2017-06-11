from multiprocessing import Process,Manager
from sklearn.feature_selection import RFE
from sklearn.metrics import *
from sklearn import linear_model
lm=linear_model.LinearRegression()
import statsmodels.formula.api as sm
import pandas as pd
import os
import math
from sklearn.neighbors import KNeighborsRegressor
from sklearn import preprocessing
from sklearn import cross_validation


# Recursive feature elimination
def RFElimination1(X_train1,train1_y,X_test1,test1_y, return_score_p1,name):
    print("in "+str(name))
    org = lm
    selector = RFE(org, 18, step=1)
    selector = selector.fit(X_train1, train1_y)
    #     print(selector.ranking_)
    rankingdf = pd.DataFrame(list(zip(X_train1.columns, selector.ranking_)), columns=["features", "ranking"])
    file="Features"+ str(name)
    rankingdf.to_csv(file+".csv")
    # print(rankingdf)
    result = sm.OLS(train1_y, X_train1).fit()
    # print(result.summary())
    pred = selector.predict(X_train1)
    sc = r2_score(train1_y, pred)
    # print("RFElimination:" + str(sc))
    # print(sc)
    return_score_p1[name] = sc
    print("Training Dataset")
    computations(selector,X_train1,train1_y)
    print("Testing Dataset")
    computations(selector,X_test1,test1_y)

#KNN
def KNNAnalysis(x_train1,y_train1,x_test1,y_test1):
    org=lm
    neigh = KNeighborsRegressor(n_neighbors=6)
    neigh.fit(x_train1,y_train1)
    print("KNN---------------")
    print("Testing Data:")
    computations(neigh,x_test1,y_test1)


def computations(org,x,y):
    testlr=org.predict(x)
    #Mean Absolute Error
    mae=mean_absolute_error(y,testlr);
    print("MAE:"+str(mae))
    #RMSE
    rmse=math.sqrt(mean_squared_error(y,testlr))
    print("RMSE:"+str(rmse))
    #Median Absolute error
    Medae=median_absolute_error(y,testlr)
    print("Median Absolute Error:"+str(Medae))

def createDummies(df):
    dummies1 = pd.get_dummies(df['purpose']).rename(columns=lambda x: 'purpose' + str(x))
    df=pd.concat([df, dummies1], axis=1)
    dummies2 = pd.get_dummies(df['application_type']).rename(columns=lambda x: 'application_type' + str(x))
    df=pd.concat([df, dummies2], axis=1)
    home_positive = ['OWN', 'MORTGAGE']
    home_negative = ['RENT', 'NONE', 'OTHER', 'ANY']

    # filter out any word that is not within home_positive & home_negative

    df = df[df['home_ownership'].isin(home_positive + home_negative)].copy()

    df['home_ownership_category'] = df['home_ownership'].isin(home_positive).astype(int)

    # Make "verified" and "Source Verified" in the "verification_status" column as 1 and non-verified as 0

    verification_positive = ['Verified', 'Source Verified']

    verification_negative = ['Not Verified']

    df = df[df['verification_status'].isin(verification_positive + verification_negative)].copy()
    label_encoder = preprocessing.LabelEncoder()
    df['addr_state'] = label_encoder.fit_transform(df['addr_state'])

    return df

if __name__ == '__main__':
    #     global score
    # Keep the following 10 features (variables) which are important
    cols_to_keep = ['term', 'purpose', 'dti', 'loan_amnt', 'annual_inc', 'home_ownership', 'addr_state',
                    'fico_range_high', 'emp_length', 'application_type', 'verification_status', 'revol_util',
                    'inq_last_6mths', 'open_acc_6m', 'pub_rec', 'pub_rec_bankruptcies', 'delinq_2yrs', 'open_acc',
                    'total_acc', 'mths_since_last_delinq', 'mths_since_last_major_derog']
    filename1 = str(os.getcwd()) + "\\Clusters\\cluster0.csv"
    df1 = pd.read_csv(filename1, skipinitialspace=True)
    train1, test1 = cross_validation.train_test_split(df1, train_size=0.7)
    train1_y = train1['int_rate']
    test1_y = test1['int_rate']
    train1_x = train1[cols_to_keep]
    train1_x=createDummies(train1_x)
    X_train1=train1_x._get_numeric_data()
    test1_x = test1[cols_to_keep]
    test1_x=createDummies(test1_x)
    X_test1=test1_x._get_numeric_data()

    filename2=str(os.getcwd())+"\\Clusters\\cluster1.csv"
    df2=pd.read_csv(filename2,skipinitialspace=True)
    train2, test2 = cross_validation.train_test_split(df2, train_size=0.7)
    train2_y = train2['int_rate']
    test2_y = test2['int_rate']
    train2_x = train2[cols_to_keep]
    train2_x=createDummies(train2_x)
    X_train2=train2_x._get_numeric_data()
    test2_x = test2[cols_to_keep]
    test2_x=createDummies(test2_x)
    X_test2=test2_x._get_numeric_data()

    filename3=str(os.getcwd())+"\\Clusters\\cluster2.csv"
    df3=pd.read_csv(filename3,skipinitialspace=True)
    train3, test3 = cross_validation.train_test_split(df3, train_size=0.7)
    train3_y = train3['int_rate']
    test3_y = test3['int_rate']
    train3_x = train3[cols_to_keep]
    train3_x=createDummies(train3_x)
    X_train3=train3_x._get_numeric_data()
    test3_x = test3[cols_to_keep]
    test3_x=createDummies(test3_x)
    X_test3=test3_x._get_numeric_data()

    filename4=str(os.getcwd())+"\\Clusters\\cluster3.csv"
    df4=pd.read_csv(filename4,skipinitialspace=True)
    train4, test4 = cross_validation.train_test_split(df4, train_size=0.7)
    train4_y = train4['int_rate']
    test4_y = test4['int_rate']
    train4_x = train4[cols_to_keep]
    train4_x=createDummies(train4_x)
    X_train4=train4_x._get_numeric_data()
    test4_x = test4[cols_to_keep]
    test4_x=createDummies(test4_x)
    X_test4=test4_x._get_numeric_data()

    filename5=str(os.getcwd())+"\\Clusters\\cluster4.csv"
    df5=pd.read_csv(filename5,skipinitialspace=True)
    train5, test5 = cross_validation.train_test_split(df5, train_size=0.7)
    train5_y = train5['int_rate']
    test5_y = test5['int_rate']
    train5_x = train5[cols_to_keep]
    train5_x=createDummies(train5_x)
    X_train5=train5_x._get_numeric_data()
    test5_x = test5[cols_to_keep]
    test5_x=createDummies(test5_x)
    X_test5=test5_x._get_numeric_data()

    manager = Manager()
    return_score_p1 = manager.dict()



    fileknn = str(os.getcwd()) + "\\CleanedFile.csv"
    dfknn = pd.read_csv(fileknn, skipinitialspace=True)
    train, test = cross_validation.train_test_split(dfknn, train_size=0.7)
    train_y = train['int_rate']
    test_y = test['int_rate']
    train_x = train[cols_to_keep]
    train_x=createDummies(train_x)
    X_trainknn=train_x._get_numeric_data()
    test_x = test[cols_to_keep]
    test_x=createDummies(test_x)
    X_testknn=test_x._get_numeric_data()

    p1 = Process(target=RFElimination1, args=(X_train1,train1_y,X_test1,test1_y,return_score_p1,"cluster0"))
    p2 = Process(target=RFElimination1,args=(X_train2,train2_y,X_test2,test2_y,return_score_p1,"cluster1"))
    p3 = Process(target=RFElimination1,args=(X_train3,train3_y,X_test3,test3_y,return_score_p1,"cluster2"))
    p4 = Process(target=RFElimination1,args=(X_train4,train4_y,X_test4,test4_y,return_score_p1,"cluster3"))
    p5 = Process(target=RFElimination1,args=(X_train5,train5_y,X_test5,test5_y,return_score_p1,"cluster4"))
    p6=  Process(target=KNNAnalysis,args=(X_trainknn,train_y,X_testknn,test_y))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()

    print(return_score_p1)

    # KNNAnalysis(X_trainknn,train_y,X_testknn,test_y)



