import numpy as np 
import networkx as nx
import matplotlib.pyplot as plt
import openpyxl
from networkx.algorithms import tree
import pandas as pd
from powerlaw import *

df = pd.read_excel('/Users/chenweixun/Desktop/coding/論文/資料/threshold_network_0.8.xlsx')
names = pd.read_excel('/Users/chenweixun/Desktop/coding/論文/資料/營收網路名稱.xlsx')

myList = []
for i in range(len(df)):
    myList.append(df.iloc[i])
myArr = np.array(myList)
G = nx.from_numpy_matrix(myArr)

nx.draw(G, node_color='gray', with_labels=True)
plt.show()

degree = {}

for node in G.nodes():
    neighbor_list = [n for n in G.neighbors(node)]
    degree[names.at[node,'names']] = len(neighbor_list)

degree_df = pd.DataFrame.from_dict(degree, orient='index', columns=['degree'])

def cal_estimate(data):
	fit = Fit(data, discrete=True,xmin=(0,1000))
	R, p=fit.distribution_compare('power_law', 'exponential', normalized_ratio = True)
	print(f'{data.name}, alpha = {fit.power_law.alpha}, xmin =  {fit.power_law.xmin}, D = {fit.power_law.D}')
	print(f'loglikelihood ratio = {R}, p-value = {p}')



def plot_powerlaw(data):
	fit = Fit(data, discrete=True, xmin=(0,1000))
	# plot_pdf(data, label="Data as PDF")
	fit.plot_pdf(label="threshold PDF")
	ax1 = fit.power_law.plot_pdf(label="Fitted PDF", ls=":")
	# x, y = pdf(data, ax = ax1)
	# ax1.scatter(x[:-1], y, color='r', s=1)
	# plt.legend(loc=3, fontsize=14);
	plt.show()


print(cal_estimate(degree_df['degree']))
plot_powerlaw(degree_df['degree'])

degree_centtailty = nx.degree_centrality(G)
degree_max_top10 = sorted(degree_centtailty, key=degree_centtailty.get, reverse=True)[:10]
print('前十家degree最高')

for node in degree_max_top10:
    print(names.at[node, 'names'])

color_map = []
for node in G:
    if degree_centtailty[node] >= degree_centtailty[degree_max_top10[4]]:
        color_map.append('red')
    else: 
        color_map.append('gray')      
nx.draw(G, node_color=color_map, with_labels=True)
plt.show()