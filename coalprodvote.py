import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

coal = pd.read_excel("coalpublic2016.xls",skiprows=[0,1],index_col=None,header=0) #data frame dropping the first two rows which only contain identifiers for the whole sheet
#Data taken from: https://www.eia.gov/coal/data/public/xls/coalpublic2016.xls
coal.columns = coal.iloc[0] #Chane column lables
coal = coal.drop([0])# Drop this row after the column names have been assigned, otherwise it causes type errors.
#print(coal.describe)
#print(coal.columns)

#coal.columns = coal.iloc[2]

#print(coal.columns)

#coal.plot.box()
#coal = coal_raw.drop([0,1])

state_abbrv = dict(AL='Alabama', 
                   AK='Alaska', 
                   AS='American Samoa', 
                   AZ='Arizona', 
                   AR='Arkansas', 
                   CA='California', 
                   CO='Colorado', 
                   CT='Connecticut', 
                   DE='Delaware', 
                   DC='District of Columbia', 
                   FM='Federated States of Micronesia', 
                   FL='Florida', 
                   GA='Georgia', 
                   GU='Guam', 
                   HI='Hawaii', 
                   ID='Idaho', 
                   IL='Illinois', 
                   IN='Indiana', 
                   IA='Iowa', 
                   KS='Kansas', 
                   KY='Kentucky', 
                   LA='Louisiana', 
                   ME='Maine', 
                   MH='Marshall Islands', 
                   MD='Maryland', 
                   MA='Massachusetts', 
                   MI='Michigan', 
                   MN='Minnesota', 
                   MS='Mississippi', 
                   MO='Missouri', 
                   MT='Montana', 
                   NE='Nebraska', 
                   NV='Nevada', 
                   NH='New Hampshire', 
                   NJ='New Jersey', 
                   NM='New Mexico', 
                   NY='New York', 
                   NC='North Carolina', 
                   ND='North Dakota', 
                   MP='Northern Mariana Islands', 
                   OH='Ohio', 
                   OK='Oklahoma', 
                   OR='Oregon', 
                   PW='Palau', 
                   PA='Pennsylvania', 
                   PR='Puerto Rico', 
                   RI='Rhode Island', 
                   SC='South Carolina', 
                   SD='South Dakota', 
                   TN='Tennessee', 
                   TX='Texas', 
                   UT='Utah', 
                   VT='Vermont', 
                   VI='Virgin Islands', 
                   VA='Virginia', 
                   WA='Washington', 
                   WV='West Virginia', 
                   WI='Wisconsin', 
                   WY='Wyoming')

print(coal.describe)
print("-----------------")
print(coal.columns)
print("-----------------")
print(coal.head)

print("===============")
#s = coal.iloc[3,14]
#print(s)
#print(type(s))
dimension = coal.shape
#rows = dimension[0]
#for i in range(0,rows):
#    s = coal.iloc[i,14]
#    print("AE row: ",i," value: ",s,
#          " type: ",type(s))
          
print("==================")

ae = coal["Average Employees"]
#print(ae)
#print(ae.describe())
#print(ae.max())

#df = pd.DataFrame(coal,columns=["Average Employees","Production (short tons)"])
#df = df.drop([0])
#print(df.head())


#print(ae.max())
#print(ae.describe())
#coal.plot()

#coal.plot.scatter(x="Average Employees", y="Production (short tons)",alpha=0.5)
coal["Mine State"].hist()
print(coal.nunique())
#county_count = coal.groupby("Mine County")["MSHA ID"].nunique()
county_dup = coal.groupby("Mine County")["Mine State"].nunique()
cd3 = county_dup[county_dup > 2] #Find counties that appear in more than one "state"
print(cd3)

coal.plot.scatter(x="Average Employees", y="Labor Hours")


#NEXT STEPS

#Make table of coal production and employees per county'
## Uniform state names
coal["State"] = coal["Mine State"].str.split(' \(').str.get(0) #Keep only state names from "Mine State" before paretheses (thus removing designators like "East" and "Bituminous")

print(coal[coal["State"]== "Pennsylvania"].head())

## Keep counties with same name in different states sepearate by creating a new column with state and county names combined
coal["Co State"] = coal["Mine County"] + ", " + coal["State"]
print(coal.head())

## Put "Refuse Recovery Mines" in their proper states

print(coal.iloc[990,3])

dimension = coal.shape
rows = dimension[0]
cols = dimension[1]
for row in range(0,rows):
    cn = coal.columns.get_loc("Mine State")
    addr_coln = coal.columns.get_loc("Operating Company Address")
    costate_coln =  coal.columns.get_loc("Co State")
    county_coln = coal.columns.get_loc("Mine County")
    mstate = coal.iloc[row,cn] #Get Column number for Mine State
    if(mstate == "Refuse Recovery"):
        #Find actual state from address
        address = coal.iloc[row,addr_coln]
        addr_array = address.split()
        
        actual_state = addr_array[len(addr_array) - 2]
        long_state = state_abbrv[actual_state] #Get long state name from dictionary
        coal.iloc[row,costate_coln] = coal.iloc[row,county_coln]+ ", " + long_state
        
       # print(row)
print("-----------------------------------")
## Sum quantities from each county
co_series = coal.groupby("Co State")["MSHA ID"].nunique()
#print(co_series.size)
print("This spreadsheet represents mines in",co_series.size,"individual US counties.")

print(coal['Average Employees'].sum())


#Import election data for vote by county (Taken from https://electionlab.mit.edu/data)
#Combine tables
#Plot election results vs. coal and employees

#Display plots
#plt.show()# This makes the plots actually appear! https://stackoverflow.com/questions/2130913/no-plot-window-in-matplotlib

