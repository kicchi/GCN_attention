import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px
import plotly.subplots as subplots
import plotly.offline as offline
import plotly.graph_objs as go


# import file
weight = pd.read_table('weight_cep.txt', delim_whitespace=True, header=None)
weight.columns = ['A', 'B'] #TODO change columns name

ecfp = pd.read_table('ecfp_propaty_cep.txt', delim_whitespace=True, header=None)
ecfp.columns = ['A', 'B', 'C', 'D', 'E'] #TODO change columns name

fcfp = pd.read_table('fcfp_propaty_cep.txt', delim_whitespace=True, header=None)
fcfp.columns = ['A', 'B', 'C', 'D', 'E', 'F'] #TODO change columns name

# count
# weight
graphs = [go.Histogram(x=item, xbins=dict(size=.01), name=column_name)
		  for column_name, item in weight.iteritems()]
fig = subplots.make_subplots(rows=len(graphs), cols=1)
for i, graph in enumerate(graphs, 1):
	fig.append_trace(graph, i, 1)
	fig.update_xaxes(range=[0, 1], row=i, col=1)
	fig.update_yaxes(title_text="count", row=i, col=1)
offline.plot(fig)

# ecfp
graphs = [go.Histogram(x=item, xbins=dict(size=.01), name=column_name)
		  for column_name, item in ecfp.iteritems()]
fig = subplots.make_subplots(rows=len(graphs), cols=1)
for i, graph in enumerate(graphs, 1):
	fig.append_trace(graph, i, 1)
	fig.update_xaxes(range=[0, 1], row=i, col=1)
	fig.update_yaxes(title_text="count", row=i, col=1)
offline.plot(fig)

# fcfp
graphs = [go.Histogram(x=item, xbins=dict(size=.01), name=column_name)
		  for column_name, item in fcfp.iteritems()]
fig = subplots.make_subplots(rows=len(graphs), cols=1)
for i, graph in enumerate(graphs, 1):
	fig.append_trace(graph, i, 1)
	fig.update_xaxes(range=[0, 1], row=i, col=1)
	fig.update_yaxes(title_text="count", row=i, col=1)
offline.plot(fig)

# probability
# weight
graphs = [go.Histogram(x=item, xbins=dict(size=.01), histnorm='probability', name=column_name)
		  for column_name, item in weight.iteritems()]
fig = subplots.make_subplots(rows=len(graphs), cols=1)
for i, graph in enumerate(graphs, 1):
	fig.append_trace(graph, i, 1)
	fig.update_xaxes(range=[0, 1], row=i, col=1)
	fig.update_yaxes(title_text="prob", range=[0, 1], row=i, col=1)
offline.plot(fig)

# ecfp
graphs = [go.Histogram(x=item, xbins=dict(size=.01), histnorm='probability', name=column_name)
		  for column_name, item in ecfp.iteritems()]
fig = subplots.make_subplots(rows=len(graphs), cols=1)
for i, graph in enumerate(graphs, 1):
	fig.append_trace(graph, i, 1)
	fig.update_xaxes(range=[0, 1], row=i, col=1)
	fig.update_yaxes(title_text="prob", range=[0, 1], row=i, col=1)
offline.plot(fig)

# fcfp
graphs = [go.Histogram(x=item, xbins=dict(size=.01), histnorm='probability', name=column_name)
		  for column_name, item in fcfp.iteritems()]
fig = subplots.make_subplots(rows=len(graphs), cols=1)
for i, graph in enumerate(graphs, 1):
	fig.append_trace(graph, i, 1)
	fig.update_xaxes(range=[0, 1], row=i, col=1)
	fig.update_yaxes(title_text="prob", range=[0, 1], row=i, col=1)
offline.plot(fig)

'''
# weight
data = [item+i for (i, (column_name, item)) in enumerate(weight.iteritems())]
fig = ff.create_distplot(data, weight.columns, bin_size=.01, show_curve=False, show_rug=False)
#fig = ff.create_distplot(data, weight.columns, bin_size=.01)
#fig = ff.create_distplot(data, weight.columns, bin_size=.01, curve_type='normal')
fig.show()

# ecfp
data = [item+i for (i, (column_name, item)) in enumerate(ecfp.iteritems())]
fig = ff.create_distplot(data, ecfp.columns, bin_size=.02, show_curve=False, show_rug=False)
#fig = ff.create_distplot(data, ecfp.columns, bin_size=.02)
#fig = ff.create_distplot(data, ecfp.columns, bin_size=.02, curve_type='normal')
fig.show()

# fcfp
data = [item+i for (i, (column_name, item)) in enumerate(fcfp.iteritems())]
fig = ff.create_distplot(data, fcfp.columns, bin_size=.01, show_curve=False, show_rug=False)
#fig = ff.create_distplot(data, fcfp.columns, bin_size=.01)
#fig = ff.create_distplot(data, fcfp.columns, bin_size=.01, curve_type='normal')
fig.show()
'''

