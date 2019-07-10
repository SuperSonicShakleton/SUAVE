import plotly.graph_objs as go
import plotly.plotly as py

# Alternate and cumbersome way of entering data

"""
trace1 = go.Carpet(
    a = [[10,10,10,10,10],
               [9.5,9.5,9.5,9.5,9.5],
               [9,9,9,9,9],
               [8.5,8.5,8.5,8.5,8.5],
               [8,8,8,8,8]],
    b = [[.3,.325,.35,.375,.4],
               [.3,.325,.35,.375,.4],
               [.3,.325,.35,.375,.4],
               [.3,.325,.35,.375,.4],
               [.3,.325,.35,.375,.4]],
    x = [2, 3, 4, 5, 2.2, 3.1, 4.1, 5.1, 1.5, 2.5, 3.5, 4.5],
    y = [[4850,4825,4750,4625,4450],
               [4700,4700,4675,4575,4450],
               [4550,4575,4575,4525,4425],
               [4350,4425,4450,4450,4375],
               [4125,4250,4300,4325,4300]],

)

"""

trace1 = go.Carpet(
    # The data arrays x, y may either be specified as one-dimensional arrays of data or as arrays of arrays.
    # x and y are arrays of arrays, then the length of a should match the inner dimension and the length of b the outer dimension.

    a=[10, 9.5, 9, 8.5, 8],
    b=[0.3, 0.325, 0.35, 0.375, 0.4],
    x=[[1, 2, 3, 4, 5],
       [1, 2, 3, 4, 5],
       [1, 2, 3, 4, 5],
       [1, 2, 3, 4, 5],
       [1, 2, 3, 4, 5]],
    y=[[4850, 4825, 4750, 4625, 4450],
       [4700, 4700, 4675, 4575, 4450],
       [4550, 4575, 4575, 4525, 4425],
       [4350, 4425, 4450, 4450, 4375],
       [4125, 4250, 4300, 4325, 4300]],

    aaxis=dict(
        tickprefix='a = ',
        ticksuffix=' psf',
        smoothing=1,
        minorgridcount=1,
        # minorgridwidth = 0.6,
        #  minorgridcolor = 'pink',
        gridcolor='magenta',  # This changes the color of the grid but not the edges
        color='magenta',
        gridwidth=3,
        type='linear',

    ),
    baxis=dict(
        tickprefix='b = ',
        smoothing=0.3,
        minorgridcount=1,
        # minorgridwidth = 0.6,
        #  minorgridcolor = 'pink',
        gridcolor='magenta',  # This changes the color of the grid but not the edges
        color='magenta',
        # This changes the color of the edges of the grid. Options blue, magenta, pink, black, white etc
        gridwidth=3,

        type='linear'

    )
)

data = [trace1]

layout = go.Layout(
    plot_bgcolor='white',
    paper_bgcolor='white',  # Plot is a subset of paper!

    margin=dict(  # This is to dictate the extent of margins around the plot
        t=40,
        r=30,
        b=30,
        l=30
    ),
    yaxis=dict(
        tickprefix='Range = ',
        ticksuffix=' nmi',
        showgrid=True,
        showticklabels=True,
        autorange=True
        #   range = [4000,5000]

    ),

    xaxis=dict(
        showgrid=True,
        showticklabels=True,
        autorange=True
        #  	range = [0.5,6]

    )

)

fig = go.Figure(data=data, layout=layout)

# fig = go.Figure(data = data)
py.plot(fig, filename="contourcarpet")