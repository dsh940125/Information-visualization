
# This is a scatterplot that shows the average record low and record high weather data in Arlington, Virginia from 2005 to 2014.
# The record high or record low broken in 2015 is also shown in the plot.

# coding: utf-8

get_ipython().magic('matplotlib notebook')
import matplotlib.pyplot as plt
import numpy as np
import mplleaflet
import pandas as pd
import matplotlib.dates as dates
import matplotlib.ticker as ticker

############### clean the data #################
df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/921a697d63e17c1cb86364faf0d309c7fe078fabf6f3e24be2cefa47.csv')
# clean the time data
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].map(lambda x: x.year)
df["Month"] = df["Date"].map(lambda x: x.month)
df["Day"] = df["Date"].map(lambda x: x.day)
# remove the leap days
dfg = df[(df["Month"] != 2)|((df["Month"] == 2) & (df["Day"] != 29))]
# get 2005-2014 data
df = dfg[dfg["Year"] != 2015]
# get the record low data
df1 = df[df["Element"] == 'TMIN'].groupby(["Month","Day"]).min()
df1["Date"] = np.arange('2015-01-01', '2016-01-01',dtype = 'datetime64[D]')
# get the record high data
df2 = df[df["Element"] == 'TMAX'].groupby(["Month","Day"]).max()
df2["Date"] = np.arange('2015-01-01', '2016-01-01', dtype='datetime64[D]')
dfs = pd.concat([df1,df2])

a = np.arange('2015-01-01', '2016-01-01', dtype='datetime64[D]')
a = list(map(pd.to_datetime,a))

# get 2015 data
dfg = dfg[dfg["Year"] == 2015]
df3 = dfg[dfg["Element"] == 'TMIN'].groupby("Date").min()
df4 = dfg[dfg["Element"] == 'TMAX'].groupby("Date").max()
dfm = pd.concat([df3, df4])
dfm = dfm.reset_index()
dff = pd.merge(dfs,dfm,left_on = ["Date","Element"], right_on = ["Date","Element"])
dff1 = dff[((dff["Data_Value_x"] < dff["Data_Value_y"]) & (dff["Element"] == 'TMAX'))]
dff2 = dff[((dff["Data_Value_x"] > dff["Data_Value_y"]) & (dff["Element"] == 'TMIN'))]

b = list(map(pd.to_datetime, dff1["Date"]))
c = list(map(pd.to_datetime, dff2["Date"]))

################## Make the scatterplot ##################
plt.figure()
plt.scatter(b, dff1["Data_Value_y"],c = "red", marker = 10)
plt.scatter(c, dff2["Data_Value_y"],c = "green", marker = 11)
plt.plot(a, dfs[dfs["Element"] == "TMAX"]["Data_Value"],'-',c = "peachpuff")
plt.plot(a, dfs[dfs["Element"] == "TMIN"]["Data_Value"],'-',c = "darkorange")
ax = plt.gca()
ax.xaxis.set_major_locator(dates.MonthLocator())
ax.xaxis.set_minor_locator(dates.MonthLocator(bymonthday = 15))
ax.xaxis.set_major_formatter(ticker.NullFormatter())
ax.xaxis.set_minor_formatter(dates.DateFormatter('%b'))
ax.fill_between(a, dfs[dfs["Element"] == "TMAX"]["Data_Value"], dfs[dfs["Element"] == "TMIN"]["Data_Value"], 
                facecolor="navajowhite", alpha = 0.3)
ax.set_title("The record high and record low temperatures \n in Arlington,Virginia for 2005-2014\n")
plt.legend(["Average High", "Average Low", "Record High Broken in 2015", "Record Low Broken in 2015"])
m = ax.get_yticks()
ax.set_yticklabels(str(i/10) + '$^\circ$C' for i in m)
ax.set_ylim(min(m), max(m))
ax2 = ax.twinx()
ax2.set_yticks(m)
ax2.set_yticklabels(str(i/10*1.8+32) + '$^\circ$F' for i in m)
ax2.set_ylim(min(m), max(m))
