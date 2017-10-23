
# This is an interactive bar-chart that let users to indicate the values of interest 
# by clicking in the plot and to compare the value with the plotted bars.



# coding: utf-8

get_ipython().magic('matplotlib notebook')
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.colors as mcol

# create the data
np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])

# calculate the standard error
err = (df.T.apply(stats.sem) * 1.96).tolist()

# define the color
red = cm.Reds
blue = cm.Blues


# make the interactivity
def onclick(event):
    yline = event.ydata
    lines.set_data(([0,1], yline))
    mean = [df.iloc[i,].values.mean() for i in range(4)]
    upper = [df.iloc[i,].values.mean() + err[i] for i in range(4)]
    lower = [df.iloc[i,].values.mean() + err[i] for i in range(4)]
    shadebelow = [np.interp(mean[i] - yline, [0, err[i]], [0, 1]) for i in range(4)]
    shadeupper = [np.interp(yline - mean[i], [0, err[i]], [0, 1]) for i in range(4)]
    colors = ['white' if yline == mean[i] else red(shadebelow[i]) 
            if yline < mean[i] else blue(shadeupper[i]) for i in range(4)]
    cax = plt.bar(np.arange(4), df.T.apply(np.mean).tolist(),align = 'center',
            yerr = err, capsize = 10, edgecolor = 'lightgrey', color = colors)
    plt.xticks(np.arange(4), df.T.columns.astype(str).values)
    for txt in plt.gca().texts:
        txt.set_visible(False)
    plt.text(-1, yline + 1000, '%0.0f' % yline)
    
# make the colorbar
cpick = cm.ScalarMappable(cmap = cm.RdBu)
cpick.set_array([])


# make the plot
plt.figure()
cax = plt.bar(np.arange(4), df.T.apply(np.mean).tolist(), align = 'center', 
        yerr = err, capsize = 10, edgecolor = 'lightgrey', color = 'lightgrey')
plt.xticks(np.arange(4), df.T.columns.astype(str).values)
lines = plt.axhline(y = df.values.mean(), color = "red", linestyle = '-')
plt.text(-1, df.values.mean() + 1000, '%0.0f' % df.values.mean())
m = plt.colorbar(cpick, orientation='horizontal')
m.set_ticks([])
m.ax.text(-0.1, -0.6, "Absolutely lower")
m.ax.text(0.85, -0.6, "Absolutely higher")
m.ax.text(0.4, -0.6, "About the same")
plt.title("Indicate your value of interest by clicking.\n Compared the value to the four bars.")


plt.gcf().canvas.mpl_connect('button_press_event', onclick)


