import plotly.graph_objs as go
import plotly.plotly as py
import numpy

trace1 = go.Carpet(
    a = [8,8,8,8,8, 8.5, 8.5,8.5,8.5,8.5,9, 9,9,9,9,9.5,9.5,9.5,9.5,9.5, 10,10,10,10,10 ],
    b = [0.3, 0.32, 0.35, 0.37, 0.4, 0.3, 0.32, 0.35, 0.37, 0.4, 0.3, 0.32, 0.35, 0.37, 0.4, 0.3, 0.32, 0.35, 0.37, 0.4, 0.3, 0.32, 0.35, 0.37, 0.4],
    #c = [8000, 9000, 10000, 11000],
    y = [4000, 4100, 4200, 4300, 4400, 4500, 4600, 4700, 4800, 4900]
)

data = [trace1]

fig = go.Figure(data = data)
py.plot(fig, filename="carpet", auto_open=True)