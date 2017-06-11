# python Part1_luigi.py getData --local-scheduler --loginemail agrawal.r@husky.neu.edu --loginpassword ADS@12345

import requests
import sys
import logging
import pandas as pd
import numpy as np
import glob
import os
import luigi
import warnings
from sklearn import preprocessing
from sklearn.linear_model import (LinearRegression, Ridge,Lasso, RandomizedLasso)
from sklearn.feature_selection import RFE, f_regression
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from bs4 import BeautifulSoup
from zipfile import ZipFile
from io import BytesIO
from luigi.parameter import MissingParameterException


def extractZip(yearwisedata,path):
    r = requests.get(yearwisedata)
    z = ZipFile(BytesIO(r.content))
    z.extractall(path)

def changedatatype(df):
    #Change the data types for all column
    df[['loan_amnt','funded_amnt','funded_amnt_inv','annual_inc','delinq_2yrs','fico_range_low','fico_range_high','inq_last_6mths']] = df[['loan_amnt','funded_amnt','funded_amnt_inv','annual_inc','delinq_2yrs','fico_range_low','fico_range_high','inq_last_6mths']].astype('int64')
    df[['mths_since_last_delinq','open_acc','pub_rec','revol_bal','total_acc']] = df[['mths_since_last_delinq','open_acc','pub_rec','revol_bal','total_acc']].astype('int64')
    df[['int_rate','revol_util']] = df[['int_rate','revol_util']].astype('float64')
    return df

def createDummies(df):
    dummies1 = pd.get_dummies(df['purpose']).rename(columns=lambda x: 'purpose' + str(x))
    df=pd.concat([df, dummies1], axis=1)
    dummies2 = pd.get_dummies(df['application_type']).rename(columns=lambda x: 'application_type' + str(x))
    df=pd.concat([df, dummies2], axis=1)
    return df

def rank_to_dict(ranks, names, order=1):
    minmax = MinMaxScaler()
    ranks = minmax.fit_transform(order*np.array([ranks]).T).T[0]
    ranks = map(lambda x: round(x, 2), ranks)
    return dict(zip(names, ranks ))

class getWebUrls(luigi.Task):

    loginemail=luigi.Parameter()
    loginpassword=luigi.Parameter()
    logging.debug('In the Task : getWebUrls')


    def run(self):
        url = 'https://www.lendingclub.com/account/login.action?'
        postUrl = 'https://www.lendingclub.com/info/download-data.action'
        payload = {'login_email': self.loginemail, 'login_password': self.loginpassword}
        with requests.Session() as s:
            loginRequest = s.post(url, data=payload)
            finalUrl = s.get(postUrl)
            linkhtml = finalUrl.text
            soup = BeautifulSoup(linkhtml, "html.parser")
            ziplist = soup.find_all('div', {"id": 'loanStatsFileNamesJS'})
            Borrowerdata = []
            Loandata = []
            loanyearlist = []
            for div in ziplist:
                for d in div:
                    link = d.split('|')
                    Borrowerdata.extend(link)
            for data in Borrowerdata:
                if data != '':
                    Loandata.append('https://resources.lendingclub.com/' + data)
            year_options = soup.findAll('select', {"id": 'loanStatsDropdown'})[0].findAll("option")
            for year in year_options:
                loanyearlist.append(year.text)
            dictionary = dict(zip(loanyearlist, Loandata))
            print(dictionary)
            for year in dictionary:
                url = dictionary[year]
                yearpath = str(os.getcwd()) + "/" + year
                extractZip(url, yearpath)
            yeardict=pd.DataFrame(list(dictionary.items()),columns=['year','Link'])
            yeardict.to_csv(self.output().path,index=False)

    def output(self):
        return luigi.LocalTarget('dictionary.csv')


class getData(luigi.Task):

    loginemail=luigi.Parameter()
    loginpassword=luigi.Parameter()
    logging.debug('In the Task : getData')

    def requires(self):
        yield getWebUrls(loginemail=self.loginemail,loginpassword=self.loginpassword)

    def run(self):
        writeHeader2 = True
        # customyear = ['2007 - 2011','2016 Q2']
        df_dict=pd.read_csv(getWebUrls(loginemail=self.loginemail,loginpassword=self.loginpassword).output().path)
        print(df_dict['year'])
        for year in df_dict['year']:
        # for year in customyear:
            yearpath = str(os.getcwd()) + "/" + year
            for filename in os.listdir(yearpath):
                print(filename)
                newFile = "ModifiedData.csv"
                for f in glob.glob(yearpath + '/' + filename):
                    datadf = pd.read_csv(f, skiprows=1, skipfooter=2, engine='python')
                    datadf = datadf[datadf['id'].astype(str) != 'Loans that do not meet the credit policy']
                    with open(newFile, 'a', encoding='utf-8', newline="") as file:
                        for f in glob.glob(str(os.getcwd()) + '/' + newFile):
                            if writeHeader2 is True:
                                datadf.to_csv(self.output().path , mode='w', header=True, index=False)
                                writeHeader2 = False
                            else:
                                datadf.to_csv(self.output().path, mode='a', header=False, index=False)

    def output(self):
        return luigi.LocalTarget('ModifiedData.csv')


class handleMissingData(luigi.Task):

    logging.debug('In the Task : handleMissingData')

    loginemail=luigi.Parameter()
    loginpassword=luigi.Parameter()

    def requires(self):
        yield getData(loginemail=self.loginemail,loginpassword=self.loginpassword)


    def run(self):
        loan_df = pd.read_csv(getData(loginemail=self.loginemail,loginpassword=self.loginpassword).output().path,low_memory=False,encoding='ISO-8859-1')
        print('Removing unused columns')
        #     loan_df = loan_df[loan_df.id != 'Loans that do not meet the credit policy']
        loan_df.drop(['id', 'member_id', 'emp_title', 'pymnt_plan', 'url', 'desc', 'title'], axis=1, inplace=True)
        column_naper_dict = {}
        print('Removing columns with nan% > 80%')
        for column in loan_df:
            if loan_df[column].isnull().sum() > 0:
                column_naper_dict[column] = loan_df[column].isnull().sum() / 1321847
                if column_naper_dict[column] > 0.80:
                    loan_df.drop(column, axis=1, inplace='True')
                    # Handling missing data
        print('Handling missing data')
        loan_df.term = pd.to_numeric(loan_df.term.str[:3])
        loan_df["int_rate"] = pd.Series(loan_df.int_rate).str.replace('%', '')
        loan_df["revol_util"] = pd.Series(loan_df.revol_util).str.replace('%', '')
        loan_df.replace('n/a', np.nan, inplace=True)
        loan_df.emp_length.fillna(value=0, inplace=True)
        loan_df['emp_length'].replace(to_replace='[^0-9]+', value='', inplace=True, regex=True)
        loan_df['emp_length'] = loan_df['emp_length'].astype(int)
        loan_df["annual_inc"].fillna(loan_df["annual_inc"].median(), inplace=True)
        loan_df["issue_d"] = loan_df["issue_d"].str.split("-")
        loan_df["issue_month"] = loan_df["issue_d"].str[0]
        loan_df["issue_year"] = loan_df["issue_d"].str[1]
        m = loan_df['mths_since_last_delinq'].max()  # max is 188 so this will be our imputed value.
        loan_df['mths_since_last_delinq'] = np.where(loan_df['mths_since_last_delinq'].isnull(), m,
                                                     loan_df['mths_since_last_delinq'])
        # Revol_util will involve a median value imputation.
        loan_df['revol_util'] = loan_df['revol_util'].fillna(loan_df['revol_util'].median())
        loan_df['tot_coll_amt'] = loan_df['tot_coll_amt'].fillna(loan_df['tot_coll_amt'].median())
        # tot_cur_bal will be fixed in similar manner.
        loan_df['tot_cur_bal'] = loan_df['tot_cur_bal'].fillna(loan_df['tot_cur_bal'].median())
        # total_rev_hi_lim will also contain median imputation
        loan_df['total_rev_hi_lim'] = loan_df['total_rev_hi_lim'].fillna(loan_df['total_rev_hi_lim'].median())
        loan_df['earliest_cr_line'] = loan_df['earliest_cr_line'].fillna('Unknown')
        loan_df['last_pymnt_d'] = loan_df['last_pymnt_d'].fillna('Unknown')
        loan_df['next_pymnt_d'] = loan_df['next_pymnt_d'].fillna('Unknown')
        loan_df['last_credit_pull_d'] = loan_df['last_credit_pull_d'].fillna('Unknown')
        loan_df['last_fico_range'] = loan_df.last_fico_range_low.astype(
            'str') + '-' + loan_df.last_fico_range_high.astype('str')
        loan_df['last_meanfico'] = (loan_df.fico_range_low + loan_df.fico_range_high) / 2
        loan_df = loan_df.fillna(0)
        loan_df = changedatatype(loan_df)
        print('Creating Cleaned CSV file')
        loan_df.to_csv(self.output().path, header=True, index=False)

    def output(self):
        return luigi.LocalTarget('CleanedFile.csv')

class processData(luigi.Task):
    logging.debug('In the Task : processData')
    loginemail=luigi.Parameter()
    loginpassword=luigi.Parameter()


    def requires(self):
        yield handleMissingData(loginemail=self.loginemail,loginpassword=self.loginpassword)

    def run(self):
        loanfreature_df = pd.read_csv(handleMissingData(loginemail=self.loginemail,loginpassword=self.loginpassword).output().path,low_memory=False,encoding='ISO-8859-1')
        # Make home owners in the "home_ownership" column as 1 and non-homeowner as 0
        home_positive = ['OWN', 'MORTGAGE']
        home_negative = ['RENT', 'NONE', 'OTHER', 'ANY']

        # filter out any word that is not within home_positive & home_negative

        loanfreature_df = loanfreature_df[loanfreature_df['home_ownership'].isin(home_positive + home_negative)].copy()

        loanfreature_df['home_ownership_category'] = loanfreature_df['home_ownership'].isin(home_positive).astype(int)

        # Make "verified" and "Source Verified" in the "verification_status" column as 1 and non-verified as 0

        verification_positive = ['Verified', 'Source Verified']

        verification_negative = ['Not Verified']

        loanfreature_df = loanfreature_df[
            loanfreature_df['verification_status'].isin(verification_positive + verification_negative)].copy()

        loanfreature_df['verification_status_category'] = loanfreature_df['verification_status'].isin(
            verification_positive).astype(int)
        # Discreet value integer encoder
        label_encoder = preprocessing.LabelEncoder()
        loanfreature_df['addr_state'] = label_encoder.fit_transform(loanfreature_df['addr_state'])
        print('Removing unused columns')
        loanfreature_df.drop(['sub_grade', 'issue_d', 'zip_code', 'earliest_cr_line', 'initial_list_status'], axis=1,inplace=True)
        loanfreature_df.to_csv(self.output().path, header=True, index=False)


    def output(self):
        return luigi.LocalTarget('ProcessedData.csv')


class featureSelection(luigi.Task):
    logging.debug('In the Task : featureSelection')
    loginemail=luigi.Parameter()
    loginpassword=luigi.Parameter()

    # login_email='agrawal.r@husky.neu.edu'
    # login_password='ADS@12345'

    def requires(self):
        yield processData(loginemail=self.loginemail,loginpassword=self.loginpassword)

    def run(self):
        loanfreature_df = pd.read_csv(processData(loginemail=self.loginemail, loginpassword=self.loginpassword).output().path,low_memory=False,encoding='ISO-8859-1')
        Y = loanfreature_df.int_rate
        loanfreature_df.drop('int_rate', axis=1, inplace=True)
        cols_to_keep = ['loan_amnt', 'term', 'emp_length', 'home_ownership_category', 'annual_inc',
                        'verification_status_category', 'purpose', 'addr_state', 'dti', 'delinq_2yrs',
                        'last_meanfico', 'inq_last_6mths', 'open_acc', 'revol_bal', 'revol_util', 'total_acc',
                        'mths_since_last_major_derog', 'funded_amnt_inv', 'installment', 'application_type', 'pub_rec',
                        'addr_state']
        loanfreature_df = loanfreature_df[cols_to_keep]
        loanfreature_df = createDummies(loanfreature_df)

        X = loanfreature_df._get_numeric_data()
        names = ["%s" % i for i in X]
        ranks = {}

        lr = LinearRegression(normalize=True)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=DeprecationWarning)
            lr.fit(X, Y)
            ranks["Linear reg"] = rank_to_dict((lr.coef_), names)

        ridge = Ridge(alpha=7)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=DeprecationWarning)
            ridge.fit(X, Y)
            ranks["Ridge"] = rank_to_dict((ridge.coef_), names)

        lasso = Lasso(alpha=.05)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=DeprecationWarning)
            lasso.fit(X, Y)
            ranks["Lasso"] = rank_to_dict(np.abs(lasso.coef_), names)

        rlasso = RandomizedLasso(alpha=0.00)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=DeprecationWarning)
            rlasso.fit(X, Y)
            ranks["Stability"] = rank_to_dict((rlasso.scores_), names)

        rf = RandomForestRegressor()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=DeprecationWarning)
            rf.fit(X, Y)
            ranks["RF"] = rank_to_dict(rf.feature_importances_, names)

        # stop the search when 5 features are left (they will get equal scores)
        rfe = RFE(lr, n_features_to_select=15)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=DeprecationWarning)
            rfe.fit(X, Y)
            ranks["RFE"] = rank_to_dict(rfe.ranking_, X.columns, order=-1)

        f, pval = f_regression(X, Y, center=True)
        ranks["Corr."] = rank_to_dict(f, names)

        r = {}
        for name in names:
            r[name] = round(np.mean([ranks[method][name]
                                     for method in ranks.keys()]), 2)
        methods = sorted(ranks.keys())
        ranks["Mean"] = r
        methods.append("Mean")

        #     f_rank = pd.DataFrame()
        print("\t%s" % "\t".join(methods))
        temp = "\t".join(methods)
        f = open("testing.txt", 'w')
        f.write(temp)
        f.write("\n")
        for name in names:
            temp = name + "\t" + " \t".join(map(str,
                                                [ranks[method][name] for method in methods]))
            f.write(temp)
            f.write("\n")
            print("%s\t%s" % (name, "\t".join(map(str,
                                                  [ranks[method][name] for method in methods]))))
        f.close()
        feature = pd.read_csv('testing.txt', sep='\t')
        feature.to_csv(self.output().path)


    def output(self):
        return luigi.LocalTarget('FeatureSelection.csv')

if __name__ == '__main__':
    try:
        luigi.run()
    except MissingParameterException:
        print("Please provide Lending Club login credentials!")
        sys.exit()


