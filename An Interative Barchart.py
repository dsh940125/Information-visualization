
# This is an interactive bar-chart that let users to define the values of interest 
# by clicking in the plot and to see if the value is covered in certain distributions.



# coding: utf-8


get_ipython().magic('matplotlib notebook')
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib import cm

# create a random data
np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])

# calculate the standard error
err = (df.T.apply(stats.sem) * 1.96).tolist()

# define the color of using
orange = cm.Oranges
blue = cm.Blues


# make the interactivity. This let you to define the value of interest by clicking in the plot
def onclick(event):
    yline = event.ydata
    lines.set_data(([0,1], yline))
    mean = [df.iloc[i,].values.mean() for i in range(4)]
    upper = [df.iloc[i,].values.mean() + err[i] for i in range(4)]
    lower = [df.iloc[i,].values.mean() + err[i] for i in range(4)]
    shadebelow = [np.interp(mean[i] - yline, [0, err[i]], [0.5, 1]) for i in range(4)]
    shadeupper = [np.interp(yline - mean[i], [0, err[i]], [0.5, 1]) for i in range(4)]
    colors = ['white' if yline == mean[i] else orange(shadebelow[i]) 
            if yline < mean[i] else blue(shadeupper[i]) for i in range(4)]
    cax = plt.bar(np.arange(4), df.T.apply(np.mean).tolist(),align = 'center',
            yerr = err, capsize = 10, edgecolor = 'lightgrey', color = colors)
    plt.xticks(np.arange(4), df.T.columns.astype(str).values)
    for txt in plt.gca().texts:
        txt.set_visible(False)
    plt.text(-1, yline + 1000, '%0.0f' % yline)



# plot the graph
plt.figure()
cax = plt.bar(np.arange(4), df.T.apply(np.mean).tolist(), align = 'center', 
        yerr = err, capsize = 10, edgecolor = 'lightgrey', color = 'lightgrey')
plt.xticks(np.arange(4), df.T.columns.astype(str).values)
lines = plt.axhline(y = df.values.mean(), color = "red", linestyle = '-')
plt.text(-1, df.values.mean() + 1000, '%0.0f' % df.values.mean())


plt.gcf().canvas.mpl_connect('button_press_event', onclick)





