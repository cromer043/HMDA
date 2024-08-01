# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 09:08:32 2024

@author: csromer
""" 
import statsmodels.api as sm
import pandas as pd
import numpy as np

cols = ['lei',
        'activity_year',
        'action_taken',
        'loan_purpose',
        'property_value',
        'interest_rate',
        'loan_term',
        'loan_amount',
        'applicant_race_1',
        'applicant_ethnicity_1',
        'tract_minority_population_percent',
        'tract_to_msa_income_percentage',
        'income',
        'debt_to_income_ratio',
        'applicant_sex',
        'combined_loan_to_value_ratio',
        'co_applicant_sex',
        'co_applicant_sex_observed',
        'applicant_credit_score_type',
        'Minority Status',
        'state_code',
        'county_code',
        'census_tract'
        ]

dtype = {'county_code' : 'str',
       'applicant_age' : 'str',
       'loan_type' : 'str',
       'loan_term' : 'str',
       'combined_loan_to_value_ratio' : 'str',
       'tract_minority_population_percent' : 'str',
       'tract_to_msa_income_percentage' : 'str',
       'debt_to_income_ratio' : 'str',
       'property_value' : 'str',
       'income' : 'str'}
combined_hmda_mdi_lar = pd.read_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/combined_hmda_mdi_lar.csv",
                                    usecols = cols + ['occupancy_type',
                                                      'lien_status',
                                                      'total_units'],
                                    dtype=dtype)

combined_hmda_mdi_lar = combined_hmda_mdi_lar[combined_hmda_mdi_lar['occupancy_type'] == 1]
combined_hmda_mdi_lar = combined_hmda_mdi_lar[combined_hmda_mdi_lar['lien_status'] == 1]
combined_hmda_mdi_lar = combined_hmda_mdi_lar[combined_hmda_mdi_lar['total_units'].isin(['1', '2', '3', '4'])]

combined_hmda_mdi_lar = combined_hmda_mdi_lar[combined_hmda_mdi_lar['activity_year'] == 2022]

combined_hmda_non_mdi_lar = pd.read_csv("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/combined_hmda_non_mdi_lar.csv",
                                        usecols = cols,
                                        dtype= dtype)
del(cols, dtype)
combined_hmda_non_mdi_lar = combined_hmda_non_mdi_lar[combined_hmda_non_mdi_lar['activity_year'] == 2022]



combined_hmda_lar = combined_hmda_non_mdi_lar._append(combined_hmda_mdi_lar,
                                                     ignore_index=True)
del(combined_hmda_mdi_lar,
    combined_hmda_non_mdi_lar)
combined_hmda_lar = combined_hmda_lar[combined_hmda_lar['loan_purpose'] == 1]
combined_hmda_lar['income'] = pd.to_numeric(combined_hmda_lar['income'], errors='coerce').astype('float')
combined_hmda_lar['loan_term'] = pd.to_numeric(combined_hmda_lar['loan_term'], errors='coerce').astype('float')
combined_hmda_lar['combined_loan_to_value_ratio'] = pd.to_numeric(combined_hmda_lar['combined_loan_to_value_ratio'], errors='coerce').astype('float')
combined_hmda_lar['tract_minority_population_percent'] = pd.to_numeric(combined_hmda_lar['tract_minority_population_percent'], errors='coerce').astype('float')
combined_hmda_lar['tract_to_msa_income_percentage'] = pd.to_numeric(combined_hmda_lar['tract_to_msa_income_percentage'], errors='coerce').astype('float')
combined_hmda_lar['property_value'] = pd.to_numeric(combined_hmda_lar['property_value'], errors='coerce').astype('float')
combined_hmda_lar['interest_rate'] = pd.to_numeric(combined_hmda_lar['interest_rate'], errors='coerce').astype('float')


hmda_ts_mdi = pd.read_csv('C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/hmda_ts_mdi.csv', 
                              usecols = ['lei', 'Minority Status']
                              )
hmda_ts_mdi = hmda_ts_mdi.drop_duplicates()

hmda_ts_non_mdi = pd.read_csv('C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/hmda_ts_non_mdi.csv',
                              usecols = ['activity_year', 'lei', 'respondent_name'])

hmda_ts_CDFI = pd.read_csv('C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/hmda_ts_CDFI.csv', 
                              usecols = ['lei']
                              )
hmda_ts_CDFI = hmda_ts_CDFI.drop_duplicates()

hmda_ts_community = pd.read_csv('C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/hmda_ts_community.csv', 
                              usecols = ['lei']
                              )
hmda_ts_community = hmda_ts_community.drop_duplicates()

hmda_ts_trad = pd.read_csv('C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/hmda_ts_trad.csv', 
                              usecols = ['lei']
                              )
hmda_ts_trad = hmda_ts_trad.drop_duplicates()

hmda_ts_fintech = pd.read_csv('C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA/1. Data intermediate/hmda_ts_fintech.csv', 
                              usecols = ['lei']
                              )
hmda_ts_fintech = hmda_ts_fintech.drop_duplicates()

uniquemdi = hmda_ts_mdi['lei'].unique()
uniquecdfi = hmda_ts_CDFI['lei'].unique()
uniquecommunity = hmda_ts_community['lei'].unique()
uniquetrad = hmda_ts_trad['lei'].unique()
uniquefintech = hmda_ts_fintech['lei'].unique()

uniquenon = combined_hmda_lar['lei'].unique()

combined_hmda_lar['MDI'] = np.where(combined_hmda_lar['lei'].isin(uniquemdi),
                             1,
                             0)
combined_hmda_lar['CDFI'] = np.where(combined_hmda_lar['lei'].isin(uniquecdfi),
                             1,
                             0)

combined_hmda_lar['Community'] = np.where(combined_hmda_lar['lei'].isin(uniquecommunity),
                             1,
                             0)

combined_hmda_lar['Traditional'] = np.where(combined_hmda_lar['lei'].isin(uniquetrad),
                             1,
                             0)

combined_hmda_lar['Fintech'] = np.where(combined_hmda_lar['lei'].isin(uniquefintech),
                             1,
                             0)

combined_hmda_lar['Hispanic'] = np.where(combined_hmda_lar['applicant_ethnicity_1'].isin([1,11,13,14]),
                                      1,
                                      0)
combined_hmda_lar['AAPI'] = np.where((combined_hmda_lar['applicant_race_1'].isin([2,21,22,23,24,25,26,27, #*AA*PI Codes
                                                         4,41,42,43,44])) &
                                     (combined_hmda_lar['Hispanic'] == 0), #AA*PI* Codes,
                                      1,
                                      0)
combined_hmda_lar['AIAN'] = np.where((combined_hmda_lar['applicant_race_1'] == 1) & 
                                     (combined_hmda_lar['Hispanic'] == 0),
                                      1,
                                      0)
combined_hmda_lar['Black'] = np.where((combined_hmda_lar['applicant_race_1'] == 3) & 
                                      (combined_hmda_lar['Hispanic'] == 0),
                                      1,
                                      0)
combined_hmda_lar['White'] = np.where((combined_hmda_lar['applicant_race_1'] == 5) & 
                                      (combined_hmda_lar['Hispanic'] == 0),
                                      1,
                                      0)

combined_hmda_lar['NoRace'] = np.where(combined_hmda_lar['Hispanic'] + combined_hmda_lar['AAPI'] + combined_hmda_lar['AIAN'] + combined_hmda_lar['Black'] +combined_hmda_lar['White'] == 0,
                                      1,
                                      0)



conditions = [
    (combined_hmda_lar['applicant_sex'] == 1),
    (combined_hmda_lar['applicant_sex']==2),
    (combined_hmda_lar['applicant_sex'].isin([3,4,6]))
    ]
values = [1,0, np.isnan]

combined_hmda_lar['male'] = np.select(conditions, values) 
combined_hmda_lar['male'] = pd.to_numeric(combined_hmda_lar['male'] ,errors = 'coerce').astype('float')
conditions = [
    (combined_hmda_lar['co_applicant_sex_observed'] == 4),
    (combined_hmda_lar['co_applicant_sex_observed'].isin([1,
                                                   2])),
    (combined_hmda_lar['co_applicant_sex_observed']==3)
    ]
values = [0,1, np.isnan]

combined_hmda_lar['co_applicant'] = np.select(conditions, values) 
combined_hmda_lar['co_applicant'] = pd.to_numeric(combined_hmda_lar['co_applicant'], errors = 'coerce').astype('float')
conditions = [
    (combined_hmda_lar['co_applicant_sex'] == 1),
    (combined_hmda_lar['co_applicant_sex']==2),
    (combined_hmda_lar['co_applicant_sex']>=3)
    ]

values = [1,0, np.isnan]

combined_hmda_lar['co_applicant_male'] = np.select(conditions, values) 
combined_hmda_lar['co_applicant_male'] = pd.to_numeric(combined_hmda_lar['co_applicant_male'], errors = 'coerce').astype('float')
combined_hmda_lar['Equifax_Beacon'] = np.where(combined_hmda_lar['applicant_credit_score_type'] == 1,
                                               1,
                                               0)
combined_hmda_lar['Experian_Fair_Isaac'] = np.where(combined_hmda_lar['applicant_credit_score_type'] == 2,
                                               1,
                                               0)
combined_hmda_lar['FICO_04'] = np.where(combined_hmda_lar['applicant_credit_score_type'] == 3,
                                               1,
                                               0)
combined_hmda_lar['FICO_98'] = np.where(combined_hmda_lar['applicant_credit_score_type'] == 4,
                                               1,
                                               0)
combined_hmda_lar['VantageScore_2'] = np.where(combined_hmda_lar['applicant_credit_score_type'] == 5,
                                               1,
                                               0)
combined_hmda_lar['VantageScore_3'] = np.where(combined_hmda_lar['applicant_credit_score_type'] == 6,
                                               1,
                                               0)
combined_hmda_lar['Other_scoring_model'] = np.where(combined_hmda_lar['applicant_credit_score_type'].isin([7,8,9,10]),
                                               1,
                                               0)


conditions = [
    (combined_hmda_lar['debt_to_income_ratio'] == "<20%" ),
    (combined_hmda_lar['debt_to_income_ratio'] == "20%-<30%" ),
    (combined_hmda_lar['debt_to_income_ratio'] == "30%-<36%" ),
    (combined_hmda_lar['debt_to_income_ratio'] == "36" ),
    (combined_hmda_lar['debt_to_income_ratio'] == "37" ),
    (combined_hmda_lar['debt_to_income_ratio'] == "38" ),
    (combined_hmda_lar['debt_to_income_ratio'] == "39" ),
    (combined_hmda_lar['debt_to_income_ratio'] == "40" ),
    (combined_hmda_lar['debt_to_income_ratio'] == "41" ),
    (combined_hmda_lar['debt_to_income_ratio'] == "42" ),
    (combined_hmda_lar['debt_to_income_ratio'] == "43" ),
    (combined_hmda_lar['debt_to_income_ratio'] == "44" ),
    (combined_hmda_lar['debt_to_income_ratio'] == "45" ),
    (combined_hmda_lar['debt_to_income_ratio'] == "46" ),
    (combined_hmda_lar['debt_to_income_ratio'] == "47" ),
    (combined_hmda_lar['debt_to_income_ratio'] == "48" ),
    (combined_hmda_lar['debt_to_income_ratio'] == "49" ),
    (combined_hmda_lar['debt_to_income_ratio'] == "50%-60%" ),
    (combined_hmda_lar['debt_to_income_ratio'] == ">60%" ),
    (combined_hmda_lar['debt_to_income_ratio'] == "Exempt")
    ]
values = [19, 
          29, 
          35, 
          36,
          37, 
          38, 
          39, 
          40, 
          41, 
          42, 
          43, 
          44, 
          45, 
          46, 
          47, 
          48, 
          49,
          50, 
          60,
          np.nan]

combined_hmda_lar['debt_to_income_ratio'] = np.select(conditions, values) 
combined_hmda_lar['debt_to_income_ratio'].unique() 
conditions = [
    (combined_hmda_lar['action_taken'].isin([3,7])),
    (combined_hmda_lar['action_taken'].isin([1,2,6,8])),
    (combined_hmda_lar['action_taken'].isin([4,5]))
    ]
values = [1,0,np.nan]

combined_hmda_lar['Denial'] = np.select(conditions, values)
combined_hmda_lar = combined_hmda_lar[combined_hmda_lar['Denial'].isin([0,1])]
combined_hmda_lar['state_code'] = np.where(pd.isna(combined_hmda_lar['state_code'])== True,
                                           'Missing',
                                           combined_hmda_lar['state_code'])


del(
    hmda_ts_CDFI, 
    hmda_ts_community, 
    hmda_ts_trad, 
    hmda_ts_fintech,
    hmda_ts_non_mdi,
    uniquemdi, 
    uniquecdfi, 
    uniquecommunity, 
    uniquetrad,
    uniquefintech,
    uniquenon,
    conditions,
    values
)

states = [
    'AL', 
    #'AK', 
    'AZ', 
    'AR', 
    'CA', 
    'CO',
    'CT',
    'DE',
    'DC',
    'FL',
    'GA',
   # 'HI',
    'ID',
    'IL',
    'IN', 
    'IA', 
    'KS',
    'KY',
    'LA',
    'ME',
    'MD',
    'MA',
    'MI',
    'MN',
    'MS',
    'MO',
    'MT',
    'NE',
    'NV',
    'NH',
    'NJ',    
    'NM',
    'NY',
    'NC',
    'ND',
    'OH',
    'OK',
    'OR',
    'PA',
    'RI',
    'SC',
    'SD',
    'TN',
    'TX',
    'UT',
    'VT',
    'VA',
    'WA',
    'WV',
    'WI',
    'WY'
]

regression_data = combined_hmda_lar[(combined_hmda_lar['state_code'].isin(states)) & (combined_hmda_lar['income'].isna() == False) & (combined_hmda_lar['co_applicant'].isna() == False) & (combined_hmda_lar['male'].isna() == False) & (combined_hmda_lar['loan_term'].isna() == False) & (combined_hmda_lar['debt_to_income_ratio'].isna() == False) & (combined_hmda_lar['property_value'].isna() == False)]
regression_data['BlackMDI'] = regression_data['MDI']*regression_data['Black']
regression_data['HispanicMDI'] = regression_data['MDI']*regression_data['Hispanic']
regression_data['AAPIMDI'] = regression_data['MDI']*regression_data['AAPI']
regression_data['AIANMDI'] = regression_data['MDI']*regression_data['AIAN']
regression_data['NoRaceMDI'] = regression_data['MDI']*regression_data['NoRace']
regression_data['income2'] = regression_data['income']**2
regression_data['l2v'] = regression_data['loan_amount']/regression_data['property_value']*100

dummies = pd.get_dummies(regression_data['state_code']).astype(int)
regression_data = regression_data.join(dummies)

y = regression_data[['Denial']]
x = regression_data[['Hispanic', 'Black', 'AAPI', 
                     'AIAN', 'NoRace', 'MDI', 'BlackMDI',
                     'HispanicMDI','AAPIMDI','AIANMDI',
                     'NoRaceMDI', 'income', 'income2',
                     'property_value', 'loan_amount',
                     'l2v', 'debt_to_income_ratio', 
                     'loan_term', 'co_applicant', 'male',
                     'co_applicant', #'co_applicant_male',
                     'tract_to_msa_income_percentage',
                     'tract_minority_population_percent',
                     #'AK', 
                     'AZ', 
                     'AR', 
                     'CA', 
                     'CO',
                     'CT',
                     'DE',
                     'DC',
                     'FL',
                     'GA',
                    # 'HI',
                     'ID',
                     'IL',
                     'IN', 
                     'IA', 
                     'KS',
                     'KY',
                     'LA',
                     'ME',
                     'MD',
                     'MA',
                     'MI',
                     'MN',
                     'MS',
                     'MO',
                     'MT',
                     'NE',
                     'NV',
                     'NH',
                     'NJ',    
                     'NM',
                     'NY',
                     'NC',
                     'ND',
                     'OH',
                     'OK',
                     'OR',
                     'PA',
                     'RI',
                     'SC',
                     'SD',
                     'TN',
                     'TX',
                     'UT',
                     'VT',
                     'VA',
                     'WA',
                     'WV',
                     'WI'
                     ]] 
x_ = sm.add_constant(x)
resultlogit = sm.Logit(y,
                       x_).fit()
print(resultlogit.summary())

np.exp(0.7368) #Black
np.exp(0.7368 -0.8909 + 0.2845) #Black MDI
np.exp(0.3961) #Hispanic
np.exp(0.3961 -0.8909 + 0.1800     ) #Hispanic MDI
np.exp(0.3651) #AAPI
np.exp(0.3651 -0.8909 + 0.2262) #AAPI MDI
np.exp(0.6941) #AIAN
np.exp(0.6941 -0.8909 + 1.4277) #AIAN MDI

xstate = regression_data[['Hispanic', 'Black', 'AAPI', 
                     'AIAN', 'NoRace', 'MDI', 'BlackMDI',
                     'HispanicMDI','AAPIMDI','AIANMDI',
                     'NoRaceMDI', 'income', 'income2',
                     'property_value', 'loan_amount',
                      'debt_to_income_ratio', 
                     'tract_to_msa_income_percentage',
                     'tract_minority_population_percent',
                    'AK', 'AL','AR','AZ','CA', 'CO',
                     'CT','DC', 'DE', 'FL','GA','GU',
                     'HI', 'IA','ID','IL','IN','KS',
                     'KY',  'LA','MA','MD','ME','MI',
                     'MN', 'MO',  'MS','MT','NC','ND',
                     'NE','NH','NJ','NM','NV','NY',
                     'OH','OK','OR','PA','PR','RI',
                     'SC','SD','TN','TX','UT','VA',
                     'VI','VT', 'WA','WI','WV','WY']] 
xstate_ = sm.add_constant(xstate)
resultlogitstate = sm.Logit(y,
                       xstate_).fit()
print(resultlogitstate.summary())

np.exp(0.6917) #Black
np.exp(0.6917   -1.0151     + 0.1927)  #Black MDI
   
np.exp(0.4088) #Hispanic
np.exp(0.4088 -1.0151 + 1.0363 ) #Hispanic MDI

np.exp(0.3235) #AAPI
np.exp(0.3235 -1.0151 +  0.6505 ) #AAPI MDI

np.exp(0.7787) #AIAN
np.exp(0.7787 -1.0151 +   1.1735  ) #AIAN MDI

print(resultlogit.summary())
regression_data.isna().sum()

MDI_data = pd.merge(regression_data,
                    hmda_ts_mdi,
                    how = 'inner')

MDI_data['MDI_Type_Black'] = np.where(MDI_data['Minority Status'] == "B",
                                       1,
                                       0)
MDI_data['MDI_Type_AIAN'] = np.where(MDI_data['Minority Status'] == "N",
                                       1,
                                       0)
MDI_data['MDI_Type_Hispanic'] = np.where(MDI_data['Minority Status'] == "H",
                                       1,
                                       0)
MDI_data['MDI_Type_AAPI'] = np.where(MDI_data['Minority Status'] == "A",
                                       1,
                                       0)

ymdi = MDI_data[['Denial']]
xmdi = MDI_data[['Hispanic', 'Black', 'AAPI', 
                 'AIAN', 'NoRace', 'MDI_Type_Black', 
                 'MDI_Type_Hispanic', 'MDI_Type_AAPI',  
                 'income', 'income2', 'property_value', 
                 'debt_to_income_ratio', 
                 'tract_to_msa_income_percentage',
                 'tract_minority_population_percent',
                 'county_code']]
x_mdi = sm.add_constant(xmdi)
resultlogitmdi = sm.Logit(ymdi, x_mdi).fit()
print(resultlogitmdi.params)
regression_data.isna().sum()

resultols = sm.formula.ols('Denial ~ Hispanic + Black+ AAPI+AIAN+NoRace+MDI+BlackMDI+HispanicMDI+AAPIMDI+AIANMDI+NoRaceMDI+income+income2+property_value+debt_to_income_ratio+tract_to_msa_income_percentage+tract_minority_population_percent', data = regression_data) 
resultols = resultols.fit()
print(resultols.summary())


check = combined_hmda_lar[combined_hmda_lar['lei']=='5493003GQDUH26DNNH17']
check = check[(check['income'].isna() == False) & (check['debt_to_income_ratio'].isna() == False)  & (check['property_value'].isna() == False) & (check['male'].isin([0,1])== True)  & (check['co_applicant'].isin([0,1]) == True) & (check['co_applicant_male'].isin([0,1])==True)]
check.isna().sum()
check['Denial']
check['Denial'].value_counts()
