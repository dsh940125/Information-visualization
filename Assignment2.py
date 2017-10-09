
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/921a697d63e17c1cb86364faf0d309c7fe078fabf6f3e24be2cefa47.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Arlington, Virginia, United States**, and the stations the data comes from are shown on the map below.

# In[165]:

get_ipython().magic('matplotlib notebook')
import matplotlib.pyplot as plt
import numpy as np
import mplleaflet
import pandas as pd
import matplotlib.dates as dates
import matplotlib.ticker as ticker


def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

# leaflet_plot_stations(400,'921a697d63e17c1cb86364faf0d309c7fe078fabf6f3e24be2cefa47')
df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/921a697d63e17c1cb86364faf0d309c7fe078fabf6f3e24be2cefa47.csv')
df["Date"]=pd.to_datetime(df["Date"])
df["Year"]=df["Date"].map(lambda x: x.year)
df["Month"]=df["Date"].map(lambda x: x.month)
df["Day"]=df["Date"].map(lambda x: x.day)
dfg=df[(df["Month"]!=2)|((df["Month"]==2) & (df["Day"]!=29))]
df=dfg[dfg["Year"]!=2015]
df1=df[df["Element"]=='TMIN'].groupby(["Month","Day"]).min()
df1["Date"]=np.arange('2015-01-01','2016-01-01',dtype='datetime64[D]')
df2=df[df["Element"]=='TMAX'].groupby(["Month","Day"]).max()
df2["Date"]=np.arange('2015-01-01','2016-01-01',dtype='datetime64[D]')
dfs=pd.concat([df1,df2])

a=np.arange('2015-01-01','2016-01-01',dtype='datetime64[D]')
a=list(map(pd.to_datetime,a))

dfg=dfg[dfg["Year"]==2015]
df3=dfg[dfg["Element"]=='TMIN'].groupby("Date").min()
df4=dfg[dfg["Element"]=='TMAX'].groupby("Date").max()
dfm=pd.concat([df3,df4])
dfm=dfm.reset_index()
dff=pd.merge(dfs,dfm,left_on=["Date","Element"],right_on=["Date","Element"])
dff1=dff[((dff["Data_Value_x"]<dff["Data_Value_y"]) & (dff["Element"]=='TMAX'))]
dff2=dff[((dff["Data_Value_x"]>dff["Data_Value_y"])& (dff["Element"]=='TMIN'))]

b=list(map(pd.to_datetime,dff1["Date"]))
c=list(map(pd.to_datetime,dff2["Date"]))

plt.figure()
plt.scatter(b,dff1["Data_Value_y"],c="red",marker=10)
plt.scatter(c,dff2["Data_Value_y"],c="green",marker=11)
plt.plot(a,dfs[dfs["Element"]=="TMAX"]["Data_Value"],'-',c="peachpuff")
plt.plot(a,dfs[dfs["Element"]=="TMIN"]["Data_Value"],'-',c="darkorange")
ax=plt.gca()
ax.xaxis.set_major_locator(dates.MonthLocator())
ax.xaxis.set_minor_locator(dates.MonthLocator(bymonthday=15))
ax.xaxis.set_major_formatter(ticker.NullFormatter())
ax.xaxis.set_minor_formatter(dates.DateFormatter('%b'))
ax.fill_between(a,dfs[dfs["Element"]=="TMAX"]["Data_Value"],dfs[dfs["Element"]=="TMIN"]["Data_Value"],facecolor="navajowhite",alpha=0.3)
ax.set_title("The record high and record low temperatures \n in Arlington,Virginia for 2005-2014\n")
plt.legend(["Average High","Average Low","Record High Broken in 2015","Record Low Broken in 2015"])
m=ax.get_yticks()
ax.set_yticklabels(str(i/10)+'$^\circ$C' for i in m)
ax.set_ylim(min(m),max(m))
ax2=ax.twinx()
ax2.set_yticks(m)
ax2.set_yticklabels(str(i/10*1.8+32)+'$^\circ$F' for i in m)
ax2.set_ylim(min(m),max(m))


# In[ ]:



