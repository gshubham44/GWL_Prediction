# GWL_Prediction
Groundwater level prediction model based on historical groundwater level fluctuations and rainfall deficit

# INPUT DATA
•	Groundwater Levels: Monthly Historical GWL level data (at least 10 years) 
•	Rainfall: Monthly Normal and Actual Rainfall data

# DIFFERENT SCENARIOS
•	Scenario 1: Predicted water levels with normal Rise/Fall with respect to November based on historical water level data
•	Scenario 2: Predicted water levels with normal Rise/Fall with respect to November based on historical water level data and by considering no rainfall from Dec to May
•	Scenario 3:  Predicted water levels with normal Rise/Fall with respect to November based on historical water level data and by considering rainfall as continued with present deficit from Dec to May
•	Scenario 4: Predicted water levels with normal Rise/Fall with respect to November based on historical water level data and by considering rainfall as continued with normal Rainfall from Dec to May

# SELECTED SCENARIO: 
In this exercise, Scenario 2 is selected for this study to predict the worst case in which there is no rainfall from Dec to May

# MODEL CALCULATIONS:
PWL_DEC = AWL_NOV- Mean (HWLF_(NOV-DEC))- RFD* |HWLF_(NOV-DEC)|
PWL_DEC: Predicted Water Level for next December
AWL_NOV: Actual Water Level for Current November
HWLF_(NOV-DEC): Historical Water Level Fluctuation between November and December
RFD: Rainfall Deviation as a ratio
	RFD = (CARF(UPTO_NOV) – CNRF(UPTO_NOV))/ CNRF(UPTO_NOV)
	CARF(UPTO_NOV): Cumulative Actual Rainfall up to November 
	CNRF(UPTO_NOV): Cumulative Normal Rainfall up to November

# Credits:
Methodology and Sample Data: Mr. K. S. Sastry (Deputy Director) and Andhra Pradesh Ground Water Department, India.
Conceptualization and Development: Shubham Goswami (IISc Bangalore), Prof. M. Sekhar (IISc Bangalore)
