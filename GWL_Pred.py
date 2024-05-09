# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 12:24:24 2024

@author:    Shubham Goswami
            IISc Bangalore (India)
            shubhamgswm2@gmail.com
            gshubham@iisc.ac.in
"""

# Importing necessary libraries
import pandas as pd
import numpy as np
import openpyxl as xl 

# Loading input data
input_file = "F:\GWL_Prediction\Trial\input_Sample.xlsx"
wb = xl.load_workbook(input_file)

# Load historical rainfall and GWL data
data = pd.read_excel(input_file,sheet_name="Historical")
data = data.set_index(data['Date'])
gwl_pred = pd.read_excel(input_file,sheet_name="Prediction")
gwl_pred = gwl_pred.set_index(gwl_pred['Date'])

# Preprocessing
data['year'] = data['Date'].dt.year
data['month'] = data['Date'].dt.month
years = np.unique(data['year'])
n_years = len(years)
# Pivot the DataFrame
rain_df = data.pivot(index='month', columns='year', values='Rain')
# convert actual rainfall (ARF) from Jan-Dec to Jun-May
arf = rain_df[-7:].append(rain_df[0:5])
gwl_df = data.pivot(index='month', columns='year', values='GWL')

## It is expected that the monthly normal rainfall is obtained using 30 year period.
## If NRF is given as input then read NRF from file:
    
if wb.sheetnames[-1]=='NRF':
    nrf = pd.read_excel(input_file,sheet_name="NRF")
    nrf = nrf.set_index(nrf["Date"])
    nrf = nrf.drop(columns = ['Date'])
    if pd.isna(nrf).values.any():
        raise Exception("Normal rainfall input data (Input file -> NRF) has NaN values")
 
else:
    # Calculation of Normal Rainfall (nrf) from available data
    normal_rainfall = data.groupby(data['Date'].dt.month)['Rain'].mean()
    nrf = normal_rainfall
# Convert year from Jan-Dec to Jun-May 
nrf = nrf[-7:].append(nrf[0:5])
# Calculation of Cumulative Normal Rainfall (cnrf)
cnrf = nrf.cumsum()
# Cumulative Actual Rainfall (CARF) calclulation
carf = arf.cumsum()
# Rainfall Deficit (rfd)
rfd = carf.copy()

#### GWL calculation

# Calculate Historical Water Level Fluctuation (hwlf)
hwlf = pd.DataFrame(index=range(0,n_years-1),columns=["Nov-Dec","Nov-Jan","Nov-Feb","Nov-Mar","Nov-Apr","Nov-May","Year"],)
for yy in range(0,n_years-1):
    hwlf.iloc[yy,0] = gwl_df.iloc[10,yy]-gwl_df.iloc[11,yy] # Nov-Dec
    hwlf.iloc[yy,1] = gwl_df.iloc[10,yy]-gwl_df.iloc[0,yy+1] # Nov-Jan
    hwlf.iloc[yy,2] = gwl_df.iloc[10,yy]-gwl_df.iloc[1,yy+1] # Nov-Feb
    hwlf.iloc[yy,3] = gwl_df.iloc[10,yy]-gwl_df.iloc[2,yy+1] # Nov-Mar
    hwlf.iloc[yy,4] = gwl_df.iloc[10,yy]-gwl_df.iloc[3,yy+1] # Nov-Apr
    hwlf.iloc[yy,5] = gwl_df.iloc[10,yy]-gwl_df.iloc[4,yy+1] # Nov-May
    hwlf.iloc[yy,6] = np.unique(data['year'])[yy]
    
mean_hwlf = hwlf.mean(axis=0)

## Verification
gwl_pred["carf_pred"] = carf.iloc[5,-1]+  gwl_pred["Rain"].cumsum()
gwl_pred["cnrf"] = cnrf.iloc[5:].values
gwl_pred["rfd"] = (gwl_pred["carf_pred"]-gwl_pred["cnrf"])/gwl_pred["cnrf"]
gwl_pred["mean_hwlf"] = 0
gwl_pred["mean_hwlf"][1:] = mean_hwlf.values[0:6]
gwl_pred["GWL_pred"] = data["GWL"][-1]
gwl_pred["GWL_pred"][1:] = data["GWL"][-1]-gwl_pred["mean_hwlf"][1:7]-(gwl_pred["rfd"][0:6].values*abs(gwl_pred["mean_hwlf"][1:7]))

##### Prediction Part:
# Case 1	predicted with normal rise/fall with respect to November based on historical WL data
# Case 2	predicted WLS by considering No Rainfall from Dec-2017 to May-2018
# Case 3	predicted WLS by considering  Rainfall as continued with present deficit from Dec-2017 to May-2018
# Case 4	predicted WLS by considering  Rainfall as continued with normal RF  from Dec-2017 to May-2018

# Case 2: No rainfall from Dec-May
gwl_pred["carf_2"] = (gwl_pred["Rain"]*0).cumsum()+carf.iloc[5,-1]
gwl_pred["rfd_2"] = (gwl_pred["carf_2"]-gwl_pred["cnrf"])/gwl_pred["cnrf"]
gwl_pred["GWL_pred_2"] = data["GWL"][-1]
gwl_pred["GWL_pred_2"][1:] = data["GWL"][-1]-gwl_pred["mean_hwlf"][1:7]-(gwl_pred["rfd_2"][0:6].values*abs(gwl_pred["mean_hwlf"][1:7]))

## Plotting
gwl_pred[["GWL","GWL_pred","GWL_pred_2"]].plot()