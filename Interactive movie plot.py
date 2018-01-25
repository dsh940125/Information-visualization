import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
%matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_palette('Set3', 10)
sns.set_context('talk')
movie=pd.read_csv('Netflix Shows.csv',encoding='cp437')
movie.head()

from ipywidgets import widgets, interactive

ppp = widgets.Dropdown(
    options=['line', 'bar'],
    value='bar',
    description='Plot:',
)

rating = widgets.Dropdown(
    options=['All'] + list(movie['rating'].unique()),
    value='All',
    description='Rating:',
)

def plotit(ppp, rating):
    if rating != 'All':
        df2 = movie[movie.rating == rating]
        tab = df2.groupby("release year").size()
        tab.plot(kind = ppp)
    else:
        tab = movie.groupby("release year").size()
        tab.plot(kind = ppp)
        
interactive(plotit, ppp=ppp, rating=rating)
