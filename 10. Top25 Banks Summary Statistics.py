# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 21:57:24 2024

@author: csromer
"""
import pandas as pd
import dask.dataframe as dd
import numpy as np
cols = ['lei',
        'activity_year',
        'census_tract',
        'action_taken',
        'loan_purpose',
        'loan_amount',
        'property_value',
        'interest_rate',
        'origination_charges',
        'applicant_race_1',
        'applicant_ethnicity_1',
        'tract_minority_population_percent',
        'tract_to_msa_income_percentage',
        'ffiec_msa_md_median_family_income',
        'tract_population',
        'income',
        'denial_reason_1',
        'denial_reason_2',
        'denial_reason_3',
        'denial_reason_4'
        ]
combined_hmda_top25_lar = dd.read_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/combined_hmda_top25_lar.csv",
                                     usecols = cols,
                                     dtype={'census_tract' : 'str',
                                            'interest_rate' : 'str',
                                            'origination_charges' : 'str',                                                
                                            'income' : 'str',
                                            'property_value' : 'str' })
hmda_ts_top25 = pd.read_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/hmda_ts_top25.csv")
#Climate Data 
#Data is in 2020 census whereas HMDA data is in 2010 census for 2019, 2020, 2021, and 2020 census for 2022
#Merging naturally on 2022
climate2022 = pd.read_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/0. Data/National_Risk_Index_Census_Tracts.csv",
                      usecols = ['TRACTFIPS',
                                 'RISK_SCORE',
                                 'RISK_RATNG'])
climate2022['activity_year'] = 2022
climate2022['RISK_RATNG'] = np.where(climate2022['RISK_RATNG'].isin(["Very High","Relatively High"]),
                                     1, 
                                     np.where(climate2022['RISK_RATNG'] == "Insufficient Data", 
                                              np.nan,
                                              0))
#Need crosswalk for 2019-2021

climate201920202021=  pd.read_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/0. Data/NRI_Table_CensusTracts.csv",
                      usecols = ['TRACTFIPS',
                                 'RISK_RATNG',
                                 'RISK_NPCTL'])
climate201920202021 = climate201920202021.rename(columns={"RISK_NPCTL": "RISK_SCORE"})

climate201920202021['RISK_RATNG'] = np.where(climate201920202021['RISK_RATNG'].isin(["Very High","Relatively High"]),
                                     1, 
                                     np.where(climate201920202021['RISK_RATNG'] == "Insufficient Data", 
                                              np.nan,
                                              0))
climate2019 = climate201920202021
climate2019['activity_year'] = 2019
climate = pd.concat([climate2019,                 
                    climate2022]
    )

climate2020 = climate201920202021
climate2020['activity_year'] = 2020

climate = pd.concat([climate,                 
                    climate2020]
    )

climate2021 = climate201920202021
climate2021['activity_year'] = 2021

climate = pd.concat([climate,                 
                    climate2021]
    )
climate['activity_year'].unique()
climate['census_tract'] = climate['TRACTFIPS'].astype('float')

combined_hmda_top25_lar['census_tract'] = combined_hmda_top25_lar['census_tract'].astype('float')
combined_hmda_top25_lar = dd.merge(combined_hmda_top25_lar,climate,
                 how = 'left',
                 indicator = True).compute()
values = ['Hispanic', 'American Indian or Alaska Native', 
          'Asian American or Pacific Islander', 'Black',
          "White", "Race not provided"]                                                
# create new columns for top25 banks and use np.select to assign values to it using our lists as arguments
conditions = [
    (combined_hmda_top25_lar['applicant_ethnicity_1'].isin([1,11,13,14])), #Hispanic codes
    (combined_hmda_top25_lar['applicant_race_1'] == 1), #AIAN codes
    (combined_hmda_top25_lar['applicant_race_1'].isin([2,21,22,23,24,25,26,27, #*AA*PI Codes
                                                             4,41,42,43,44])), #AA*PI* Codes
    (combined_hmda_top25_lar['applicant_race_1'] == 3), #Black code
    (combined_hmda_top25_lar['applicant_race_1'] == 5), #White code
    (combined_hmda_top25_lar['applicant_race_1'].isin([6,7]) | np.isnan(combined_hmda_top25_lar['applicant_race_1'])) #Missing codes
    ]

conditions2 = [
    (combined_hmda_top25_lar['action_taken'].isin([3,7])),
    (combined_hmda_top25_lar['action_taken'].isin([1,2,6,8])),
    (combined_hmda_top25_lar['action_taken'].isin([4,5]))
    ]

values2 = [1,0,np.nan]

combined_hmda_top25_lar['Race'] = np.select(conditions, values)
# create new columns for denial and use np.select to assign values to it using our lists as arguments

combined_hmda_top25_lar['Denial'] = np.select(conditions2, values2)
combined_hmda_top25_lar['income'] = pd.to_numeric(combined_hmda_top25_lar['income'], errors='coerce').astype('float')

combined_hmda_top25_lar['tract_income'] = combined_hmda_top25_lar['ffiec_msa_md_median_family_income'] * combined_hmda_top25_lar['tract_to_msa_income_percentage'] / 100
combined_hmda_top25_lar['tract_minority_pop'] = combined_hmda_top25_lar['tract_population'] * combined_hmda_top25_lar['tract_minority_population_percent'] / 100

conditions3 = [
    (combined_hmda_top25_lar['ffiec_msa_md_median_family_income']*.8 >= combined_hmda_top25_lar['income']*1000),
    (combined_hmda_top25_lar['ffiec_msa_md_median_family_income']*.8 < combined_hmda_top25_lar['income']*1000),
    (np.isnan(combined_hmda_top25_lar['income'])==True)
    ]
values3 = [1,0, np.isnan]
combined_hmda_top25_lar['lmi_borrower'] = pd.to_numeric(np.select(conditions3, values3), errors= 'coerce')
#Income Quantile
conditions4 = [
    (combined_hmda_top25_lar['income']*1000 <= 28007),#Brookings 20th percentile https://www.taxpolicycenter.org/statistics/household-income-quintiles
    (combined_hmda_top25_lar['income']*1000 <= 55000),#Brookings 40th percentile https://www.taxpolicycenter.org/statistics/household-income-quintiles
    (combined_hmda_top25_lar['income']*1000 <= 89744),#Brookings 60th percentile https://www.taxpolicycenter.org/statistics/household-income-quintiles
    (combined_hmda_top25_lar['income']*1000 <= 149131),#Brookings 80th percentile https://www.taxpolicycenter.org/statistics/household-income-quintiles
    (combined_hmda_top25_lar['income']*1000 > 149131),#Brookings 80th percentile https://www.taxpolicycenter.org/statistics/household-income-quintiles
    (np.isnan(combined_hmda_top25_lar['income'])==True)
    ]

values4 = ['0-20th income percentile',
           '20-40th',
           '40-60th',
           '60-80th',
           '80-100th',
           'Income data missing'
           ]
combined_hmda_top25_lar['Income_quantile'] = np.select(conditions4, values4)

combined_hmda_top25_lar['MajMin Indicator'] = np.where(combined_hmda_top25_lar['tract_minority_population_percent'] > 50,
                                                  1,
                                                  0)
combined_hmda_top25_lar['origination_charges'] = pd.to_numeric(combined_hmda_top25_lar['origination_charges'], 
                                                              errors='coerce')
combined_hmda_top25_lar['property_value'] = pd.to_numeric(combined_hmda_top25_lar['property_value'], 
                                                         errors='coerce')
combined_hmda_top25_lar['interest_rate'] = pd.to_numeric(combined_hmda_top25_lar['interest_rate'], 
                                                        errors='coerce')

combined_hmda_top25_lar['lmi_borrower']= np.where(combined_hmda_top25_lar['ffiec_msa_md_median_family_income']*.8 >= 
                                                 combined_hmda_top25_lar['income']*1000,
                                                  1,
                                                  0)
combined_hmda_top25_lar['Debt to income ratio'] = np.where((combined_hmda_top25_lar['denial_reason_1'] == 1) |(combined_hmda_top25_lar['denial_reason_2'] == 1)|(combined_hmda_top25_lar['denial_reason_3'] == 1)|(combined_hmda_top25_lar['denial_reason_4'] == 1),
1,
0)

combined_hmda_top25_lar['Employment history'] = np.where((combined_hmda_top25_lar['denial_reason_1'] == 2) |(combined_hmda_top25_lar['denial_reason_2'] == 2)|(combined_hmda_top25_lar['denial_reason_3'] == 2)|(combined_hmda_top25_lar['denial_reason_4'] == 2),
1,
0)

combined_hmda_top25_lar['Credit history'] = np.where((combined_hmda_top25_lar['denial_reason_1'] == 3 )|(combined_hmda_top25_lar['denial_reason_2'] == 3)|(combined_hmda_top25_lar['denial_reason_3'] == 3)|(combined_hmda_top25_lar['denial_reason_4'] == 3),
1,
0)
combined_hmda_top25_lar['Collateral'] = np.where((combined_hmda_top25_lar['denial_reason_1'] == 4) |(combined_hmda_top25_lar['denial_reason_2'] == 4)|(combined_hmda_top25_lar['denial_reason_3'] == 4)|(combined_hmda_top25_lar['denial_reason_4'] == 4),
1,
0)

combined_hmda_top25_lar['Insufficient cash'] = np.where((combined_hmda_top25_lar['denial_reason_1'] == 5) |(combined_hmda_top25_lar['denial_reason_2'] == 5)|(combined_hmda_top25_lar['denial_reason_3'] == 5)|(combined_hmda_top25_lar['denial_reason_4'] == 5),
1,
0)

combined_hmda_top25_lar['Mortgage insurance denied'] = np.where((combined_hmda_top25_lar['denial_reason_1'] == 8) |(combined_hmda_top25_lar['denial_reason_2'] == 8)|(combined_hmda_top25_lar['denial_reason_3'] == 8)|(combined_hmda_top25_lar['denial_reason_4'] == 8),
1,
0)
combined_hmda_top25_lar['DenialOther'] = np.where((combined_hmda_top25_lar['denial_reason_1'].isin([6,7,9,10])) |(combined_hmda_top25_lar['denial_reason_2'].isin([6,7,9,10]))|(combined_hmda_top25_lar['denial_reason_3'].isin([6,7,9,10]))|(combined_hmda_top25_lar['denial_reason_4'].isin([6,7,9,10])),
                                                             1,
                                                             0)
denied_loans = combined_hmda_top25_lar[combined_hmda_top25_lar['Denial'] == 1]
denied_loans = denied_loans[denied_loans['denial_reason_1'] != 1111]

##################################    
##################################
#By top25
#Summary statistics for 2. Data Output by top25

top25_loan_approved_and_taken = combined_hmda_top25_lar.loc[combined_hmda_top25_lar['action_taken'] == 1]

top25_loan_approved_and_taken = top25_loan_approved_and_taken.loc[top25_loan_approved_and_taken['loan_purpose'] == 1]

top25_loan_approved_and_taken['LMI Indicator'] = np.where(top25_loan_approved_and_taken['tract_to_msa_income_percentage'] < 80,
                                                            1,
                                                            0)
##################################
# Overall median loan dollars, loan numbers, and total loans
median_loan_dollars = top25_loan_approved_and_taken.groupby(['activity_year'])['loan_amount'].agg('median')
median_loan_dollars = median_loan_dollars.reset_index()
median_loan_dollars = median_loan_dollars.rename(columns = {'loan_amount': "Median loan"})
loan_numbers = top25_loan_approved_and_taken.groupby(['activity_year']).size()
loan_numbers = loan_numbers.reset_index()
loan_numbers = loan_numbers.rename(columns = {0: "Loans"})
loan_amounts = top25_loan_approved_and_taken.groupby(['activity_year'])['loan_amount'].agg('sum')
loan_amounts = loan_amounts.reset_index()  
loan_amounts = loan_amounts.rename(columns = {'loan_amount': "Total loan dollars"})

lmi_borrower = top25_loan_approved_and_taken.groupby(['activity_year'])['lmi_borrower'].mean()
lmi_borrower = lmi_borrower.reset_index()

Income_quantile = top25_loan_approved_and_taken.groupby(['activity_year', 'Income_quantile']).size()
Income_quantile = Income_quantile.reset_index()
Income_quantile = Income_quantile.pivot(index='activity_year', columns='Income_quantile', values=0)
Income_quantile = Income_quantile.reset_index()

percent_loans_maj_min = top25_loan_approved_and_taken.groupby(['activity_year'])['MajMin Indicator'].mean()
percent_loans_maj_min = percent_loans_maj_min.reset_index()

percent_loans_LMI= top25_loan_approved_and_taken.groupby(['activity_year'])['LMI Indicator'].mean()
percent_loans_LMI = percent_loans_LMI.reset_index()

origination_charges = top25_loan_approved_and_taken.groupby(['activity_year'])['origination_charges'].agg('median')
origination_charges = origination_charges.reset_index()
origination_charges = origination_charges.rename(columns = {'origination_charges': "Median Origination Fee"})

property_value = top25_loan_approved_and_taken.groupby(['activity_year'])['property_value'].agg('median')
property_value = property_value.reset_index()
property_value = property_value.rename(columns = {'property_value': "Median Property Value"})

interest_rate = top25_loan_approved_and_taken.groupby(['activity_year'])['interest_rate'].agg('median')
interest_rate = interest_rate.reset_index()
interest_rate = interest_rate.rename(columns = {'interest_rate': "Median Interest Rate"})


denial_rate = combined_hmda_top25_lar.groupby(['activity_year'])['Denial'].agg('mean')
denial_rate = denial_rate.reset_index()


denial_income = combined_hmda_top25_lar.groupby(['activity_year', 'Income_quantile',])['Denial'].agg('mean')
denial_income = denial_income.reset_index()
denial_income['Income_quantile'] = 'Denied: ' + denial_income['Income_quantile']
denial_income = denial_income.pivot(index=['activity_year'], columns='Income_quantile', values='Denial')
denial_income = denial_income.reset_index()


DRD2I = denied_loans.groupby(['activity_year'])['Debt to income ratio'].agg('mean')
DRD2I = DRD2I.reset_index()
DRD2I = DRD2I.rename(columns = {'Debt to income ratio': "DRD2I"})

DREH = denied_loans.groupby(['activity_year'])['Employment history'].agg('mean')
DREH = DREH.reset_index()
DREH = DREH.rename(columns = {'Employment history': "DREH"})

DRCH = denied_loans.groupby(['activity_year'])['Credit history'].agg('mean')
DRCH = DRCH.reset_index()
DRCH = DRCH.rename(columns = {'Credit history': "DRCH"})

DRCollat = denied_loans.groupby(['activity_year'])['Collateral'].agg('mean')
DRCollat = DRCollat.reset_index()
DRCollat = DRCollat.rename(columns = {'Collateral': "DRCollat"})

DRCash = denied_loans.groupby(['activity_year'])['Insufficient cash'].agg('mean')
DRCash = DRCash.reset_index()
DRCash = DRCash.rename(columns = {'Insufficient cash': 'DRCash'})

DRMID = denied_loans.groupby(['activity_year'])['Mortgage insurance denied'].agg('mean')
DRMID = DRMID.reset_index()
DRMID = DRMID.rename(columns = {'Mortgage insurance denied': 'DRMID'})

DRother = denied_loans.groupby(['activity_year'])['DenialOther'].agg('mean')
DRother = DRother.reset_index()
DRother = DRother.rename(columns = {'DenialOther': 'DRother'})

RISK_RATNG = combined_hmda_top25_lar.groupby(['activity_year'])['RISK_RATNG'].agg('mean')
RISK_RATNG = RISK_RATNG.reset_index()
RISK_RATNG = RISK_RATNG.rename(columns = {'RISK_RATNG': "Percent High Risk"})

RISK_SCORE = top25_loan_approved_and_taken[['census_tract', 
                                           'activity_year',
                                           'RISK_SCORE']].drop_duplicates()
RISK_SCORE =  RISK_SCORE.groupby(['activity_year'])['RISK_SCORE'].agg('median')
RISK_SCORE = RISK_SCORE.reset_index()
RISK_SCORE = RISK_SCORE.rename(columns = {'RISK_SCORE': "Median Climate Risk"})


overall_loans_top25 = pd.merge(loan_numbers,
                         pd.merge(Income_quantile,
                                  pd.merge(median_loan_dollars,
                                           pd.merge(loan_amounts,
                                  pd.merge(percent_loans_LMI, 
                                           pd.merge(percent_loans_maj_min, 
                                                    pd.merge(denial_rate,
                                                             pd.merge(origination_charges,
                                                                      pd.merge(property_value,
                                                                               pd.merge(interest_rate,
                                                                                        pd.merge(RISK_SCORE,
                                                                                                 pd.merge(RISK_RATNG, 
                                                                                                          pd.merge(lmi_borrower,
                                                                                                                   denial_income)))))))))))))
overall_loans_top25 = pd.merge(overall_loans_top25,DRD2I, how = 'left')
overall_loans_top25 = pd.merge(overall_loans_top25,DREH, how = 'left')
overall_loans_top25 = pd.merge(overall_loans_top25,DRCH, how = 'left')
overall_loans_top25 = pd.merge(overall_loans_top25,DRCollat, how = 'left')
overall_loans_top25 = pd.merge(overall_loans_top25,DRCash, how = 'left')
overall_loans_top25 = pd.merge(overall_loans_top25,DRMID, how = 'left')
overall_loans_top25 = pd.merge(overall_loans_top25,DRother, how = 'left')

overall_loans_top25 = overall_loans_top25.drop_duplicates()
overall_loans_top25 = overall_loans_top25.rename(columns={ 
                                              'activity_year' : "Year",
                                              'MajMin Indicator' : 'Percent majority minority',
                                              'LMI Indicator' : 'Percent LMI',
                                              'lmi_borrower' : 'LMI Borrower'})
overall_loans_top25 = overall_loans_top25[['Year',
                               "Loans",
                               "Total loan dollars",
                               "Median loan",
                               'LMI Borrower',
                               '0-20th income percentile',
                               '20-40th',
                               '40-60th',
                               '60-80th',
                               '80-100th',
                               'Income data missing',
                               'Median Origination Fee',
                               'Median Property Value',
                               'Median Interest Rate',
                               'Percent majority minority',
                               'Percent LMI',                               
                               'Median Climate Risk',
                               "Percent High Risk",
                               'Denial',
                                'Denied: 0-20th income percentile',
                                'Denied: 20-40th',
                                'Denied: 40-60th',
                                'Denied: 60-80th',
                                'Denied: 80-100th',
                                'Denied: Income data missing',
                               'DRD2I',
                               'DREH',
                               'DRCH',
                               'DRCollat',
                               'DRCash',
                               'DRMID',
                               'DRother'
                               ]]

with pd.ExcelWriter("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/2. Data Output/Summary Statistics.xlsx",
                    mode="a",
                    if_sheet_exists="replace") as writer:
    overall_loans_top25.to_excel(writer, sheet_name = "Overall top25 Banks") 

##################################
# By bank median loan dollars, loan numbers, and total loans
median_loan_dollars = top25_loan_approved_and_taken.groupby(['activity_year', 'lei'])['loan_amount'].agg('median')
median_loan_dollars = median_loan_dollars.reset_index()
median_loan_dollars = median_loan_dollars.rename(columns = {'loan_amount': "Median loan"})
loan_numbers = top25_loan_approved_and_taken.groupby(['activity_year', 'lei']).size()
loan_numbers = loan_numbers.reset_index()
loan_numbers = loan_numbers.rename(columns = {0: "Loans"})
loan_amounts = top25_loan_approved_and_taken.groupby(['activity_year', 'lei'])['loan_amount'].agg('sum')
loan_amounts = loan_amounts.reset_index()  
loan_amounts = loan_amounts.rename(columns = {'loan_amount': "Total loan dollars"})

lmi_borrower = top25_loan_approved_and_taken.groupby(['activity_year', 'lei'])['lmi_borrower'].mean()
lmi_borrower = lmi_borrower.reset_index()

Income_quantile = top25_loan_approved_and_taken.groupby(['activity_year', 'lei', 'Income_quantile']).size()
Income_quantile = Income_quantile.reset_index()
Income_quantile = Income_quantile.pivot(index=['activity_year', 'lei'], columns='Income_quantile', values=0)
Income_quantile = Income_quantile.reset_index()

percent_loans_maj_min = top25_loan_approved_and_taken.groupby(['activity_year', 'lei'])['MajMin Indicator'].mean()
percent_loans_maj_min = percent_loans_maj_min.reset_index()

percent_loans_LMI= top25_loan_approved_and_taken.groupby(['activity_year', 'lei'])['LMI Indicator'].mean()
percent_loans_LMI = percent_loans_LMI.reset_index()


origination_charges = top25_loan_approved_and_taken.groupby(['activity_year', 'lei'])['origination_charges'].agg('median')
origination_charges = origination_charges.reset_index()
origination_charges = origination_charges.rename(columns = {'origination_charges': "Median Origination Fee"})

property_value = top25_loan_approved_and_taken.groupby(['activity_year', 'lei'])['property_value'].agg('median')
property_value = property_value.reset_index()
property_value = property_value.rename(columns = {'property_value': "Median Property Value"})

interest_rate = top25_loan_approved_and_taken.groupby(['activity_year', 'lei'])['interest_rate'].agg('median')
interest_rate = interest_rate.reset_index()
interest_rate = interest_rate.rename(columns = {'interest_rate': "Median Interest Rate"})


denial_rate = combined_hmda_top25_lar.groupby(['activity_year', 'lei'])['Denial'].agg('mean')
denial_rate = denial_rate.reset_index()

denial_income = combined_hmda_top25_lar.groupby(['activity_year', 'lei', 'Income_quantile',])['Denial'].agg('mean')
denial_income = denial_income.reset_index()
denial_income['Income_quantile'] = 'Denied: ' + denial_income['Income_quantile']
denial_income = denial_income.pivot(index=['activity_year', 'lei'], columns='Income_quantile', values='Denial')
denial_income = denial_income.reset_index()

DRD2I = denied_loans.groupby(['activity_year', 'lei'])['Debt to income ratio'].agg('mean')
DRD2I = DRD2I.reset_index()
DRD2I = DRD2I.rename(columns = {'Debt to income ratio': "DRD2I"})

DREH = denied_loans.groupby(['activity_year', 'lei'])['Employment history'].agg('mean')
DREH = DREH.reset_index()
DREH = DREH.rename(columns = {'Employment history': "DREH"})

DRCH = denied_loans.groupby(['activity_year', 'lei'])['Credit history'].agg('mean')
DRCH = DRCH.reset_index()
DRCH = DRCH.rename(columns = {'Credit history': "DRCH"})

DRCollat = denied_loans.groupby(['activity_year', 'lei'])['Collateral'].agg('mean')
DRCollat = DRCollat.reset_index()
DRCollat = DRCollat.rename(columns = {'Collateral': "DRCollat"})

DRCash = denied_loans.groupby(['activity_year', 'lei'])['Insufficient cash'].agg('mean')
DRCash = DRCash.reset_index()
DRCash = DRCash.rename(columns = {'Insufficient cash': 'DRCash'})

DRMID = denied_loans.groupby(['activity_year', 'lei'])['Mortgage insurance denied'].agg('mean')
DRMID = DRMID.reset_index()
DRMID = DRMID.rename(columns = {'Mortgage insurance denied': 'DRMID'})

DRother = denied_loans.groupby(['activity_year','lei'])['DenialOther'].agg('mean')
DRother = DRother.reset_index()
DRother = DRother.rename(columns = {'DenialOther': 'DRother'})

RISK_RATNG = combined_hmda_top25_lar.groupby(['activity_year', 'lei'])['RISK_RATNG'].agg('mean')
RISK_RATNG = RISK_RATNG.reset_index()
RISK_RATNG = RISK_RATNG.rename(columns = {'RISK_RATNG': "Percent High Risk"})

RISK_SCORE = top25_loan_approved_and_taken[['census_tract', 
                                           'lei',
                                           'activity_year',
                                           'RISK_SCORE']].drop_duplicates()
RISK_SCORE =  RISK_SCORE.groupby(['activity_year', 'lei'])['RISK_SCORE'].agg('median')
RISK_SCORE = RISK_SCORE.reset_index()
RISK_SCORE = RISK_SCORE.rename(columns = {'RISK_SCORE': "Median Climate Risk"})

loans_by_bank_top25 = pd.merge(loan_numbers,
                         pd.merge(Income_quantile,
                                  pd.merge(median_loan_dollars,
                                           pd.merge(loan_amounts,
                                  pd.merge(percent_loans_LMI, 
                                           pd.merge(percent_loans_maj_min, 
                                                    pd.merge(denial_rate,
                                                             pd.merge(origination_charges,
                                                                      pd.merge(property_value,
                                                                               pd.merge(interest_rate,
                                                                                        pd.merge(RISK_SCORE,
                                                                                                 pd.merge(RISK_RATNG, 
                                                                                                          pd.merge(lmi_borrower,
                                                                                                                   denial_income)))))))))))))
loans_by_bank_top25 = pd.merge(loans_by_bank_top25,DRD2I, how = 'left')
loans_by_bank_top25 = pd.merge(loans_by_bank_top25,DREH, how = 'left')
loans_by_bank_top25 = pd.merge(loans_by_bank_top25,DRCH, how = 'left')
loans_by_bank_top25 = pd.merge(loans_by_bank_top25,DRCollat, how = 'left')
loans_by_bank_top25 = pd.merge(loans_by_bank_top25,DRCash, how = 'left')
loans_by_bank_top25 = pd.merge(loans_by_bank_top25,DRMID, how = 'left')
loans_by_bank_top25 = pd.merge(loans_by_bank_top25,DRother, how = 'left')


loans_by_bank_top25 = pd.merge(hmda_ts_top25,loans_by_bank_top25, how = "inner")

loans_by_bank_top25 = loans_by_bank_top25.rename(columns={ 'Bank name' : "Bank",
                                              'activity_year' : "Year",
                                              'MajMin Indicator' : 'Percent majority minority',
                                              'LMI Indicator' : 'Percent LMI',
                                              'lmi_borrower' : 'LMI Borrower'})

loans_by_bank_top25 = loans_by_bank_top25[['Bank',
                               'Year',
                               "Loans",
                               "Total loan dollars",
                               "Median loan",
                               'LMI Borrower',
                               '0-20th income percentile',
                               '20-40th',
                               '40-60th',
                               '60-80th',
                               '80-100th',
                               'Income data missing',
                               'Median Origination Fee',
                               'Median Property Value',
                               'Median Interest Rate',
                               'Percent majority minority',
                               'Percent LMI',
                               'Median Climate Risk',
                               "Percent High Risk",
                               'Denial',
                                'Denied: 0-20th income percentile',
                                'Denied: 20-40th',
                                'Denied: 40-60th',
                                'Denied: 60-80th',
                                'Denied: 80-100th',
                                'Denied: Income data missing',
                               'DRD2I',
                               'DREH',
                               'DRCH',
                               'DRCollat',
                               'DRCash',
                               'DRMID',
                               'DRother'
                               ]]
loans_by_bank_top25 = loans_by_bank_top25.drop_duplicates()


with pd.ExcelWriter("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/2. Data Output/Summary Statistics.xlsx",
                    mode="a",
                    if_sheet_exists="replace") as writer:
    loans_by_bank_top25.to_excel(writer, sheet_name = "By bank top25 banks") 



##################################
# By race of borrower median loan dollars, loan numbers, and total loans
median_loan_dollars = top25_loan_approved_and_taken.groupby(['activity_year', 'Race'])['loan_amount'].agg('median')
median_loan_dollars = median_loan_dollars.reset_index()
median_loan_dollars = median_loan_dollars.rename(columns = {'loan_amount': "Median loan"})
loan_numbers = top25_loan_approved_and_taken.groupby(['activity_year', 'Race']).size()
loan_numbers = loan_numbers.reset_index()
loan_numbers = loan_numbers.rename(columns = {0: "Loans"})
loan_amounts = top25_loan_approved_and_taken.groupby(['activity_year', 'Race'])['loan_amount'].agg('sum')
loan_amounts = loan_amounts.reset_index()  
loan_amounts = loan_amounts.rename(columns = {'loan_amount': "Total loan dollars"})

lmi_borrower = top25_loan_approved_and_taken.groupby(['activity_year', 'Race'])['lmi_borrower'].mean()
lmi_borrower = lmi_borrower.reset_index()

Income_quantile = top25_loan_approved_and_taken.groupby(['activity_year', 'Race', 'Income_quantile']).size()
Income_quantile = Income_quantile.reset_index()
Income_quantile = Income_quantile.pivot(index=['activity_year', 'Race'], columns='Income_quantile', values=0)
Income_quantile = Income_quantile.reset_index()


percent_loans_maj_min = top25_loan_approved_and_taken.groupby(['activity_year', 'Race'])['MajMin Indicator'].mean()
percent_loans_maj_min = percent_loans_maj_min.reset_index()

percent_loans_LMI= top25_loan_approved_and_taken.groupby(['activity_year', 'Race'])['LMI Indicator'].mean()
percent_loans_LMI = percent_loans_LMI.reset_index()

origination_charges = top25_loan_approved_and_taken.groupby(['activity_year', 'Race'])['origination_charges'].agg('median')
origination_charges = origination_charges.reset_index()
origination_charges = origination_charges.rename(columns = {'origination_charges': "Median Origination Fee"})

property_value = top25_loan_approved_and_taken.groupby(['activity_year', 'Race'])['property_value'].agg('median')
property_value = property_value.reset_index()
property_value = property_value.rename(columns = {'property_value': "Median Property Value"})

interest_rate = top25_loan_approved_and_taken.groupby(['activity_year', 'Race'])['interest_rate'].agg('median')
interest_rate = interest_rate.reset_index()
interest_rate = interest_rate.rename(columns = {'interest_rate': "Median Interest Rate"})



denial_rate = combined_hmda_top25_lar.groupby(['activity_year', 'Race'])['Denial'].agg('mean')
denial_rate = denial_rate.reset_index()


denial_income = combined_hmda_top25_lar.groupby(['activity_year', 'Race', 'Income_quantile',])['Denial'].agg('mean')
denial_income = denial_income.reset_index()
denial_income['Income_quantile'] = 'Denied: ' + denial_income['Income_quantile']
denial_income = denial_income.pivot(index=['activity_year', 'Race'], columns='Income_quantile', values='Denial')
denial_income = denial_income.reset_index()

DRD2I = denied_loans.groupby(['activity_year', 'Race'])['Debt to income ratio'].agg('mean')
DRD2I = DRD2I.reset_index()
DRD2I = DRD2I.rename(columns = {'Debt to income ratio': "DRD2I"})

DREH = denied_loans.groupby(['activity_year', 'Race'])['Employment history'].agg('mean')
DREH = DREH.reset_index()
DREH = DREH.rename(columns = {'Employment history': "DREH"})

DRCH = denied_loans.groupby(['activity_year', 'Race'])['Credit history'].agg('mean')
DRCH = DRCH.reset_index()
DRCH = DRCH.rename(columns = {'Credit history': "DRCH"})

DRCollat = denied_loans.groupby(['activity_year', 'Race'])['Collateral'].agg('mean')
DRCollat = DRCollat.reset_index()
DRCollat = DRCollat.rename(columns = {'Collateral': "DRCollat"})

DRCash = denied_loans.groupby(['activity_year', 'Race'])['Insufficient cash'].agg('mean')
DRCash = DRCash.reset_index()
DRCash = DRCash.rename(columns = {'Insufficient cash': 'DRCash'})

DRMID = denied_loans.groupby(['activity_year', 'Race'])['Mortgage insurance denied'].agg('mean')
DRMID = DRMID.reset_index()
DRMID = DRMID.rename(columns = {'Mortgage insurance denied': 'DRMID'})

DRother = denied_loans.groupby(['activity_year','Race'])['DenialOther'].agg('mean')
DRother = DRother.reset_index()
DRother = DRother.rename(columns = {'DenialOther': 'DRother'})

RISK_RATNG = combined_hmda_top25_lar.groupby(['activity_year', 'Race'])['RISK_RATNG'].agg('mean')
RISK_RATNG = RISK_RATNG.reset_index()
RISK_RATNG = RISK_RATNG.rename(columns = {'RISK_RATNG': "Percent High Risk"})

RISK_SCORE = top25_loan_approved_and_taken[['census_tract', 
                                           'Race',
                                           'activity_year',
                                           'RISK_SCORE']].drop_duplicates()
RISK_SCORE =  RISK_SCORE.groupby(['activity_year', 'Race'])['RISK_SCORE'].agg('median')
RISK_SCORE = RISK_SCORE.reset_index()
RISK_SCORE = RISK_SCORE.rename(columns = {'RISK_SCORE': "Median Climate Risk"})

loans_by_race_top25 = pd.merge(loan_numbers,
                         pd.merge(Income_quantile,
                                  pd.merge(median_loan_dollars,
                                           pd.merge(loan_amounts,
                                  pd.merge(percent_loans_LMI, 
                                           pd.merge(percent_loans_maj_min, 
                                                    pd.merge(denial_rate,
                                                             pd.merge(origination_charges,
                                                                      pd.merge(property_value,
                                                                               pd.merge(interest_rate,
                                                                                        pd.merge(RISK_SCORE,
                                                                                                 pd.merge(RISK_RATNG, 
                                                                                                          pd.merge(lmi_borrower,
                                                                                                                   denial_income)))))))))))))
loans_by_race_top25 = pd.merge(loans_by_race_top25,DRD2I, how = 'left')
loans_by_race_top25 = pd.merge(loans_by_race_top25,DREH, how = 'left')
loans_by_race_top25 = pd.merge(loans_by_race_top25,DRCH, how = 'left')
loans_by_race_top25 = pd.merge(loans_by_race_top25,DRCollat, how = 'left')
loans_by_race_top25 = pd.merge(loans_by_race_top25,DRCash, how = 'left')
loans_by_race_top25 = pd.merge(loans_by_race_top25,DRMID, how = 'left')
loans_by_race_top25 = pd.merge(loans_by_race_top25,DRother, how = 'left')

loans_by_race_top25 = loans_by_race_top25.rename(columns={'activity_year' : "Year",
                                              'MajMin Indicator' : 'Percent majority minority',
                                              'LMI Indicator' : 'Percent LMI',
                                              'lmi_borrower' : 'LMI Borrower'})
loans_by_race_top25 = loans_by_race_top25[['Race',
                               'Year',
                               "Loans",
                               "Total loan dollars",
                               "Median loan",
                               'LMI Borrower',
                               '0-20th income percentile',
                               '20-40th',
                               '40-60th',
                               '60-80th',
                               '80-100th',
                               'Income data missing',
                               'Median Origination Fee',
                               'Median Property Value',
                               'Median Interest Rate',
                               'Percent majority minority',
                               'Percent LMI',
                               'Median Climate Risk',
                               "Percent High Risk",
                               'Denial',
                                'Denied: 0-20th income percentile',
                                'Denied: 20-40th',
                                'Denied: 40-60th',
                                'Denied: 60-80th',
                                'Denied: 80-100th',
                                'Denied: Income data missing',
                               'DRD2I',
                               'DREH',
                               'DRCH',
                               'DRCollat',
                               'DRCash',
                               'DRMID',
                               'DRother'
                               ]]
loans_by_race_top25 = loans_by_race_top25.drop_duplicates()

with pd.ExcelWriter("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/2. Data Output/Summary Statistics.xlsx",
                    mode="a",
                    if_sheet_exists="replace") as writer:
    loans_by_race_top25.to_excel(writer, sheet_name = "By race top25 bank")  