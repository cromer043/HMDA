# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 15:00:52 2024

@author: csromer
"""
#02.06.24 #Seperating the fuzzy matching in the first phase from the second phase of matching to individual loans

import dask.dataframe as dd
import pandas as pd
import numpy as np

cols = [
    "lei",
    "activity_year",
    "state_code",
    "county_code",
    "census_tract",
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
    'combined_loan_to_value_ratio',
    "debt_to_income_ratio",
    "applicant_ethnicity_1",
    "applicant_race_1",
    "applicant_sex",
    "applicant_age",
    "denial_reason_1",
    "denial_reason_2",
    "denial_reason_3",
    "denial_reason_4",
    "tract_population",
    "tract_minority_population_percent",
    'tract_median_age_of_housing_units',
    "ffiec_msa_md_median_family_income",
    "tract_to_msa_income_percentage",
    'occupancy_type',
    'lien_status',
    'co_applicant_sex',
    'co_applicant_sex_observed',
    'applicant_credit_score_type'

    

    ]

dtype = {'applicant_ethnicity_1': 'string',
       'applicant_race_1' : 'string',
       'applicant_age' : 'str',

       'census_tract': 'string',
       'co_applicant_sex': 'string',
       'co_applicant_sex_observed': 'string',
       'combined_loan_to_value_ratio': 'string',
       'county_code': 'string',
       'discount_points': 'string',
       'income': 'string',
       'interest_rate': 'string',
       'intro_rate_period': 'string',
       'lender_credits': 'string',
       'loan_term': 'string',
       'multifamily_affordable_units': 'string',
       'tract_median_age_of_housing_units' :'string',
       'origination_charges': 'string',
       'prepayment_penalty_term': 'string',
       'property_value': 'string',
       'rate_spread': 'string',
       'total_loan_costs': 'string',
       'total_points_and_fees': 'string',
       'total_units': 'string',
       'applicant_credit_score_type' : 'string'
       }

hmda_ts_mdi = dd.read_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/hmda_ts_mdi.csv")
hmda_ts_CDFI = dd.read_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/hmda_ts_CDFI.csv")
hmda_ts_credit_union = dd.read_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/hmda_ts_credit_union.csv")
hmda_ts_community = dd.read_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/hmda_ts_community.csv")
hmda_ts_fintech = dd.read_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/hmda_ts_fintech.csv")
hmda_ts_trad = dd.read_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/hmda_ts_trad.csv")
hmda_ts_top25 = dd.read_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/hmda_ts_top25.csv")

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
                            dtype= dtype)

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
del(HMDA_lar_2019,
    HMDA_lar_2020,
    HMDA_lar_2021,
    HMDA_lar_2022,
    dtype,
    cols)

combined_hmda_mdi_lar =  dd.merge(combined_hmda_lar, hmda_ts_mdi[['lei', 'activity_year','Minority Status']]).compute()
combined_hmda_mdi_lar['applicant_race_1'] = pd.to_numeric(combined_hmda_mdi_lar['applicant_race_1'], errors='coerce').apply(np.floor).astype('float')
combined_hmda_mdi_lar['applicant_ethnicity_1'] = pd.to_numeric(combined_hmda_mdi_lar['applicant_ethnicity_1'], errors='coerce').apply(np.floor).astype('float')
combined_hmda_mdi_lar.to_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/combined_hmda_mdi_lar.csv")
del(hmda_ts_mdi)
del(combined_hmda_mdi_lar)


combined_hmda_lar = combined_hmda_lar[combined_hmda_lar['occupancy_type'] == 1]
combined_hmda_lar = combined_hmda_lar[combined_hmda_lar['lien_status'] == 1]
combined_hmda_lar = combined_hmda_lar[combined_hmda_lar['total_units'].isin(['1', '2', '3', '4'])]
del(combined_hmda_lar['occupancy_type'],
    combined_hmda_lar['lien_status'],
    combined_hmda_lar['total_units'])



combined_hmda_CDFI_lar =  dd.merge(combined_hmda_lar, hmda_ts_CDFI[['lei', 'activity_year']]).compute()
combined_hmda_CDFI_lar['applicant_race_1'] = pd.to_numeric(combined_hmda_CDFI_lar['applicant_race_1'], errors='coerce').apply(np.floor).astype('float')
combined_hmda_CDFI_lar['applicant_ethnicity_1'] = pd.to_numeric(combined_hmda_CDFI_lar['applicant_ethnicity_1'], errors='coerce').apply(np.floor).astype('float')
combined_hmda_CDFI_lar.to_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/combined_hmda_CDFI_lar.csv")
del(combined_hmda_CDFI_lar)
del(hmda_ts_CDFI)

combined_hmda_credit_union_lar =  dd.merge(combined_hmda_lar, hmda_ts_credit_union[['lei', 'activity_year']]).compute()
combined_hmda_credit_union_lar['applicant_race_1'] = pd.to_numeric(combined_hmda_credit_union_lar['applicant_race_1'], errors='coerce').apply(np.floor).astype('float')
combined_hmda_credit_union_lar['applicant_ethnicity_1'] = pd.to_numeric(combined_hmda_credit_union_lar['applicant_ethnicity_1'], errors='coerce').apply(np.floor).astype('float')
combined_hmda_credit_union_lar.to_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/combined_hmda_credit_union_lar.csv")
del(combined_hmda_credit_union_lar)
del(hmda_ts_credit_union)

combined_hmda_community_lar =  dd.merge(combined_hmda_lar, hmda_ts_community[['lei', 'activity_year']]).compute()
combined_hmda_community_lar['applicant_race_1'] = pd.to_numeric(combined_hmda_community_lar['applicant_race_1'], errors='coerce').apply(np.floor).astype('float')
combined_hmda_community_lar['applicant_ethnicity_1'] = pd.to_numeric(combined_hmda_community_lar['applicant_ethnicity_1'], errors='coerce').apply(np.floor).astype('float')
combined_hmda_community_lar.to_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/combined_hmda_community_lar.csv")
del(combined_hmda_community_lar)
del(hmda_ts_community)

combined_hmda_fintech_lar =  dd.merge(combined_hmda_lar, hmda_ts_fintech[['lei', 'activity_year']]).compute()
combined_hmda_fintech_lar['applicant_race_1'] = pd.to_numeric(combined_hmda_fintech_lar['applicant_race_1'], errors='coerce').apply(np.floor).astype('float')
combined_hmda_fintech_lar['applicant_ethnicity_1'] = pd.to_numeric(combined_hmda_fintech_lar['applicant_ethnicity_1'], errors='coerce').apply(np.floor).astype('float')
combined_hmda_fintech_lar.to_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/combined_hmda_fintech_lar.csv")
del(combined_hmda_fintech_lar)
del(hmda_ts_fintech)


combined_hmda_top25_lar =  dd.merge(combined_hmda_lar, hmda_ts_top25[['lei', 'activity_year']]).compute()
combined_hmda_top25_lar['applicant_race_1'] = pd.to_numeric(combined_hmda_top25_lar['applicant_race_1'], errors='coerce').apply(np.floor).astype('float')
combined_hmda_top25_lar['applicant_ethnicity_1'] = pd.to_numeric(combined_hmda_top25_lar['applicant_ethnicity_1'], errors='coerce').apply(np.floor).astype('float')
combined_hmda_top25_lar.to_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/combined_hmda_top25_lar.csv")
del(combined_hmda_top25_lar)
del(hmda_ts_top25)


combined_hmda_trad_lar =  dd.merge(combined_hmda_lar, hmda_ts_trad[['lei', 'activity_year']]).compute()
combined_hmda_trad_lar['applicant_race_1'] = pd.to_numeric(combined_hmda_trad_lar['applicant_race_1'], errors='coerce').apply(np.floor).astype('float')
combined_hmda_trad_lar['applicant_ethnicity_1'] = pd.to_numeric(combined_hmda_trad_lar['applicant_ethnicity_1'], errors='coerce').apply(np.floor).astype('float')
combined_hmda_trad_lar.to_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/combined_hmda_trad_lar.csv")
del(combined_hmda_trad_lar)
del(hmda_ts_trad)
