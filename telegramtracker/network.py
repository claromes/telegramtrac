# -*- coding: utf-8 -*-

import ast
import time
import argparse
import pandas as pd
import networkx as nx
import community
import matplotlib

from utils import (
	normalize_values
)

'''

Arguments

'''

parser = argparse.ArgumentParser(description='Arguments.')
parser.add_argument(
	'--data-path',
	'-d',
	type=str,
	required=False,
	help='Path where data is located. Will use `./output/data` if not given.'
)

# parse arguments
args = vars(parser.parse_args())

# get main path
if args['data_path']:
	main_path = args['data_path']
	if main_path.endswith('/'):
		main_path = main_path[:-1]
else:
	main_path = './output/data'


# log results
text = f'''
Init program at {time.ctime()}

'''
print (text)

# read collected chats data
print ('Creating network graph')
chats_file_path = f'{main_path}/collected_chats.csv'
chats_file = pd.read_csv(
	chats_file_path,
	encoding='utf-8'
)

# create network
net = {}
source = [
	j for i in chats_file['source'].tolist()
	for j in ast.literal_eval(i)
]

# remove duplicates
source = list(set(source))
channels = [
	(i, j) for i, j in zip(chats_file['username'], chats_file['counter'])
]

for user, counter in channels:
	src = chats_file[
		chats_file['username'] == user
	]['source'].iloc[0]
	src = list(set(ast.literal_eval(src)))
	for i in src:
		if user != i:
			targets = [user] * counter
			if i not in net.keys():
				net[i] = targets
			else:
				net[i].extend(targets)

# create network data
network_data = pd.concat(
	[
		pd.DataFrame(
			{
				'source': [k] * len(net[k]),
				'target': net[k]
			}
		) for k in net.keys()
	]
)

# create graph
G = nx.from_pandas_edgelist(
	network_data,
	create_using=nx.DiGraph()
)

# save network data
network_path = f'{main_path}/Graph.gexf'
nx.write_gexf(G, network_path)
print ('Saved')

# community louvain -> compute the best partition
G_louvain = nx.from_pandas_edgelist(
	network_data,
	create_using=nx.Graph()
)
partition = community.community_louvain.best_partition(G_louvain)

# pos -> Graph
pos = nx.spring_layout(G)

# color the nodes according to their partition
cmap = matplotlib.cm.get_cmap('viridis', max(partition.values()) + 1)

# plt fig size
matplotlib.pyplot.figure(figsize=(16, 10), frameon=False)

# draw network
nx.draw_networkx_edges(G, pos, alpha=0.3)
nx.draw_networkx_nodes(
	G,
	pos,
	partition.keys(),
	node_size=normalize_values(
		list(dict(G.degree).items())
	),
	cmap=cmap,
	node_color=list(partition.values()),
	alpha=0.9
)
nx.draw_networkx_labels(
	G,
	pos,
	font_size=9,
	font_family='georgia',
	bbox={'facecolor':'white', 'alpha':0.5, 'edgecolor':'#373737'}
)

# save image
matplotlib.pyplot.savefig(f'{main_path}/network.png')
