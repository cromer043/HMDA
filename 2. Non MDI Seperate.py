# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 17:59:08 2024

@author: csromer
"""

import dask.dataframe as dd
import pandas as pd
import numpy as np

hmda_ts_non_mdi = pd.read_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/hmda_ts_non_mdi.csv",
                              usecols = ['lei',
                                      'activity_year', 
                                      'Minority Status'])
cols = [
    "lei",
    "activity_year",
    "census_tract",
    'county_code',
    'state_code',
    "action_taken",
    "loan_type",
    "loan_purpose",
    "loan_amount",
    'loan_term',
    "interest_rate",
    "total_loan_costs",
    "origination_charges",
    "property_value",
    "total_units",
    "income",
    "debt_to_income_ratio",
    "applicant_ethnicity_1",
    "applicant_race_1",
    "applicant_sex",
    'combined_loan_to_value_ratio',
    "applicant_age",
    "denial_reason_1",
    "denial_reason_2",
    "denial_reason_3",
    "denial_reason_4",
    "tract_population",
    "tract_minority_population_percent",
    "ffiec_msa_md_median_family_income",
    'tract_median_age_of_housing_units',
    "tract_to_msa_income_percentage",
    'occupancy_type',
    'lien_status',
    'co_applicant_sex',
    'co_applicant_sex_observed',
    'applicant_credit_score_type'
    ]

dtype = {'applicant_ethnicity_1': 'string',
         'county_code' : 'string',
       'applicant_race_1' : 'string',
       'census_tract': 'string',
       'co_applicant_ethnicity_1': 'string',
       'co_applicant_sex_observed': 'string',
       'combined_loan_to_value_ratio': 'string',
       'income': 'string',
       'interest_rate': 'string',
       'intro_rate_period': 'string',
       'loan_term': 'string',
       'tract_median_age_of_housing_units' :'string',
       'origination_charges': 'string',
       'prepayment_penalty_term': 'string',
       'property_value': 'string',
       'total_loan_costs': 'string',
       'total_units': 'string',
       'applicant_credit_score_type' : 'string'

       }
#Get data for loans
HMDA_lar_2019 = "C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/0. Data/2019_public_lar_one_year.csv"
HMDA_lar_2020 = "C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/0. Data/2020_public_lar_one_year.csv"
HMDA_lar_2021 = "C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/0. Data/2021_public_lar_one_year_csv.csv"
HMDA_lar_2022 = "C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/0. Data/2022_public_lar_csv.csv"


#Import HMDA Loan data
HMDA_lar_2019 = dd.read_csv(HMDA_lar_2019, 
                            usecols = cols,
                            dtype=dtype)
HMDA_lar_2020 = dd.read_csv(HMDA_lar_2020, 
                            usecols = cols,
                            dtype=dtype)
HMDA_lar_2021 = dd.read_csv(HMDA_lar_2021, 
                            usecols = cols,
                            dtype=dtype)
HMDA_lar_2022 = dd.read_csv(HMDA_lar_2022, 
                            usecols = cols,
                            dtype=dtype)

combined_hmda_lar = dd.concat([HMDA_lar_2019,
                              HMDA_lar_2020,
                              HMDA_lar_2021,
                              HMDA_lar_2022])
del(
    HMDA_lar_2019,
    HMDA_lar_2020,
    HMDA_lar_2021,
    HMDA_lar_2022, 
    dtype,
    cols
    )
combined_hmda_lar = combined_hmda_lar[combined_hmda_lar['occupancy_type'] == 1]
combined_hmda_lar = combined_hmda_lar[combined_hmda_lar['lien_status'] == 1]
combined_hmda_lar = combined_hmda_lar[combined_hmda_lar['total_units'].isin(['1', '2', '3', '4'])]
del(
    combined_hmda_lar['occupancy_type'],
    combined_hmda_lar['lien_status'],
    combined_hmda_lar['total_units']
    )

combined_hmda_non_mdi_lar = dd.merge(combined_hmda_lar, hmda_ts_non_mdi)
del(
    combined_hmda_lar, 
    hmda_ts_non_mdi
    )
combined_hmda_non_mdi_lar['applicant_race_1'] = dd.to_numeric(combined_hmda_non_mdi_lar['applicant_race_1'], errors='coerce').apply(np.floor).astype('float')
combined_hmda_non_mdi_lar['applicant_ethnicity_1'] = dd.to_numeric(combined_hmda_non_mdi_lar['applicant_ethnicity_1'], errors='coerce').apply(np.floor).astype('float')

combined_hmda_non_mdi_lar = combined_hmda_non_mdi_lar.compute()
combined_hmda_non_mdi_lar.to_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/combined_hmda_non_mdi_lar.csv")
