import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

fig = {
    'data': [
          {
          'x': df.gdpPercap,
            'y': df.lifeExp,
            'text': df.country,
            'mode': 'markers',
            'name': '2007'},
    ],
    'layout': {
        'xaxis': {'title': 'GDP per Capita', 'type': 'log'},
        'yaxis': {'title': "Life Expectancy"}
    }
}

py.plot(fig, filename='pandas-multiple-scatter')