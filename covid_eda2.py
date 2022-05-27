import os
import csv
import pandas as pd

cwd = os.getcwd()
project_dir = 'D:\\GitHubProjects\\covid_mortality_prediction'
data_dir = 'D:\\GitHubProjects\\synthea_covid19_data\\100k_synthea_covid19_csv\\'


# ========================================================================================================
# Filter for patients who have had some record of COVID
# Originally grabbed all patients with anything record related to COVID, but this ended up including 
# 'Suspected COVID' patients who were never confirmed positive, so I filtered more precisely in covid_eda3.py
# ========================================================================================================

csv_file_names = [file for file in os.listdir(data_dir) if file.endswith('.csv')]

covid_patient_ids = set()

# ==========================
# Careplans
# ==========================

# Careplans file has covid-related information in the 'REASONDESCRIPTION' column
careplans = pd.read_csv(data_dir+'careplans.csv', usecols=['PATIENT', 'DESCRIPTION', 'REASONDESCRIPTION'])

covid_reason_bool = careplans['REASONDESCRIPTION'].str.lower().str.contains('covid')
covid_reason_bool = covid_reason_bool.convert_dtypes()
covid_reason_df = careplans[covid_reason_bool]
covid_reason_df['REASONDESCRIPTION'].value_counts()

# Does careplans file have covid-related information in the 'DESCRIPTION' column?
covid_description_bool = careplans['DESCRIPTION'].str.lower().str.contains('covid')
covid_description_bool = covid_description_bool.convert_dtypes()
covid_description_df = careplans[covid_description_bool]
# No

covid_patient_ids = covid_patient_ids.union(set(covid_reason_df['PATIENT']))
len(covid_patient_ids) # 91039

del careplans, covid_reason_bool, covid_reason_df, covid_description_bool, covid_description_df

# ==========================
# Conditions
# ==========================

conditions = pd.read_csv(data_dir+'conditions.csv', usecols=['PATIENT', 'DESCRIPTION'])

covid_description_bool = conditions['DESCRIPTION'].str.lower().str.contains('covid')
covid_description_bool = covid_description_bool.convert_dtypes()
covid_description_df = conditions[covid_description_bool]
covid_description_df['DESCRIPTION'].value_counts()

covid_patient_ids = covid_patient_ids.union(set(covid_description_df['PATIENT']))
len(covid_patient_ids) # 91039

del conditions

# ==========================
# Encounters
# ==========================

encounters = pd.read_csv(data_dir+'encounters.csv', usecols=['PATIENT', 'REASONDESCRIPTION'])

covid_reason_bool = encounters['REASONDESCRIPTION'].str.lower().str.contains('covid')
covid_reason_bool = covid_reason_bool.convert_dtypes()
covid_reason_df = encounters[covid_reason_bool]

covid_patient_ids = covid_patient_ids.union(set(covid_reason_df['PATIENT']))
len(covid_patient_ids) # 91039

del encounters

# ==========================
# Medications
# ==========================
medications = pd.read_csv(data_dir+'medications.csv', usecols=['PATIENT', 'REASONDESCRIPTION'])

covid_reason_bool = medications['REASONDESCRIPTION'].str.lower().str.contains('covid')
covid_reason_bool = covid_reason_bool.convert_dtypes()
covid_reason_df = medications[covid_reason_bool]

covid_patient_ids = covid_patient_ids.union(set(covid_reason_df['PATIENT']))
len(covid_patient_ids) # 91039

del medications

# ==========================
# Observations
# ==========================

observations = pd.read_csv(data_dir+'observations.csv', usecols=['PATIENT', 'DESCRIPTION'])

unique_description = observations['DESCRIPTION'].value_counts()
unique_description_list = unique_description.index.to_list()
for item in unique_description_list:
    if (('covid' in item.lower()) or ('sar' in item.lower())):
        print(item)

covid_description_bool = observations['DESCRIPTION'].str.lower().str.contains('covid')
covid_description_bool = covid_description_bool.convert_dtypes()
covid_description_df = observations[covid_description_bool]
# None

covid_description_bool = observations['DESCRIPTION'].str.lower().str.contains('sars')
covid_description_bool = covid_description_bool.convert_dtypes()
covid_description_df = observations[covid_description_bool]
# 120,341 rows of 'SARS-CoV-2 RNA Pnl Resp NAA+probe'

covid_patient_ids = covid_patient_ids.union(set(covid_description_df['PATIENT']))
len(covid_patient_ids) # 91039

del observations


# ==========================
# Procedures
# ==========================

procedures = pd.read_csv(data_dir+'procedures.csv', usecols=['PATIENT', 'REASONDESCRIPTION'])

covid_reason_bool = procedures['REASONDESCRIPTION'].str.lower().str.contains('covid')
covid_reason_bool = covid_reason_bool.convert_dtypes()
covid_reason_df = procedures[covid_reason_bool]

covid_patient_ids = covid_patient_ids.union(set(covid_reason_df['PATIENT']))
len(covid_patient_ids) # 91039

del procedures

# ==========================
# Save list of patient ids
# ==========================
# Patients were all identified through careplans.csv 'REASONDESCRIPTION' field. Found 91039 patients. 
# No new patients with covid-related data were found in
# conditions, encounters, medications, observations, or procedures.csv

patient_ids_list = list(covid_patient_ids)
len(patient_ids_list)

with open(data_dir+'covid_patient_ids.csv', mode='w', newline='') as covid_patients_file:
    writer = csv.writer(covid_patients_file)
    writer.writerows([id] for id in patient_ids_list)
print('done')















