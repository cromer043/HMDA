# -*- coding: utf-8 -*-
"""
Date Created: 2024/19/2024

@author: csromer
"""
#This file merges HMDA Data with MDI, CDFI, Community Bank Trad Banks and Fintechs
#pip install pandas
#pip install fuzzywuzzy
#pip install dask
#pip install statsmodels


#LAR Data Description
#https://ffiec.cfpb.gov/documentation/publications/loan-level-datasets/lar-data-fields
#TS Data Description
#https://ffiec.cfpb.gov/documentation/publications/loan-level-datasets/ts-data-fields

#2019-2021 Data
#https://ffiec.cfpb.gov/data-publication/one-year-national-loan-level-dataset/2021
#2022 Data
#https://ffiec.cfpb.gov/data-publication/snapshot-national-loan-level-dataset/2022

#Community bank list
#https://www.fdic.gov/resources/community-banking/cbi-data.html

#Credit union list 
#https://catalog.data.gov/dataset/ncua-active-federally-insured-credit-unions-list-59c68

#CDFI list
#https://www.cdfifund.gov/sites/cdfi/files/2021-04/CDFI%20Cert%20List%2004-14-2021%20Final.xlsx

#Fintech List
#https://sites.google.com/view/fintech-and-shadow-banks


#Tradbank list
#https://sites.google.com/view/fintech-and-shadow-banks
#Top 25 list
#https://en.wikipedia.org/wiki/List_of_largest_banks_in_the_United_States


from fuzzywuzzy import process
import pandas as pd
import numpy as np
from datetime import datetime
from urllib.request import urlopen
import io
import zipfile


start = datetime.now()

#Name HMDA Data

url = "https://s3.amazonaws.com/cfpb-hmda-public/prod/one-year-data/2019/2019_public_ts_one_year_csv.zip"

#Import credit_union Bank data

file =zipfile.ZipFile((io.BytesIO(urlopen(url).read())))
file_name = file.namelist()[0]
HMDA_ts_2019 = pd.read_csv(file.open(file_name))

url = "https://s3.amazonaws.com/cfpb-hmda-public/prod/one-year-data/2020/2020_public_ts_one_year_csv.zip"

#Import credit_union Bank data

file =zipfile.ZipFile((io.BytesIO(urlopen(url).read())))
file_name = file.namelist()[0]
HMDA_ts_2020 = pd.read_csv(file.open(file_name))

url = "https://s3.amazonaws.com/cfpb-hmda-public/prod/one-year-data/2021/2021_public_ts_one_year_csv.zip"

#Import credit_union Bank data

file =zipfile.ZipFile((io.BytesIO(urlopen(url).read())))
file_name = file.namelist()[0]
HMDA_ts_2021 = pd.read_csv(file.open(file_name),
                           sep=',', 
                           on_bad_lines='skip')

url = "https://s3.amazonaws.com/cfpb-hmda-public/prod/snapshot-data/2022/2022_public_ts_csv.zip"

#Import credit_union Bank data

file =zipfile.ZipFile((io.BytesIO(urlopen(url).read())))
file_name = file.namelist()[0]
HMDA_ts_2022 = pd.read_csv(file.open(file_name),
                           sep=',', 
                           on_bad_lines='skip')

combined_hmda_ts = pd.concat([HMDA_ts_2019,
                              HMDA_ts_2020,
                              HMDA_ts_2021,
                              HMDA_ts_2022])
del(HMDA_ts_2019,
    HMDA_ts_2020,
    HMDA_ts_2021,
    HMDA_ts_2022,
    url,
    file,
    file_name)

combined_hmda_ts = combined_hmda_ts.reset_index() #reset rownames as they are based on which file they're frokm
combined_hmda_ts = combined_hmda_ts[combined_hmda_ts.columns[1:]] #Remove those rownames
#normalize HMDA data -- will do same procedure on other dataset to merge     
combined_hmda_ts['Name'] = combined_hmda_ts['respondent_name'].str.replace('[^\w\s]',
                                                        '',
                                                        regex=True) #remove punctuation
combined_hmda_ts['Name'] = combined_hmda_ts['Name'].str.replace(' ', 
                                                        '',
                                                        regex=True) #remove spaces

combined_hmda_ts['Name'] = combined_hmda_ts['Name'].apply(str.lower) #Convert all data to lowercase
combined_hmda_ts['Name'] = combined_hmda_ts['Name'].str.replace('association', 
                                                        'assn',
                                                        regex=True) #remove spaces
combined_hmda_ts['Name'] = combined_hmda_ts['Name'].str.replace('nationalassn', 
                                                        'na',
                                                        regex=True)
combined_hmda_ts['Name'] = combined_hmda_ts['Name'].str.replace('nationalassn', 
                                                        'na',
                                                        regex=True)
combined_hmda_ts['Name'] = combined_hmda_ts['Name'].str.replace('ntnlassn', 
                                                        'na',
                                                        regex=True)
combined_hmda_ts['Name'] = combined_hmda_ts['Name'].str.replace('bank', 
                                                        'bk',
                                                        regex=True)
combined_hmda_ts['Name'] = combined_hmda_ts['Name'].str.replace('creditunion', 
                                                        'cu',
                                                        regex=True)

combined_hmda_ts['City'] = combined_hmda_ts['respondent_city'].astype(str) #convert to string
combined_hmda_ts['City'] = combined_hmda_ts['City'].apply(str.lower) #Convert all data to lowercase
combined_hmda_ts['City'] = combined_hmda_ts['City'].str.replace('[^\w\s]', #remove Punctuation
                                                        '',
                                                        regex=True)

combined_hmda_ts['City'] = combined_hmda_ts['City'].str.replace(' ', 
                                                        '',
                                                        regex=True) #remove spaces
combined_hmda_ts['City'] = combined_hmda_ts['City'].str.replace('claremont', 
                                                        'la',
                                                        regex=True)
combined_hmda_ts['City'] = combined_hmda_ts['City'].str.replace('losangeles', 
                                                        'la',
                                                        regex=True)
combined_hmda_ts['City'] = combined_hmda_ts['City'].str.replace('edinburg',  #Texas national bank's city is mislabelled
                                                        'mercedes',
                                                        regex=True)



combined_hmda_ts['State'] = combined_hmda_ts['respondent_state'].astype(str) #convert to string
combined_hmda_ts['State'] = combined_hmda_ts['State'].apply(str.lower) #Convert all data to lowercase
combined_hmda_ts['State'] = combined_hmda_ts['State'].str.replace('[^\w\s]', #remove Punctuation
                                                          '',
                                                          regex=True)
combined_hmda_ts['State'] = combined_hmda_ts['State'].str.replace(' ', 
                                                          '',
                                                          regex=True) #remove spaces



#Name MDI Data link
historical_mdi_link = 'https://www.fdic.gov/regulations/resources/minority/mdi-history.xlsx'

#Import MDI Data
combined_mdi = pd.concat([pd.read_excel(historical_mdi_link,
                                            "2019",
                                            skiprows= 4,
                                            usecols = [1,2,3,8],
                                            names = ("Name",
                                                    "City",
                                                    "State",
                                                    "Minority Status")),
                          
                          pd.read_excel(historical_mdi_link,
                                            "2020",
                                            skiprows= 4,
                                            usecols = [1,2,3,8],
                                            names = ("Name",
                                                    "City",
                                                    "State",
                                                    "Minority Status")),
                         pd.read_excel(historical_mdi_link,
                                           "2021",
                                           skiprows= 4,
                                           usecols = [1,2,3,8],
                                           names = ("Name",
                                                   "City",
                                                   "State",
                                                   "Minority Status")),
                        pd.read_excel(historical_mdi_link,
                                            "2022",
                                            skiprows= 4,
                                            usecols = [1,2,3,8],
                                            names = ("Name",
                                                    "City",
                                                    "State",
                                                    "Minority Status"))                         
                          
                             ])
combined_mdi = combined_mdi.reset_index() #reset rownames as they are based on which file they're frokm
combined_mdi = combined_mdi[combined_mdi.columns[1:]] #Remove those rownames

#normalize MDI data -- will do same procedure on other dataset to merge
combined_mdi = combined_mdi.dropna() #Remove Missing Data 
    
    
combined_mdi['Name'] = combined_mdi['Name'].str.replace('[^\w\s]',
                                                        '',
                                                        regex=True) #remove punctuation
combined_mdi['Name'] = combined_mdi['Name'].str.replace(' ', 
                                                        '',
                                                        regex=True) #remove spaces

combined_mdi['Name'] = combined_mdi['Name'].apply(str.lower) #Convert all data to lowercase
combined_mdi['Name'] = combined_mdi['Name'].str.replace('association', 
                                                        'assn',
                                                        regex=True) #remove spaces
combined_mdi['Name'] = combined_mdi['Name'].str.replace('nationalassn', 
                                                        'na',
                                                        regex=True)
combined_mdi['Name'] = combined_mdi['Name'].str.replace('ntnlassn', 
                                                        'na',
                                                        regex=True)
combined_mdi['Name'] = combined_mdi['Name'].str.replace('bank', 
                                                        'bk',
                                                        regex=True)
combined_mdi['Name'] = combined_mdi['Name'].str.replace('creditunion', 
                                                        'cu',
                                                        regex=True)


combined_mdi['City'] = combined_mdi['City'].astype(str) #convert to string
combined_mdi['City'] = combined_mdi['City'].apply(str.lower) #Convert all data to lowercase
combined_mdi['City'] = combined_mdi['City'].str.replace('[^\w\s]', #remove Punctuation
                                                        '',
                                                        regex=True)
combined_mdi['City'] = combined_mdi['City'].str.replace(' ', 
                                                        '',
                                                        regex=True) #remove spaces
combined_mdi['City'] = combined_mdi['City'].str.replace('claremont', 
                                                        'la',
                                                        regex=True)
combined_mdi['City'] = combined_mdi['City'].str.replace('losangeles', 
                                                        'la',
                                                        regex=True)
combined_mdi['City'] = combined_mdi['City'].str.replace('edinburg', 
                                                        'mercedes',
                                                        regex=True)


combined_mdi['State'] = combined_mdi['State'].astype(str) #convert to string
combined_mdi['State'] = combined_mdi['State'].apply(str.lower) #Convert all data to lowercase
combined_mdi['State'] = combined_mdi['State'].str.replace('[^\w\s]', #remove Punctuation
                                                          '',
                                                          regex=True)
combined_mdi['State'] = combined_mdi['State'].str.replace(' ', 
                                                          '',
                                                          regex=True) #remove spaces
   
combined_mdi = combined_mdi.reset_index() #reset rownames as they are based on which file they're frokm
combined_mdi = combined_mdi[combined_mdi.columns[1:]] #Remove those rownames
combined_mdi = combined_mdi.drop_duplicates()
#####################################################
#####################################################
#####################################################

#Name credit_union data

url = "https://www.ncua.gov/files/publications/analysis/federally-insured-credit-union-list-march-2021.zip"

#Import credit_union Bank data

file =zipfile.ZipFile((io.BytesIO(urlopen(url).read())))
file_name = file.namelist()[0]
credit_union = pd.read_excel(file.open(file_name).read(), 
                               skiprows= range(0,2))  # <-- add .read()

credit_union = credit_union[['Credit Union name',
                                 'City (Mailing address)',
                                 'State (Mailing address)']]
credit_union = credit_union.rename(columns={'Credit Union name' : "BankName",
                            'City (Mailing address)' : "BankCity",
                            'State (Mailing address)' : "BankState"})

credit_union['Name'] = credit_union['BankName'].str.replace('[^\w\s]',
                                                        '',
                                                        regex=True) #remove punctuation
credit_union['Name'] = credit_union['Name'].str.replace(' ', 
                                                        '',
                                                        regex=True) #remove spaces

credit_union['Name'] = credit_union['Name'].apply(str.lower) #Convert all data to lowercase
credit_union['Name'] = credit_union['Name'].str.replace('association', 
                                                        'assn',
                                                        regex=True) #remove spaces
credit_union['Name'] = credit_union['Name'].str.replace('nationalassn', 
                                                        'na',
                                                        regex=True)
credit_union['Name'] = credit_union['Name'].str.replace('nationalassn', 
                                                        'na',
                                                        regex=True)
credit_union['Name'] = credit_union['Name'].str.replace('ntnlassn', 
                                                        'na',
                                                        regex=True)
credit_union['Name'] = credit_union['Name'].str.replace('bank', 
                                                        'bk',
                                                        regex=True)
credit_union['Name'] = credit_union['Name'].str.replace('creditunion', 
                                                        'cu',
                                                        regex=True)

credit_union['City'] = credit_union['BankCity'].astype(str) #convert to string
credit_union['City'] = credit_union['City'].apply(str.lower) #Convert all data to lowercase
credit_union['City'] = credit_union['City'].str.replace('[^\w\s]', #remove Punctuation
                                                        '',
                                                        regex=True)
credit_union['City'] = credit_union['City'].str.replace(' ', 
                                                        '',
                                                        regex=True) #remove spaces
credit_union['City'] = credit_union['City'].str.replace('claremont', 
                                                        'la',
                                                        regex=True)
credit_union['City'] = credit_union['City'].str.replace('losangeles', 
                                                        'la',
                                                        regex=True)

credit_union['City'] = credit_union['City'].str.replace('edinburg', 
                                                        'mercedes',
                                                        regex=True)

credit_union['State'] = credit_union['BankState'].astype(str) #convert to string
credit_union['State'] = credit_union['State'].apply(str.lower) #Convert all data to lowercase
credit_union['State'] = credit_union['State'].str.replace('[^\w\s]', #remove Punctuation
                                                          '',
                                                          regex=True)
credit_union['State'] = credit_union['State'].str.replace(' ', 
                                                          '',
                                                          regex=True) #remove spaces

#####################################################
#####################################################

#Name CDFI data

CDFI = "https://www.cdfifund.gov/sites/cdfi/files/2021-04/CDFI%20Cert%20List%2004-14-2021%20Final.xlsx"

#Import CDFI Bank data

CDFI = pd.read_excel(CDFI, 
                               skiprows= range(0,6))

CDFI = CDFI[['Organization Name',
                                 'City',
                                 'State']]
CDFI = CDFI.rename(columns={'Organization Name' : "BankName",
                            'City' : "BankCity",
                            'State' : "BankState"})

CDFI['Name'] = CDFI['BankName'].str.replace('[^\w\s]',
                                                        '',
                                                        regex=True) #remove punctuation
CDFI['Name'] = CDFI['Name'].str.replace(' ', 
                                                        '',
                                                        regex=True) #remove spaces

CDFI['Name'] = CDFI['Name'].apply(str.lower) #Convert all data to lowercase
CDFI['Name'] = CDFI['Name'].str.replace('association', 
                                                        'assn',
                                                        regex=True) #remove spaces
CDFI['Name'] = CDFI['Name'].str.replace('nationalassn', 
                                                        'na',
                                                        regex=True)
CDFI['Name'] = CDFI['Name'].str.replace('nationalassn', 
                                                        'na',
                                                        regex=True)
CDFI['Name'] = CDFI['Name'].str.replace('ntnlassn', 
                                                        'na',
                                                        regex=True)
CDFI['Name'] = CDFI['Name'].str.replace('bank', 
                                                        'bk',
                                                        regex=True)
CDFI['Name'] = CDFI['Name'].str.replace('creditunion', 
                                                        'cu',
                                                        regex=True)

CDFI['City'] = CDFI['BankCity'].astype(str) #convert to string
CDFI['City'] = CDFI['City'].apply(str.lower) #Convert all data to lowercase
CDFI['City'] = CDFI['City'].str.replace('[^\w\s]', #remove Punctuation
                                                        '',
                                                        regex=True)
CDFI['City'] = CDFI['City'].str.replace(' ', 
                                                        '',
                                                        regex=True) #remove spaces
CDFI['City'] = CDFI['City'].str.replace('claremont', 
                                                        'la',
                                                        regex=True)
CDFI['City'] = CDFI['City'].str.replace('losangeles', 
                                                        'la',
                                                        regex=True)

CDFI['City'] = CDFI['City'].str.replace('edinburg', 
                                                        'mercedes',
                                                        regex=True)

CDFI['State'] = CDFI['BankState'].astype(str) #convert to string
CDFI['State'] = CDFI['State'].apply(str.lower) #Convert all data to lowercase
CDFI['State'] = CDFI['State'].str.replace('[^\w\s]', #remove Punctuation
                                                          '',
                                                          regex=True)
CDFI['State'] = CDFI['State'].str.replace(' ', 
                                                          '',
                                                          regex=True) #remove spaces
#####################################################
#####################################################
#####################################################

#Name Community Bank data

community_bank = "https://www.fdic.gov/resources/community-banking/data/historical-community-banking-reference-data-2019-to-2023.zip"

#Import Community Bank data

community_bank = pd.read_csv(community_bank)
community_bank = community_bank[(community_bank['CB'] ==1)] 
community_bank = community_bank[(community_bank['Year'].isin([2019,
                                                              2020,
                                                              2021,
                                                              2022]))] 

community_bank = community_bank[['NameFull',
                                 'City',
                                 'Stalp',
                                 'Year']]
community_bank = community_bank.rename(columns={"City" : "BankCity",
                                                "Stalp" : "BankState",
                                                'NameFull' : "BankName",
                                                'Year' : 'activity_year'})

community_bank['Name'] = community_bank['BankName'].str.replace('[^\w\s]',
                                                        '',
                                                        regex=True) #remove punctuation
community_bank['Name'] = community_bank['Name'].str.replace(' ', 
                                                        '',
                                                        regex=True) #remove spaces

community_bank['Name'] = community_bank['Name'].apply(str.lower) #Convert all data to lowercase
community_bank['Name'] = community_bank['Name'].str.replace('association', 
                                                        'assn',
                                                        regex=True) #remove spaces
community_bank['Name'] = community_bank['Name'].str.replace('nationalassn', 
                                                        'na',
                                                        regex=True)
community_bank['Name'] = community_bank['Name'].str.replace('nationalassn', 
                                                        'na',
                                                        regex=True)
community_bank['Name'] = community_bank['Name'].str.replace('ntnlassn', 
                                                        'na',
                                                        regex=True)
community_bank['Name'] = community_bank['Name'].str.replace('bank', 
                                                        'bk',
                                                        regex=True)
community_bank['Name'] = community_bank['Name'].str.replace('creditunion', 
                                                        'cu',
                                                        regex=True)

community_bank['City'] = community_bank['BankCity'].astype(str) #convert to string
community_bank['City'] = community_bank['City'].apply(str.lower) #Convert all data to lowercase
community_bank['City'] = community_bank['City'].str.replace('[^\w\s]', #remove Punctuation
                                                        '',
                                                        regex=True)
community_bank['City'] = community_bank['City'].str.replace(' ', 
                                                        '',
                                                        regex=True) #remove spaces
community_bank['City'] = community_bank['City'].str.replace('claremont', 
                                                        'la',
                                                        regex=True)
community_bank['City'] = community_bank['City'].str.replace('losangeles', 
                                                        'la',
                                                        regex=True)
community_bank['City'] = community_bank['City'].str.replace('edinburg', 
                                                        'mercedes',
                                                        regex=True)



community_bank['State'] = community_bank['BankState'].astype(str) #convert to string
community_bank['State'] = community_bank['State'].apply(str.lower) #Convert all data to lowercase
community_bank['State'] = community_bank['State'].str.replace('[^\w\s]', #remove Punctuation
                                                          '',
                                                          regex=True)
community_bank['State'] = community_bank['State'].str.replace(' ', 
                                                          '',
                                                          regex=True) #remove spaces
#####################################################
#####################################################
#####################################################
#Define a fuzzy merge procedure

def fuzzy_merge(df_1, df_2, left_on, right_on, threshold, limit, matches):
    """
    :param df_1: the left table to join
    :param df_2: the right table to join
    :param left_on: key column of the left table
    :param right_on: key column of the right table
    :param threshold: how close the matches should be to return a match, based on Levenshtein distance
    :param limit: the amount of matches that will get returned, these are sorted high to low
    :return: dataframe with boths keys and matches
    """
   # c = list(df_1.columns) #get column names of first dataframe
    
    s = df_2[right_on].tolist() #Get vector of merging of second dataframe
    
    m = df_1[left_on].apply(lambda x: process.extract(x, s, limit=limit))  #merge vector of first dataframe with vector of second   
    
    df_1[matches] = m #Apply vector of matches to first dataframe
    m2 = df_1[matches].apply(lambda x: ', '.join([i[0] for i in x if i[1] >= threshold])) 
    df_1[matches] = m2
    return df_1
  
#####################################################
#####################################################
#####################################################
#Now try to fuzzy merge for MDI

combined_hmda_ts_banks = combined_hmda_ts[['Name',
                                     'lei']] #LEI is bank unique identifier

combined_hmda_ts_cities = combined_hmda_ts[['City',
                                     'lei']]

combined_hmda_ts_states = combined_hmda_ts[['State',
                                     'lei']]

combined_hmda_ts_banks = combined_hmda_ts_banks.drop_duplicates()
combined_hmda_ts_cities = combined_hmda_ts_cities.drop_duplicates()
combined_hmda_ts_states = combined_hmda_ts_states.drop_duplicates()

colnames_banks = list(combined_hmda_ts_banks.columns)
colnames_cities = list(combined_hmda_ts_cities.columns)
colnames_states = list(combined_hmda_ts_states.columns)

fuzzy_merge(combined_hmda_ts_banks,
            combined_mdi,
            left_on = 'Name',
            right_on = 'Name', 
            threshold = 90, 
            limit = 10000, 
            matches = "NameMatch")


fuzzy_merge(combined_hmda_ts_cities,
            combined_mdi,
            left_on = 'City',
            right_on = 'City', 
            threshold = 85, 
            limit = 200, 
            matches = "CityMatch")


fuzzy_merge(combined_hmda_ts_states,
            combined_mdi,
            left_on = 'State',
            right_on = 'State', 
            threshold = 90, 
            limit = 200, 
            matches = "StateMatch")


combined_hmda_ts_banks = combined_hmda_ts_banks.set_index(colnames_banks).apply(lambda x : x.str.split(',')).stack().apply(pd.Series).stack().unstack(level=2).reset_index(level=[0,1])
combined_hmda_ts_cities = combined_hmda_ts_cities.set_index(colnames_cities).apply(lambda x : x.str.split(',')).stack().apply(pd.Series).stack().unstack(level=2).reset_index(level=[0,1])
combined_hmda_ts_states = combined_hmda_ts_states.set_index(colnames_states).apply(lambda x : x.str.split(',')).stack().apply(pd.Series).stack().unstack(level=2).reset_index(level=[0,1])

combined_hmda_ts_banks['NameMatch'] = combined_hmda_ts_banks['NameMatch'].str.replace(' ', 
                                                                                    '',
                                                                                    regex=True) #remove spaces
combined_hmda_ts_cities['CityMatch'] = combined_hmda_ts_cities['CityMatch'].str.replace(' ', 
                                                                                    '',
                                                                                    regex=True) #remove space
combined_hmda_ts_states['StateMatch'] = combined_hmda_ts_states['StateMatch'].str.replace(' ', 
                                                                                    '',
                                                                                    regex=True) #remove spaces

combined_hmda_ts_banks = combined_hmda_ts_banks.drop_duplicates()
combined_hmda_ts_cities = combined_hmda_ts_cities.drop_duplicates()
combined_hmda_ts_states = combined_hmda_ts_states.drop_duplicates()

combined_hmda_ts_fuzzy_merged = pd.merge(combined_hmda_ts_banks,
                                combined_hmda_ts_cities,
                                how = 'inner')

combined_hmda_ts_fuzzy_merged = pd.merge(combined_hmda_ts_fuzzy_merged,
                                combined_hmda_ts_states,
                                how = 'inner')

combined_hmda_ts_fuzzy_merged = combined_hmda_ts_fuzzy_merged.replace(r'^\s*$', np.nan, regex=True)
combined_hmda_ts_fuzzy_merged = combined_hmda_ts_fuzzy_merged.dropna(subset = ['NameMatch',
                                                             'CityMatch',
                                                             'StateMatch'])
combined_hmda_ts_fuzzy_merged = combined_hmda_ts_fuzzy_merged.rename(columns={"Name" : "hmda name",
                                                                              "City" : "hmda city",
                                                                              "State" : "hmda state"})
combined_hmda_ts_mdi_fuzzy_merged =pd.merge(combined_mdi, 
                   combined_hmda_ts_fuzzy_merged, 
                   left_on= ['Name',
                             'City',
                             'State'], 
                   right_on = ['NameMatch',
                               'CityMatch',
                               'StateMatch'], 
                   how='inner')

combined_hmda_ts_mdi_fuzzy_merged = combined_hmda_ts_mdi_fuzzy_merged[['lei', 'Minority Status']]
combined_hmda_ts_mdi_fuzzy_merged = combined_hmda_ts_mdi_fuzzy_merged.drop_duplicates()

##########################################
#merge list of unique identifiers back into HMDA data

hmda_ts_mdi = pd.merge(combined_hmda_ts, combined_hmda_ts_mdi_fuzzy_merged)

#Get count of loan applications made to all MDIS make sure this matches below in LAR data
sum(hmda_ts_mdi['lar_count'])

##########################################################################################
##########################################################################################
#Now use that same data to get non_mdis
hmda_ts_non_mdi = pd.merge(combined_hmda_ts, combined_hmda_ts_mdi_fuzzy_merged,
                           how = "left",
                           indicator = True)

hmda_ts_non_mdi = hmda_ts_non_mdi[hmda_ts_non_mdi['_merge'] == 'left_only']

combined_hmda_ts_non_mdi_fuzzy_merged = hmda_ts_non_mdi[['lei']].drop_duplicates()

##########################################################################################
##########################################################################################
#Now do same merging for credit_unions 

combined_hmda_ts_banks = combined_hmda_ts[['Name',
                                     'lei']] #LEI is bank unique identifier

combined_hmda_ts_cities = combined_hmda_ts[['City',
                                     'lei']]

combined_hmda_ts_states = combined_hmda_ts[['State',
                                     'lei']]

combined_hmda_ts_banks = combined_hmda_ts_banks.drop_duplicates()
combined_hmda_ts_cities = combined_hmda_ts_cities.drop_duplicates()
combined_hmda_ts_states = combined_hmda_ts_states.drop_duplicates()

colnames_banks = list(combined_hmda_ts_banks.columns)
colnames_cities = list(combined_hmda_ts_cities.columns)
colnames_states = list(combined_hmda_ts_states.columns)

fuzzy_merge(combined_hmda_ts_banks,
            credit_union,
            left_on = 'Name',
            right_on = 'Name', 
            threshold = 90, 
            limit = 10000, 
            matches = "NameMatch")


fuzzy_merge(combined_hmda_ts_cities,
            credit_union,
            left_on = 'City',
            right_on = 'City', 
            threshold = 85, 
            limit = 200, 
            matches = "CityMatch")


fuzzy_merge(combined_hmda_ts_states,
            credit_union,
            left_on = 'State',
            right_on = 'State', 
            threshold = 90, 
            limit = 200, 
            matches = "StateMatch")


combined_hmda_ts_banks = combined_hmda_ts_banks.set_index(colnames_banks).apply(lambda x : x.str.split(',')).stack().apply(pd.Series).stack().unstack(level=2).reset_index(level=[0,1])
combined_hmda_ts_cities = combined_hmda_ts_cities.set_index(colnames_cities).apply(lambda x : x.str.split(',')).stack().apply(pd.Series).stack().unstack(level=2).reset_index(level=[0,1])
combined_hmda_ts_states = combined_hmda_ts_states.set_index(colnames_states).apply(lambda x : x.str.split(',')).stack().apply(pd.Series).stack().unstack(level=2).reset_index(level=[0,1])

combined_hmda_ts_banks['NameMatch'] = combined_hmda_ts_banks['NameMatch'].str.replace(' ', 
                                                                                    '',
                                                                                    regex=True) #remove spaces
combined_hmda_ts_cities['CityMatch'] = combined_hmda_ts_cities['CityMatch'].str.replace(' ', 
                                                                                    '',
                                                                                    regex=True) #remove space
combined_hmda_ts_states['StateMatch'] = combined_hmda_ts_states['StateMatch'].str.replace(' ', 
                                                                                    '',
                                                                                    regex=True) #remove spaces

combined_hmda_ts_banks = combined_hmda_ts_banks.drop_duplicates()
combined_hmda_ts_cities = combined_hmda_ts_cities.drop_duplicates()
combined_hmda_ts_states = combined_hmda_ts_states.drop_duplicates()

combined_hmda_ts_fuzzy_merged = pd.merge(combined_hmda_ts_banks,
                                combined_hmda_ts_cities,
                                how = 'inner')

combined_hmda_ts_fuzzy_merged = pd.merge(combined_hmda_ts_fuzzy_merged,
                                combined_hmda_ts_states,
                                how = 'inner')

combined_hmda_ts_fuzzy_merged = combined_hmda_ts_fuzzy_merged.replace(r'^\s*$', np.nan, regex=True)
combined_hmda_ts_fuzzy_merged = combined_hmda_ts_fuzzy_merged.dropna(subset = ['NameMatch',
                                                             'CityMatch',
                                                             'StateMatch'])
combined_hmda_ts_fuzzy_merged = combined_hmda_ts_fuzzy_merged.rename(columns={"Name" : "hmda name",
                                                                              "City" : "hmda city",
                                                                              "State" : "hmda state"})
combined_hmda_ts_credit_union_fuzzy_merged =pd.merge(credit_union, 
                   combined_hmda_ts_fuzzy_merged, 
                   left_on= ['Name',
                             'City',
                             'State'], 
                   right_on = ['NameMatch',
                               'CityMatch',
                               'StateMatch'], 
                   how='inner')

combined_hmda_ts_credit_union_fuzzy_merged = combined_hmda_ts_credit_union_fuzzy_merged[['lei']]
combined_hmda_ts_credit_union_fuzzy_merged = combined_hmda_ts_credit_union_fuzzy_merged.drop_duplicates()

##########################################
#merge list of unique identifiers back into HMDA data

hmda_ts_credit_union = pd.merge(combined_hmda_ts, combined_hmda_ts_credit_union_fuzzy_merged)

#Get count of loan applications made to all Community Bnaks make sure this matches below in LAR data
sum(hmda_ts_credit_union['lar_count'])
##########################################################################################
##########################################################################################
#Now do same merging for CDFIs 

combined_hmda_ts_banks = combined_hmda_ts[['Name',
                                     'lei']] #LEI is bank unique identifier

combined_hmda_ts_cities = combined_hmda_ts[['City',
                                     'lei']]

combined_hmda_ts_states = combined_hmda_ts[['State',
                                     'lei']]

combined_hmda_ts_banks = combined_hmda_ts_banks.drop_duplicates()
combined_hmda_ts_cities = combined_hmda_ts_cities.drop_duplicates()
combined_hmda_ts_states = combined_hmda_ts_states.drop_duplicates()

colnames_banks = list(combined_hmda_ts_banks.columns)
colnames_cities = list(combined_hmda_ts_cities.columns)
colnames_states = list(combined_hmda_ts_states.columns)

fuzzy_merge(combined_hmda_ts_banks,
            CDFI,
            left_on = 'Name',
            right_on = 'Name', 
            threshold = 90, 
            limit = 10000, 
            matches = "NameMatch")


fuzzy_merge(combined_hmda_ts_cities,
            CDFI,
            left_on = 'City',
            right_on = 'City', 
            threshold = 85, 
            limit = 200, 
            matches = "CityMatch")


fuzzy_merge(combined_hmda_ts_states,
            CDFI,
            left_on = 'State',
            right_on = 'State', 
            threshold = 90, 
            limit = 200, 
            matches = "StateMatch")


combined_hmda_ts_banks = combined_hmda_ts_banks.set_index(colnames_banks).apply(lambda x : x.str.split(',')).stack().apply(pd.Series).stack().unstack(level=2).reset_index(level=[0,1])
combined_hmda_ts_cities = combined_hmda_ts_cities.set_index(colnames_cities).apply(lambda x : x.str.split(',')).stack().apply(pd.Series).stack().unstack(level=2).reset_index(level=[0,1])
combined_hmda_ts_states = combined_hmda_ts_states.set_index(colnames_states).apply(lambda x : x.str.split(',')).stack().apply(pd.Series).stack().unstack(level=2).reset_index(level=[0,1])

combined_hmda_ts_banks['NameMatch'] = combined_hmda_ts_banks['NameMatch'].str.replace(' ', 
                                                                                    '',
                                                                                    regex=True) #remove spaces
combined_hmda_ts_cities['CityMatch'] = combined_hmda_ts_cities['CityMatch'].str.replace(' ', 
                                                                                    '',
                                                                                    regex=True) #remove space
combined_hmda_ts_states['StateMatch'] = combined_hmda_ts_states['StateMatch'].str.replace(' ', 
                                                                                    '',
                                                                                    regex=True) #remove spaces

combined_hmda_ts_banks = combined_hmda_ts_banks.drop_duplicates()
combined_hmda_ts_cities = combined_hmda_ts_cities.drop_duplicates()
combined_hmda_ts_states = combined_hmda_ts_states.drop_duplicates()

combined_hmda_ts_fuzzy_merged = pd.merge(combined_hmda_ts_banks,
                                combined_hmda_ts_cities,
                                how = 'inner')

combined_hmda_ts_fuzzy_merged = pd.merge(combined_hmda_ts_fuzzy_merged,
                                combined_hmda_ts_states,
                                how = 'inner')

combined_hmda_ts_fuzzy_merged = combined_hmda_ts_fuzzy_merged.replace(r'^\s*$', np.nan, regex=True)
combined_hmda_ts_fuzzy_merged = combined_hmda_ts_fuzzy_merged.dropna(subset = ['NameMatch',
                                                             'CityMatch',
                                                             'StateMatch'])
combined_hmda_ts_fuzzy_merged = combined_hmda_ts_fuzzy_merged.rename(columns={"Name" : "hmda name",
                                                                              "City" : "hmda city",
                                                                              "State" : "hmda state"})
combined_hmda_ts_CDFI_fuzzy_merged =pd.merge(CDFI, 
                   combined_hmda_ts_fuzzy_merged, 
                   left_on= ['Name',
                             'City',
                             'State'], 
                   right_on = ['NameMatch',
                               'CityMatch',
                               'StateMatch'], 
                   how='inner')

combined_hmda_ts_CDFI_fuzzy_merged = combined_hmda_ts_CDFI_fuzzy_merged[['lei']]
combined_hmda_ts_CDFI_fuzzy_merged = combined_hmda_ts_CDFI_fuzzy_merged.drop_duplicates()

##########################################
#merge list of unique identifiers back into HMDA data

hmda_ts_CDFI = pd.merge(combined_hmda_ts, combined_hmda_ts_CDFI_fuzzy_merged)

#Get count of loan applications made to all Community Bnaks make sure this matches below in LAR data
sum(hmda_ts_CDFI['lar_count'])

##########################################################################################
##########################################################################################
#Now do same merging for Community banks

combined_hmda_ts_banks = combined_hmda_ts[['Name',
                                     'lei']] #LEI is bank unique identifier

combined_hmda_ts_cities = combined_hmda_ts[['City',
                                     'lei']]

combined_hmda_ts_states = combined_hmda_ts[['State',
                                     'lei']]

combined_hmda_ts_banks = combined_hmda_ts_banks.drop_duplicates()
combined_hmda_ts_cities = combined_hmda_ts_cities.drop_duplicates()
combined_hmda_ts_states = combined_hmda_ts_states.drop_duplicates()

colnames_banks = list(combined_hmda_ts_banks.columns)
colnames_cities = list(combined_hmda_ts_cities.columns)
colnames_states = list(combined_hmda_ts_states.columns)

fuzzy_merge(combined_hmda_ts_banks,
            community_bank,
            left_on = 'Name',
            right_on = 'Name', 
            threshold = 90, 
            limit = 10000, 
            matches = "NameMatch")


fuzzy_merge(combined_hmda_ts_cities,
            community_bank,
            left_on = 'City',
            right_on = 'City', 
            threshold = 85, 
            limit = 200, 
            matches = "CityMatch")


fuzzy_merge(combined_hmda_ts_states,
            community_bank,
            left_on = 'State',
            right_on = 'State', 
            threshold = 90, 
            limit = 200, 
            matches = "StateMatch")


combined_hmda_ts_banks = combined_hmda_ts_banks.set_index(colnames_banks).apply(lambda x : x.str.split(',')).stack().apply(pd.Series).stack().unstack(level=2).reset_index(level=[0,1])
combined_hmda_ts_cities = combined_hmda_ts_cities.set_index(colnames_cities).apply(lambda x : x.str.split(',')).stack().apply(pd.Series).stack().unstack(level=2).reset_index(level=[0,1])
combined_hmda_ts_states = combined_hmda_ts_states.set_index(colnames_states).apply(lambda x : x.str.split(',')).stack().apply(pd.Series).stack().unstack(level=2).reset_index(level=[0,1])

combined_hmda_ts_banks['NameMatch'] = combined_hmda_ts_banks['NameMatch'].str.replace(' ', 
                                                                                    '',
                                                                                    regex=True) #remove spaces
combined_hmda_ts_cities['CityMatch'] = combined_hmda_ts_cities['CityMatch'].str.replace(' ', 
                                                                                    '',
                                                                                    regex=True) #remove space
combined_hmda_ts_states['StateMatch'] = combined_hmda_ts_states['StateMatch'].str.replace(' ', 
                                                                                    '',
                                                                                    regex=True) #remove spaces

combined_hmda_ts_banks = combined_hmda_ts_banks.drop_duplicates()
combined_hmda_ts_cities = combined_hmda_ts_cities.drop_duplicates()
combined_hmda_ts_states = combined_hmda_ts_states.drop_duplicates()

combined_hmda_ts_fuzzy_merged = pd.merge(combined_hmda_ts_banks,
                                combined_hmda_ts_cities,
                                how = 'inner')

combined_hmda_ts_fuzzy_merged = pd.merge(combined_hmda_ts_fuzzy_merged,
                                combined_hmda_ts_states,
                                how = 'inner')

combined_hmda_ts_fuzzy_merged = combined_hmda_ts_fuzzy_merged.replace(r'^\s*$', np.nan, regex=True)
combined_hmda_ts_fuzzy_merged = combined_hmda_ts_fuzzy_merged.dropna(subset = ['NameMatch',
                                                             'CityMatch',
                                                             'StateMatch'])
combined_hmda_ts_fuzzy_merged = combined_hmda_ts_fuzzy_merged.rename(columns={"Name" : "hmda name",
                                                                              "City" : "hmda city",
                                                                              "State" : "hmda state"})
combined_hmda_ts_community_fuzzy_merged =pd.merge(community_bank, 
                   combined_hmda_ts_fuzzy_merged, 
                   left_on= ['Name',
                             'City',
                             'State'], 
                   right_on = ['NameMatch',
                               'CityMatch',
                               'StateMatch'], 
                   how='inner')

combined_hmda_ts_community_fuzzy_merged = combined_hmda_ts_community_fuzzy_merged[['lei']]
combined_hmda_ts_community_fuzzy_merged = combined_hmda_ts_community_fuzzy_merged.drop_duplicates()

##########################################
#merge list of unique identifiers back into HMDA data

hmda_ts_community = pd.merge(combined_hmda_ts, combined_hmda_ts_community_fuzzy_merged)

#Get count of loan applications made to all Community Bnaks make sure this matches below in LAR data
sum(hmda_ts_community['lar_count'])

##########################################################################################
##########################################################################################
#Now for Fintechs
fintechs = "C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/6. Drafts/Lit Review/Lit Review HMDA.xlsx"

fintechs = pd.read_excel(fintechs,
                           sheet_name="Bushak fintechs")

hmda_ts_fintech = pd.merge(fintechs[['lei', 'Bank name']], combined_hmda_ts)

##########################################################################################
##########################################################################################
#We already have LEIs for the traditional banks 
trad_banks = "C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/6. Drafts/Lit Review/Lit Review HMDA.xlsx"

trad_banks = pd.read_excel(trad_banks,
                           sheet_name="Bushak trad banks")
hmda_ts_trad = pd.merge(trad_banks[['lei', 'Bank name']], combined_hmda_ts)
##########################################################################################
##########################################################################################
#We already have LEIs for the top 25 banks 
top25 = "C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/0. Data/Top25.csv"

top25 = pd.read_csv(top25)
hmda_ts_top25 = pd.merge(top25, combined_hmda_ts)
##########################################################################################
##########################################################################################

#Put these all in intermediate folder


hmda_ts_mdi.to_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/hmda_ts_mdi.csv")
hmda_ts_non_mdi.to_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/hmda_ts_non_mdi.csv")
hmda_ts_credit_union.to_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/hmda_ts_credit_union.csv")
hmda_ts_CDFI.to_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/hmda_ts_CDFI.csv")
hmda_ts_community.to_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/hmda_ts_community.csv")
hmda_ts_fintech.to_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/hmda_ts_fintech.csv")
hmda_ts_trad.to_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/hmda_ts_trad.csv")
hmda_ts_top25.to_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/hmda_ts_top25.csv")


end = datetime.now()
td = (end - start).total_seconds() /60
print(f"The time of execution of above program is : {td:.03f}m")
