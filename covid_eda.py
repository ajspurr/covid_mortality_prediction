import os
import numpy as np
import pandas as pd
import datetime

cwd = os.getcwd()
project_dir = 'D:\\GitHubProjects\\covid_mortality_prediction'
data_dir = 'D:\\GitHubProjects\\synthea_covid19_data\\100k_synthea_covid19_csv\\'


# ========================================================================================================
# Explore whether patient death date data correlate to a specific patient encounter
# ========================================================================================================

# Load relevant patient data
patients = pd.read_csv(data_dir+'patients.csv', usecols=['Id', 'BIRTHDATE', 'DEATHDATE'])

# Load relevant encounter data
encounters = pd.read_csv(data_dir+'encounters.csv', usecols=['Id', 'START', 'STOP', 'PATIENT', 'ENCOUNTERCLASS', 'DESCRIPTION', 'REASONDESCRIPTION'])

# Remove patients without a death date
patient_df = patients.dropna(subset=['DEATHDATE'])

# Inner join patient_df and encounters so that we are only seeing the encounters of patients who have died
# Rename patient id columns to 'patient_id' in both tables
patient_df.rename(columns={'Id':'patient_id'}, inplace=True)
encounters.rename(columns={'PATIENT':'patient_id'}, inplace=True)
encounters.rename(columns={'Id':'encounter_id'}, inplace=True)

# Inner join
patient_encounters_df = pd.merge(patient_df, encounters, on ='patient_id', how ="inner")

patient_encounters_df.columns

# ====================================================
# Look at one patient at a time
# ====================================================

# Get patient ID's
patient_ids = patient_df['patient_id']
patient_ids.nunique()

# ==========================
# Look at first patient
# ==========================
patient_id_1 = patient_ids.iat[0]

patient_1_encounters = patient_encounters_df[patient_encounters_df['patient_id']==patient_id_1]

patient_1_deathdate = patient_1_encounters['DEATHDATE'].iat[0]

# Convert death date string to datetime object
patient_1_deathdate_dt = datetime.datetime.strptime(patient_1_deathdate, '%Y-%m-%d')

# Convert encounter 'START' and 'STOP' into datetime object series
patient_1_encounters[['START', 'STOP']]
dt_starts = pd.to_datetime(patient_1_encounters['START'], format='%Y-%m-%dT%H:%M:%SZ')
dt_stops = pd.to_datetime(patient_1_encounters['STOP'], format='%Y-%m-%dT%H:%M:%SZ')

patient_1_deathdate_dt > dt_starts.iat[0]

# See which encounters STOP datetime is later than the death date
death_date_less_than_stop = patient_1_deathdate_dt < dt_stops

# Two results: 
# First is admission to ICU, where 'STOP' is technically the day after death date
patient_1_encounters.iloc[50]
# Second is Death certification which had a 'START' and 'STOP' was two weeks after death date
patient_1_encounters.iloc[51]

# ====================================================
# Do all patients who have a death date also have a death certification encounter?
# ====================================================
death_cert_encounters = patient_encounters_df[patient_encounters_df['DESCRIPTION']=='Death Certification']
# No, there are 18134 death certification encounters and 24150 patients who have died

# Get patient ids of patients with no death certification encounter
death_cert_patient_ids = death_cert_encounters['patient_id']

patient_id_no_death_cert = list(set(patient_ids).difference(death_cert_patient_ids))
len(patient_id_no_death_cert)
# 6106 patients with no death certification encounter, which matches 24150 patients who have died minus 18134 death certification encounters

# ====================================================
# Explore most recent encounters in patients who have died who have no death certification encounter
# ====================================================
patient_id_2 = patient_id_no_death_cert[0]
patient_2_encounters = patient_encounters_df[patient_encounters_df['patient_id']==patient_id_2]
patient_2_deathdate = patient_2_encounters['DEATHDATE'].iat[0]
patient_2_deathdate_dt = datetime.datetime.strptime(patient_2_deathdate, '%Y-%m-%d')

# Convert encounter 'START' and 'STOP' into datetime object series
patient_2_encounters[['START', 'STOP']]
patient2_dt_starts = pd.to_datetime(patient_2_encounters['START'], format='%Y-%m-%dT%H:%M:%SZ')
patient2_dt_stops = pd.to_datetime(patient_2_encounters['STOP'], format='%Y-%m-%dT%H:%M:%SZ')

# See which encounters STOP datetime is later than the death date
death_date_less_than_stop_2 = patient_2_deathdate_dt < patient2_dt_stops
death_date_less_than_stop_2.nunique()
# None

# Find most recent encounter
patient_2_encounters['stop_dt'] = patient2_dt_stops
patient_2_encounters_sorted = patient_2_encounters.sort_values(by='stop_dt')
patient_2_last_encounter = patient_2_encounters_sorted.tail(1)

patient_2_last_encounter[['START', 'STOP', 'ENCOUNTERCLASS', 'DESCRIPTION', 'REASONDESCRIPTION', 'DEATHDATE']].T

# Was there a covid encounter at some point?
patient2_covid_encounters = patient_2_encounters['REASONDESCRIPTION'].str.lower().str.contains('covid')
patient2_covid_encounters.nunique()
patient2_covid_encounters.value_counts()
# No

# Was there a covid 'condition' at some point?
patient2_conditions_csv = pd.read_csv(data_dir+'conditions.csv', chunksize=10000)
patient2_conditions_df = pd.concat((x.query("PATIENT == '2b902612-7f67-4043-af26-ecfd36ba89d9'") for x in patient2_conditions_csv), ignore_index=True)

patient2_covid_conditions = patient2_conditions_df['DESCRIPTION'].str.lower().str.contains('covid')
# No


# Was there a covid 'observation' at some point?
patient2_observations_csv = pd.read_csv(data_dir+'observations.csv', chunksize=10000)
patient2_observations_df = pd.concat((x.query("PATIENT == '2b902612-7f67-4043-af26-ecfd36ba89d9'") for x in patient2_observations_csv), ignore_index=True)

patient2_covid_observations = patient2_observations_df['DESCRIPTION'].str.lower().str.contains('cov')
patient2_covid_observations.value_counts()

patient2_observations_df['DESCRIPTION'].unique()
# No






