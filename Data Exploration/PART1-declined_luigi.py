# python RejectPart1_luigi.py FeatureSelection --loginemail agrawal.r@husky.neu.edu --loginpassword ADS@12345

import luigi
import requests
import sys
import logging
import pandas as pd
import numpy as np
import glob
import os
from bs4 import BeautifulSoup
from zipfile import ZipFile
from io import BytesIO
from luigi.parameter import MissingParameterException

def changedatatype(df):
    #Change the data types for all column
    df[['Amount Requested','Risk_Score']] = df[['Amount Requested','Risk_Score']].astype('int64')
    df[['Debt-To-Income Ratio']] = df[['Debt-To-Income Ratio']].astype('float64')
    return df

def extractZip(yearwisedata,path):
    r = requests.get(yearwisedata)
    z = ZipFile(BytesIO(r.content))
    z.extractall(path)


class getWebUrls(luigi.Task):
    logging.debug('In the Task : getWebUrls')
    loginemail=luigi.Parameter()
    loginpassword=luigi.Parameter()
    # login_email='agrawal.r@husky.neu.edu'
    # login_password='ADS@12345'

    def run(self):
        url = 'https://www.lendingclub.com/account/login.action?'
        postUrl = 'https://www.lendingclub.com/info/download-data.action'
        payload = {'login_email': self.loginemail, 'login_password': self.loginpassword}
        with requests.Session() as s:
            loginRequest = s.post(url, data=payload)
            finalUrl = s.get(postUrl)
            linkhtml = finalUrl.text
            soup = BeautifulSoup(linkhtml, "html.parser")
            ziplist = soup.find_all('div', {"id": 'rejectedLoanStatsFileNamesJS'})
            Borrowerdata = []
            rejectLoandata = []
            rejectloanyearlist = []
            for div in ziplist:
                for d in div:
                    link = d.split('|')
                    Borrowerdata.extend(link)
            for data in Borrowerdata:
                if data != '':
                    rejectLoandata.append('https://resources.lendingclub.com/' + data)
            year_options = soup.findAll('select', {"id": 'rejectStatsDropdown'})[0].findAll("option")
            for year in year_options:
                rejectloanyearlist.append(year.text)
            dictionary = dict(zip(rejectloanyearlist, rejectLoandata))
            # print(dictionary)
            for year in dictionary:
                url = dictionary[year]
                yearpath = str(os.getcwd()) + "/RejectData/" + year
                extractZip(url, yearpath)
            yeardict=pd.DataFrame(list(dictionary.items()),columns=['year','Link'])
            yeardict.to_csv(self.output().path,index=False)

    def output(self):
        return luigi.LocalTarget('rejectdictionary.csv')


class getData(luigi.Task):
    logging.debug('In the Task : getData')
    loginemail=luigi.Parameter()
    loginpassword=luigi.Parameter()

    def requires(self):
        yield getWebUrls(loginemail=self.loginemail,loginpassword=self.loginpassword)

    def run(self):
        writeHeader2 = True
        # customyear = ['2007 - 2011','2016 Q2']
        df_dict=pd.read_csv(getWebUrls(loginemail=self.loginemail,loginpassword=self.loginpassword).output().path,low_memory=False,encoding='ISO-8859-1')
        print(df_dict['year'])
        for year in df_dict['year']:
        # for year in customyear:
            yearpath = str(os.getcwd()) + "/RejectData/" + year
            for filename in os.listdir(yearpath):
                print(filename)
                newFile = "RejectModifiedData.csv"
                for f in glob.glob(yearpath + '/' + filename):
                    datadf = pd.read_csv(f, skiprows=1, skipfooter=2, engine='python')
                    # datadf = datadf[datadf.id != 'Loans that do not meet the credit policy']
                    with open(newFile, 'a', encoding='utf-8', newline="") as file:
                        for f in glob.glob(str(os.getcwd()) + '/' + newFile):
                            if writeHeader2 is True:
                                datadf.to_csv(self.output().path , mode='w', header=True, index=False)
                                writeHeader2 = False
                            else:
                                datadf.to_csv(self.output().path, mode='a', header=False, index=False)

    def output(self):
        return luigi.LocalTarget('RejectModifiedData.csv')

class handleMissingData(luigi.Task):
    logging.debug('In the Task : handleMissingData')
    loginemail=luigi.Parameter()
    loginpassword=luigi.Parameter()

    def requires(self):
        yield getData(loginemail=self.loginemail, loginpassword=self.loginpassword)

    def run(self):
        reject_df=pd.read_csv(getData(loginemail=self.loginemail,loginpassword=self.loginpassword).output().path,low_memory=False,encoding='ISO-8859-1')
        print('Removing unused columns')

        reject_df.drop(['Zip Code'], axis=1, inplace=True)
        column_naper_dict = {}
        print('Removing columns with nan% > 80%')
        for column in reject_df:
            if reject_df[column].isnull().sum() > 0:
                column_naper_dict[column] = reject_df[column].isnull().sum() / 11079372
                if column_naper_dict[column] > 0.80:
                    reject_df.drop(column, axis=1, inplace='True')
        # Handling missing data
        print('Handling missing data')
        reject_df["Debt-To-Income Ratio"] = pd.Series(reject_df['Debt-To-Income Ratio']).str.replace('%', '')
        reject_df.replace('n/a', np.nan, inplace=True)
        reject_df['Employment Length'].fillna(value=0, inplace=True)
        reject_df['Employment Length'].replace(to_replace='[^0-9]+', value='', inplace=True, regex=True)
        reject_df['Employment Length'] = reject_df['Employment Length'].astype(int)
        reject_df["Risk_Score"].fillna(0, inplace=True)
        reject_df['Loan Title'] = reject_df['Loan Title'].fillna('other')
        reject_df['State'] = reject_df['State'].fillna('NA')
        reject_df = changedatatype(reject_df)
        print('Creating Cleaned CSV file')
        reject_df.to_csv(self.output().path, header=True, index=False)

    def output(self):
        return luigi.LocalTarget('CleanedRejectLoan.csv')

class FeatureSelection(luigi.Task):
    logging.debug('In the Task : FeatureSelection')
    loginemail=luigi.Parameter()
    loginpassword=luigi.Parameter()

    def requires(self):
        yield handleMissingData(loginemail=self.loginemail, loginpassword=self.loginpassword)

    def run(self):
        loanrejectfreature_df=pd.read_csv(handleMissingData(loginemail=self.loginemail,loginpassword=self.loginpassword).output().path,low_memory=False,encoding='ISO-8859-1')
        cor = loanrejectfreature_df.corr()
        cor.loc[:, :] = np.tril(cor, k=-1)  # below main lower triangle of an array
        cor = cor.stack()
        cor[(cor > 0.55) | (cor < -0.55)]
        correction_df = pd.DataFrame()
        correction_df = cor

        correction_df.to_csv(self.output().path,mode='w')

    def output(self):
        return luigi.LocalTarget('RejectCorrelation.csv')


if __name__ == '__main__':
    try:
        luigi.run()
    except MissingParameterException:
        print("Please provide Lending Club login credentials!")
        sys.exit()


