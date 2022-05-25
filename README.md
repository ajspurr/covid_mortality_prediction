# COVID Mortality Prediction
## Overview
In this project I use synthetic patient data to predict COVID-19 mortality. Similar to real-world projects, the data is represented in a high-dimensional multi-table relational format. As such, plenty of time and effort is given to flattening and transforming the data such that it is optimized for binary classification machine learning to predict mortality. 

### Data
**Source:** Synthea™ Novel coronavirus (COVID-19) synthetic data set

**Format:** 16 relational tables (patients, conditions, encounters, medications, procedures, etc.)

**Background:** Per Synthea's publication (referenced below) "March through May 2020, a model of novel coronavirus (COVID-19) disease progression and treatment was constructed for the open-source Synthea patient simulation. The model was constructed using three peer-reviewed publications published in the early stages of the global pandemic ... The simulation outputs synthetic Electronic Health Records (EHR) ... For this simulation, we generated 124,150 synthetic patients, with 88,166 infections and 18,177 hospitalized patients. Patient symptoms, disease severity, and morbidity outcomes were calibrated using clinical data from the peer-reviewed publications ... The resulting model, data, and analysis are available as open-source code on GitHub and an open-access data set is available for download."

**Reference:** Walonoski J, Klaus S, Granger E, Hall D, Gregorowicz A, Neyarapally G, Watson A, Eastman J. Synthea™ Novel coronavirus (COVID-19) model and synthetic data set. Intelligence-Based Medicine. 2020 Nov;1:100007. https://doi.org/10.1016/j.ibmed.2020.100007
