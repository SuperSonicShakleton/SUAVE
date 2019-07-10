import plotly.graph_objs as go
import plotly.plotly as py

trace1 = go.Carpet(
    a = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3],
    b = [4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6],
    x = [2, 3, 4, 5, 2.2, 3.1, 4.1, 5.1, 1.5, 2.5, 3.5, 4.5],
    y = [1, 1.4, 1.6, 1.75, 2, 2.5, 2.7, 2.75, 3, 3.5, 3.7, 3.75],
    aaxis = dict(
        tickprefix = 'a = ',
        smoothing = 0,
        minorgridcount = 9,
        type = 'linear'
    ),
    baxis = dict(
        tickprefix = 'b = ',
        smoothing = 0,
        minorgridcount = 9,
        type = 'linear'
    )
)

data = [trace1]

layout = go.Layout(
    margin = dict(
    	t = 40,
        r = 30,
        b = 30,
        l = 30
    ),
    yaxis = dict(
        range = [0.388,4.361]
    ),
    xaxis = dict(
    	range = [0.667,5.932]
    )
)

fig = go.Figure(data = data, layout = layout)
py.plot(fig, filename = "contourcarpet")