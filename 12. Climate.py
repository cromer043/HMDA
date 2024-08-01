# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 10:04:08 2024

@author: csromer
"""
#Climate data
#https://resilience.climate.gov/datasets/FEMA::national-risk-index-census-tracts/about
#Import necessary data tools
import pandas as pd
import numpy as np
from scipy import stats
import dask.dataframe as dd
#Import data
###################################################
cols = ['lei',
        'activity_year',
        'census_tract',
        'action_taken',
        'loan_purpose'
        ]

combined_hmda_mdi_lar = dd.read_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/combined_hmda_mdi_lar.csv",
                                    usecols= cols,
                                    dtype={'census_tract' : 'str'})

combined_hmda_non_mdi_lar = dd.read_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/combined_hmda_non_mdi_lar.csv",
                                        usecols = cols,
                                        dtype={'census_tract' : 'str'})

combined_hmda_CDFI_lar = dd.read_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/combined_hmda_CDFI_lar.csv",
                                     usecols= cols,
                                     dtype={'census_tract' : 'str'})

combined_hmda_community_lar = dd.read_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/combined_hmda_community_lar.csv",
                                          usecols= cols,
                                          dtype={'census_tract' : 'str'})

combined_hmda_top25_lar = dd.read_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/combined_hmda_top25_lar.csv",
                                     usecols= cols,
                                     dtype={'census_tract' : 'str'})

combined_hmda_fintech_lar = dd.read_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/combined_hmda_fintech_lar.csv",
                                        usecols= cols,
                                        dtype={'census_tract' : 'str'})

combined_hmda_credit_union_lar = dd.read_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/combined_hmda_credit_union_lar.csv",
                                     usecols= cols,
                                     dtype={'census_tract' : 'str'})
combined_hmda_mdi_lar = combined_hmda_mdi_lar[combined_hmda_mdi_lar['action_taken']==1]
combined_hmda_mdi_lar = combined_hmda_mdi_lar[combined_hmda_mdi_lar['loan_purpose'] == 1]
combined_hmda_mdi_lar = combined_hmda_mdi_lar[combined_hmda_mdi_lar['activity_year']==2022].compute()
combined_hmda_mdi_lar['TRACTFIPS'] = pd.to_numeric(combined_hmda_mdi_lar['census_tract'], errors='coerce')

combined_hmda_non_mdi_lar = combined_hmda_non_mdi_lar[combined_hmda_non_mdi_lar['action_taken']==1]
combined_hmda_non_mdi_lar = combined_hmda_non_mdi_lar[combined_hmda_non_mdi_lar['loan_purpose'] == 1]
combined_hmda_non_mdi_lar = combined_hmda_non_mdi_lar[combined_hmda_non_mdi_lar['activity_year']==2022].compute()
combined_hmda_non_mdi_lar['TRACTFIPS'] = pd.to_numeric(combined_hmda_non_mdi_lar['census_tract'], errors='coerce')

combined_hmda_CDFI_lar = combined_hmda_CDFI_lar[combined_hmda_CDFI_lar['action_taken']==1]
combined_hmda_CDFI_lar = combined_hmda_CDFI_lar[combined_hmda_CDFI_lar['loan_purpose'] == 1]
combined_hmda_CDFI_lar = combined_hmda_CDFI_lar[combined_hmda_CDFI_lar['activity_year']==2022].compute()
combined_hmda_CDFI_lar['TRACTFIPS'] = pd.to_numeric(combined_hmda_CDFI_lar['census_tract'], errors='coerce')

combined_hmda_community_lar = combined_hmda_community_lar[combined_hmda_community_lar['action_taken']==1]
combined_hmda_community_lar = combined_hmda_community_lar[combined_hmda_community_lar['loan_purpose'] == 1]
combined_hmda_community_lar = combined_hmda_community_lar[combined_hmda_community_lar['action_taken']==1].compute()
combined_hmda_community_lar['TRACTFIPS'] = pd.to_numeric(combined_hmda_community_lar['census_tract'], errors='coerce')

combined_hmda_top25_lar = combined_hmda_top25_lar[combined_hmda_top25_lar['action_taken']==1]
combined_hmda_top25_lar = combined_hmda_top25_lar[combined_hmda_top25_lar['loan_purpose'] == 1]
combined_hmda_top25_lar = combined_hmda_top25_lar[combined_hmda_top25_lar['activity_year']==2022].compute()
combined_hmda_top25_lar['TRACTFIPS'] = pd.to_numeric(combined_hmda_top25_lar['census_tract'], errors='coerce')

combined_hmda_fintech_lar = combined_hmda_fintech_lar[combined_hmda_fintech_lar['action_taken']==1]
combined_hmda_fintech_lar = combined_hmda_fintech_lar[combined_hmda_fintech_lar['loan_purpose'] == 1]
combined_hmda_fintech_lar = combined_hmda_fintech_lar[combined_hmda_fintech_lar['activity_year']==2022].compute()
combined_hmda_fintech_lar['TRACTFIPS'] = pd.to_numeric(combined_hmda_fintech_lar['census_tract'], errors='coerce')


combined_hmda_credit_union_lar = combined_hmda_credit_union_lar[combined_hmda_credit_union_lar['action_taken']==1]
combined_hmda_credit_union_lar = combined_hmda_credit_union_lar[combined_hmda_credit_union_lar['loan_purpose'] == 1]
combined_hmda_credit_union_lar = combined_hmda_credit_union_lar[combined_hmda_credit_union_lar['activity_year']==2022].compute()
combined_hmda_credit_union_lar['TRACTFIPS'] = pd.to_numeric(combined_hmda_credit_union_lar['census_tract'], errors='coerce')

#Climate Data 
#Data is in 2020 census whereas HMDA data is in 2010 census for 2019, 2020, 2021, and 2020 census for 2022
#Merging naturally on 2022
climate2022 = pd.read_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/0. Data/National_Risk_Index_Census_Tracts.csv",
                      usecols = ['TRACTFIPS',
                                 'RISK_SCORE'],
                                 dtype={'TRACTFIPS' : 'str'})
climate2022['TRACTFIPS'] = pd.to_numeric(climate2022['TRACTFIPS'], errors='coerce')

#####################################################
 #Climate 
 
mdi_climate = pd.merge(combined_hmda_mdi_lar, climate2022,
                       how = 'left')
mdi_climate = mdi_climate[['RISK_SCORE', 'census_tract']].drop_duplicates()

non_mdi_climate = pd.merge(combined_hmda_non_mdi_lar, climate2022,
                       how = 'left')
non_mdi_climate = non_mdi_climate[['RISK_SCORE', 'census_tract']].drop_duplicates()

cdfi_climate = pd.merge(combined_hmda_CDFI_lar, climate2022,
                       how = 'left')
cdfi_climate = cdfi_climate[['RISK_SCORE', 'census_tract']].drop_duplicates()

community_climate = pd.merge(combined_hmda_community_lar, climate2022,
                       how = 'left')
community_climate = community_climate[['RISK_SCORE', 'census_tract']].drop_duplicates()

top25_climate = pd.merge(combined_hmda_top25_lar, climate2022,
                       how = 'left')
top25_climate = top25_climate[['RISK_SCORE', 'census_tract']].drop_duplicates()

fintech_climate = pd.merge(combined_hmda_fintech_lar, climate2022,
                       how = 'left')
fintech_climate = fintech_climate[['RISK_SCORE', 'census_tract']].drop_duplicates()

credit_union_climate = pd.merge(combined_hmda_credit_union_lar, climate2022,
                       how = 'left')
credit_union_climate = credit_union_climate[['RISK_SCORE', 'census_tract']].drop_duplicates()


climate_data = pd.DataFrame(columns = ['Percentile',
                                       'MDI',
                                       'Non-MDI',
                                       'CDFI',
                                       'Community',
                                       'Top 25',
                                       'Fintech',
                                       'Credit union'],
                            index = range(0,100))

credit_union_climate['RISK_SCORE'].mean()
top25_climate['RISK_SCORE'].mean()

for i in range(0,100):
    climate_data.loc[i].Percentile = i
    climate_data.loc[i].MDI = mdi_climate['RISK_SCORE'].quantile(q = i/100)
    climate_data.loc[i]['Non-MDI'] = non_mdi_climate['RISK_SCORE'].quantile(q = i/100)
    climate_data.loc[i].CDFI = cdfi_climate['RISK_SCORE'].quantile(q = i/100)
    climate_data.loc[i].Community = community_climate['RISK_SCORE'].quantile(q = i/100)
    climate_data.loc[i]['Top 25'] = top25_climate['RISK_SCORE'].quantile(q = i/100)
    climate_data.loc[i].Fintech = fintech_climate['RISK_SCORE'].quantile(q = i/100)
    climate_data.loc[i]['Credit union'] = credit_union_climate['RISK_SCORE'].quantile(q = i/100)

climate_data.to_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/2. Data Output/Climate percentile data.csv")
mdi_climate['RISK_SCORE'].to_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/2. Data Output/MDI normal dist.csv")
