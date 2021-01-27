#The goal of this script is to devlope my data cleaning skills in python.
#Is there a correlation between coal production or employment and the presidential election results in 2016?

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

coal = pd.read_excel("coalpublic2016.xls",skiprows=[0,1],index_col=None,header=0) #data frame dropping the first two rows which only contain identifiers for the whole sheet
#Data taken from: https://www.eia.gov/coal/data/public/xls/coalpublic2016.xls
coal.columns = coal.iloc[0] #Change column lables
coal = coal.drop([0])# Drop this row after the column names have been assigned, otherwise it causes type errors.
#print(coal.describe)
#print(coal.columns)

#coal.columns = coal.iloc[2]

#print(coal.columns)

#coal.plot.box()
#coal = coal_raw.drop([0,1])

state_abbrv = dict(AL='Alabama', 
                   AK='Alaska', 
                   #AS='American Samoa', 
                   AZ='Arizona', 
                   AR='Arkansas', 
                   CA='California', 
                   CO='Colorado', 
                   CT='Connecticut', 
                   DE='Delaware', 
                   DC='District of Columbia', 
                   #FM='Federated States of Micronesia', 
                   FL='Florida', 
                   GA='Georgia', 
                   #GU='Guam', 
                   HI='Hawaii', 
                   ID='Idaho', 
                   IL='Illinois', 
                   IN='Indiana', 
                   IA='Iowa', 
                   KS='Kansas', 
                   KY='Kentucky', 
                   LA='Louisiana', 
                   ME='Maine', 
                   #MH='Marshall Islands', 
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
                   #MP='Northern Mariana Islands', 
                   OH='Ohio', 
                   OK='Oklahoma', 
                   OR='Oregon', 
                   #PW='Palau', 
                   PA='Pennsylvania', 
                   #PR='Puerto Rico', 
                   RI='Rhode Island', 
                   SC='South Carolina', 
                   SD='South Dakota', 
                   TN='Tennessee', 
                   TX='Texas', 
                   UT='Utah', 
                   VT='Vermont', 
                   #VI='Virgin Islands', 
                   VA='Virginia', 
                   WA='Washington', 
                   WV='West Virginia', 
                   WI='Wisconsin', 
                   WY='Wyoming')


num_counties = {'Alabama':67,
                'Montana':57,'Alaska':25,'Nebraska':93,'Arizona':15,'Nevada':17,'Arkansas':75,'New Hampshire':10,'California':58,'New Jersey':21,'Colorado':63,'New Mexico':33,'Connecticut':8,'New York':62,'Delaware':3,'North Carolina':100,'District of Columbia':1,'North Dakota':53,'Florida':67,'Ohio':88,'Georgia':159,'Oklahoma':77,'Hawaii':5,'Oregon':36,'Idaho':44,'Pennsylvania':67,'Illinois':102,'Rhode Island':5,'Indiana':92,'South Carolina':46,'Iowa':99,'South Dakota':66,'Kansas':105,'Tennessee':95,'Kentucky':120,'Texas':254,'Louisiana':64,'Utah':29,'Maine':16,'Vermont':14,'Maryland':24,'Virginia':136,'Massachusetts':14,'Washington':39,'Michigan':83,'West Virginia':55,'Minnesota':87,'Wisconsin':72,'Mississippi':82,'Wyoming':23,'Missouri':115}
    

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
#coal["Mine State"].hist()
print(coal.nunique())
#county_count = coal.groupby("Mine County")["MSHA ID"].nunique()
county_dup = coal.groupby("Mine County")["Mine State"].nunique()
cd3 = county_dup[county_dup > 2] #Find counties that appear in more than one "state"
print(cd3)

#coal.plot.scatter(x="Average Employees", y="Labor Hours")


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
    state_coln = coal.columns.get_loc("State")
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
        coal.iloc[row,state_coln] = long_state
        
       # print(row)
print("-----------------------------------")
## Sum quantities from each county
co_series = coal.groupby("Co State")["MSHA ID"].nunique()
#print(co_series.size)
print("This spreadsheet represents mines in",co_series.size,"individual US counties.")

print(coal['Average Employees'].sum())

co_emp = coal.groupby('Co State')["Average Employees"].sum() #Sum each county's employees
co_prod = coal.groupby('Co State')["Production (short tons)"].sum()
state_emp = coal.groupby('State')["Average Employees"].sum()
state_prod = coal.groupby('State')["Production (short tons)"].sum()

#Creat table with just counties, empoloyees, and production
coal_condensed = pd.merge(co_emp,co_prod,how='left',on='Co State')

#print(type(co_emp))
#print(co_emp.head(20))
print(coal_condensed.head(25))
#print(state_prod.head(25))


#state_emp.plot(kind='bar',title='Average employees in coal mines by state',figsize=(8,6),xlabel='State',ylabel='Coal Mine Employees (Ave.)')

#Import election data for vote by county (Taken from https://electionlab.mit.edu/data)

election_data = pd.read_csv("countypres_2000-2016.csv")
print(election_data.head(15))
print(election_data.columns)

#Select only 2016 results 
edf = election_data[election_data['year']==2016]


#Add column with combined state an county in order to match with coal data
edf["Co State"] = edf["county"] + ", " + edf["state"]

#Calculate candidate percentages
edf['frac'] = edf['candidatevotes']/edf['totalvotes']

#Combine tables
#Go through election spreadsheet, and add county data from coal spreadsheet to relevant rows

coal_elec = pd.merge(edf,coal_condensed,how='left',on='Co State') 

#Plot election results vs. coal and employees

#Replace NaN values with sensible values as appropriate
#https://www.geeksforgeeks.org/replace-nan-values-#with-zeros-in-pandas-dataframe
coal_elec['Production (short tons)'] = coal_elec['Production (short tons)'].fillna(0)
coal_elec['Average Employees'] = coal_elec['Average Employees'].fillna(0)

print("Sample of our combined data sheet ==== ")

print(coal_elec.head(25))

for i in range(0,3):
    print(coal_elec.iloc[i])




ce_rep = coal_elec[coal_elec["candidate"].str.contains('Trump')]
print((ce_rep[ce_rep['state']=="Alaska"]).shape[0])
print(ce_rep.shape[0])
ce_rep_withcoal = ce_rep[ce_rep['Average Employees']>0]




ce_rep_withcoal.plot.scatter(x="Average Employees",y="frac")
#ce_rep.plot.scatter(x="Production (short tons)",y="frac")
#ce_rep.plot.scatter(x="Average Employees",y="Production (short tons)")

#NEXT STEPS
## Histograms of coal vs. no coal
## Scatter plots with different colors (e.g. black for coal, hollow for others)
## Geographic plots (maps)
## Address county discrepancies 

co_diff = 0

for st in state_abbrv:
    coindata = (ce_rep[ce_rep['state']==state_abbrv[st]]).shape[0]
    coinreality = num_counties[state_abbrv[st]]
    if(not(coindata == coinreality)):
        diff = coindata - coinreality
        co_diff += diff
        print(st," has",coindata,"county equivalents in our data, but", coinreality,"county equivalents in real life! Difference: ",diff)
        
    #print(st,":",(ce_rep[ce_rep['state']==state_abbrv[st]]).shape[0] ) #Check if the number of counties in the data matches the nubmer of county equivalents in the state from: https://www2.census.gov/geo/pdfs/reference/GARM/Ch4GARM.pdf


print("Total Difference =",co_diff)

#Display plots
plt.show()# This makes the plots actually appear! https://stackoverflow.com/questions/2130913/no-plot-window-in-matplotlib

