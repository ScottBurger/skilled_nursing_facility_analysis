# -*- coding: utf-8 -*-
"""
for each years worth of data,
take a list of which columns you want to rank by
then subset the main dataset by those columns
apply ranking criteria for them
then pythag optimize the ranks for a score

then plot by year how those scores have changed


datasets from https://data.cms.gov/provider-data/archived-data/nursing-homes
amazingly the data goes back monthly to 2015. we specifically want the 
NH_ProviderInfo_MMMYYYY.csv files out of each zip

15K rows per month
720K rows for 4 years of monthly data

data for 2021 nov/dec off by a month?

how did covid impact these rankings over time?

WEIGHTED_ALL_CYCLES_SCORE
Total Weighted Health Survey Score


"""

 


import os
import pandas as pd


def provider_score(input_file):
    print("processing {}".format(input_file))
    # provider_info_file = pd.read_csv('NH_ProviderInfo_Apr2022.csv',encoding_errors='ignore')
    
    provider_info_file = pd.read_csv(input_file,encoding_errors='ignore')
    #which columns and do they need to be ranked Ascending? true or false. ie: is a lower number better?
    features = {
        # 'Adjusted Total Nurse Staffing Hours per Resident per Day':True,
        # 'Total nursing staff turnover':False,
        # 'Reported Nurse Aide Staffing Hours per Resident per Day':True
        'Number of Certified Beds':False,
        'Average Number of Residents per Day':True, # lower is better
        'Overall Rating':False,
        'Health Inspection Rating':False,
        'Staffing Rating':False,
        'RN Staffing Rating':False,
        'Reported Nurse Aide Staffing Hours per Resident per Day':False
        }
       
    feature_list = list(features.items())
    
    # apply ranks and score
    for i in feature_list:
        provider_info_file['{}_rank'.format(i[0])] = provider_info_file[i[0]].rank(ascending = i[1])
        
    # subset to just the _rank columns. this is the last N for the number of features provided
    rank_subset = provider_info_file[provider_info_file.columns[-len(feature_list):]]
    
    # square each rank then sum and sqrt at row level
    rank_subset = rank_subset.pow(2)
    rank_subset['score'] = (rank_subset.sum(axis=1))**(0.5)
    
    provider_info_file['score'] = rank_subset['score']
   
    # output name, date, score to final results DF
    # Provider Address	Provider City	Provider State	Provider Zip Code

    provider_info_score = provider_info_file[['Processing Date','Provider Name','Provider Address', 'Provider City','Provider State','score']]
    
    return provider_info_score



# get a list of the csvs
os.chdir('F:\docs\dev\python\snf_analysis\data')
files = [x for x in os.listdir() if 'ProviderInfo' in x]

results = pd.DataFrame()
for i in files:
    results = results.append(provider_score(i))    
