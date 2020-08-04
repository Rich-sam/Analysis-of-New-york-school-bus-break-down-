#!/usr/bin/env python
# coding: utf-8

# # VA Project Assignment 
# submititted by
# Kimaita Bundi 19/04156
# Dominic Mutahi 

# DASHBOARDS are useful devices that communicate data changes over any given time period. To create a functional dashboard, it is crucial to draw from a regularly updated source, define indicators that are critical to the company's or target mission, and show details related to decision making. Dashboards will also display the effects of internal improvements that have been made to help the accelerated implementation of data-driven decisions.
# 
# The dataset I picked is the data collection for the New York Bus Breakdown and Delays. I have selected this dataset because about the entire education sector plays a big part in the transport industry of a town. the arrival and departure of students plays a big part in theire daily activicties of all stakehoders of the industry.
# 
# the information here can be used as the following
# 
# 1.The information can be used to decide the appropriate time of departures
# 2.The information can be used to make decision on quality of busses, the route taken, the lines of communcation, and the training of bus-driving personnel.
# 3.somethings we can't adjust but it can affect the result (like school year, or environmental conditions) we can't change the drop-off times, traffic congestion, occasional equipment glitches, school year dates, environment & climate, and school district budgets,but we can make informed decision with the righ data

# # import necessary libraries

# In[2]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import plotly
import chart_studio.plotly as py
from plotly.offline import init_notebook_mode, iplot
init_notebook_mode()
import plotly.graph_objs as go


# # load the data

# In[3]:


data=pd.read_csv("D:/Data visualization/bus-breakdown-and-delays.csv")


# # PREPROCESS DATA/CLEANING

# In[4]:


#
print(data.info())


# In[5]:


print(data.head(10))


# In[6]:


df=data


# In[7]:


df.columns


# In[8]:


for c in df.columns:
    print("---",c,"---")
    unq = df[c].value_counts() 
    print(unq)


# In[9]:


print(df["How_Long_Delayed"][0:10])


# In[10]:


delayed_str = df["How_Long_Delayed"].values
trial = ["-", "hr", "min", "/"]
for t in trial:
    matching = [s for s in delayed_str if t in str(s)]
    print(matching[0:6])
    
"""
Let's come back and clean this up later.
"""


# Some columns, such as school year and run type, are clearly categorical. Others, such as Occured on, should be datetimes. Many columns, unfortunately, need to be cleaned up, such as How_Long_Delayed. With a sample of each column, and a descrption of the elements within each column, it's possible to now define a datatype structure.

# In[11]:


dtype_structure = {
    "category":["School_Year", "Busbreakdown_ID", "Run_Type", "Bus_No", "Route_Number", "Reason", 
                "Schools_Serviced", "Boro", "Bus_Company_Name", "Incident_Number", 
                "Breakdown_or_Running_Late", "School_Age_or_PreK"],
    #"float":   ["How_Long_Delayed"], # This will need to be cleaned later
    "int":     ["Number_Of_Students_On_The_Bus"],
    "datetime64":["Occurred_On", "Created_On", "Informed_On", "Last_Updated_On"],
    "bool":    ["Has_Contractor_Notified_Schools", "Has_Contractor_Notified_Parents", "Have_You_Alerted_OPT"],
    "object":  []    
}


# In[12]:


#Once the columns have been cleaned up, I will finally convert to a clean Dataframe

for dtp, col in dtype_structure.items():
    df[col] = df[col].astype(dtp)
    
print(df.info())


# # What are the most common type of delays?

# In[13]:


rsn = df.groupby("Reason").size()
lth = range(len(rsn))
plt.bar(lth, rsn)
plt.xticks(lth, rsn.index, rotation=90)
plt.show()


# Heavy traffic account for a majority of the delays. Perhaps alternate routes can be explored on days which are known to have haviest traffic.
# 
# When do delays occur most often?

# In[14]:


delay_time = df.groupby(df["Occurred_On"].map(lambda t: t.hour)).size()
lth = range(len(delay_time))
plt.bar(lth, delay_time)
plt.xticks(lth, delay_time.index, rotation=90)
plt.title("Number of Delays by Hour of the Day")
plt.ylabel("Number of delays reported")
plt.xlabel("Hour of the day")
plt.show()


# As expected, most of the delays occur between 5am and 9am, and 1pm to 5pm, times when school is beginning and ending.

# # Which days are worst for traffic?

# In[15]:


traff_day = df[df["Reason"] == "Heavy Traffic"].groupby(
                                                df["Occurred_On"].map(lambda t: t.weekday())).size()
wkd = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
lth = range(len(traff_day))
plt.bar(lth, traff_day)
plt.xticks(lth, wkd, rotation=90)
plt.title("Occurances of Heavy Traffic by Day of the Week")
plt.ylabel("Heavy Traffic Reports")
plt.show()


# # What about other types of delays?

# In[16]:


wkd = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]#, "Saturday", "Sunday"]
nrows = 4
ncols = 3

fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(16, 6), dpi=80)
plt.suptitle("Occurance of Delay Reason by Weekday")
i = 1
for rsn in df["Reason"].unique():
    reason_day = df[df["Reason"] == rsn].groupby(
                                        df["Occurred_On"].map(lambda t: t.weekday())).size()
    lth = range(len(reason_day))
    plt.subplot(nrows,ncols,i)
    plt.bar(lth, reason_day)
    plt.xticks(lth, wkd, rotation=90)
    #plt.title("Occurances of {r} by Day of the Week".format(r=rsn))
    plt.ylabel(str(rsn))
    i+=1 

# delete empty axes
# axes[5,0].set_axis_off()
plt.show()


# Interestingly, more delays due to Weather Conditions occur on Fridays.

# Now, I'd like to investigate the relatioship between a delay due to "Mechanical Problem" and Bus_Company_Name. Perhaps some companies have faulty busses in general. Bus_Company_Name is a bit messy, so let's clean it up first.

# In[17]:


newdf = pd.DataFrame(df["School_Year"].value_counts())
newdf.rename(index=str, columns={"School_Year": "Bus Breakdowns"},inplace=True)
newdf.index.name = "Year"
newdf.sort_index(ascending=True,inplace=True)
newdf


# In[21]:


from matplotlib.pyplot import figure

newdf.plot.bar(align='center', alpha=0.8,color='blue')
plt.title("Counting the number of bus breakdowns per school year")
plt.show()


# we notice the breakdowns have been increasing each year

# # Visualizing: Proportion of reasons for bus breakdowns per year

# In[22]:


df2 = df[["School_Year","Reason"]]


for ano in df2["School_Year"].unique():
    f, axes = plt.subplots(figsize=(8,8))
    dados = df2.loc[df["School_Year"] == ano]
    dados = pd.DataFrame(dados["Reason"].value_counts())
    
    total = sum(dados["Reason"])
    novo = [x/total for x in dados["Reason"]]
    dados["Fraction"] = novo

    axes.pie(dados["Fraction"],labels=dados.index, autopct='%.2f')
    plt.title("Year "+ str(ano))
    plt.show()
    plt.close('all')
    


# The biggest cause of delays is traffic related followed by mechanical problems.

# In[18]:


bus_comp_val = df["Bus_Company_Name"].value_counts()

print(bus_comp_val[0:10])
 


# In[19]:


borough_affected = data.Boro.value_counts().plot.bar()


# Manhattan is the the neighbourhood which is highly affected by traffic delays while connecticut is the lowest affected. When making decision on estate to bring up school going children or searching for a school this information could help

# In[ ]:




