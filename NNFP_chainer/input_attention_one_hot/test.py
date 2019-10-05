import chart_studio.plotly as py
import plotly.figure_factory as ff
import plotly.offline as offline
import numpy as np

data = np.loadtxt("weight.txt",delimiter=' ')
print(data)
data = data.T
x1 = data[0]-2
x2 = data[1]-1
x3 = data[2]-0
x4 = data[3]-1
x5 = data[4]-2

hist_data = [x1, x2, x3, x4, x5]
group_labels = ['G1', 'G2', 'G3', 'G4', 'G5']

fig = ff.create_distplot(hist_data, group_labels, bin_size=.2)
fig.show()
