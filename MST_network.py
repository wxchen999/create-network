import numpy as np 
import networkx as nx
import matplotlib.pyplot as plt
import openpyxl
from networkx.algorithms import tree
import pandas as pd
from powerlaw import *


df = pd.read_excel('/Users/chenweixun/Desktop/coding/論文/資料/營收網路.xlsx')
names = pd.read_excel('/Users/chenweixun/Desktop/coding/論文/資料/營收網路名稱.xlsx')

myList = []
for i in range(len(df)):
    myList.append(df.iloc[i])
myArr = np.array(myList)


G = nx.from_numpy_matrix(myArr)
mst = tree.minimum_spanning_edges(G, algorithm="kruskal", data=False)
edgelist = list(mst)

A = nx.Graph()    
A.add_edges_from(edgelist)
# print(nx.number_of_nodes(A))
# print(nx.number_of_edges(A))
# nx.draw(A, node_color='gray', with_labels=True)
# plt.show()





degree_centtailty = nx.degree_centrality(A)
degree_max_top5 = sorted(degree_centtailty, key=degree_centtailty.get, reverse=True)[:5]
print('前五家degree最高')
for node in degree_max_top5 :
    print(names.iloc[node])
color_map = []
for node in A:
    if degree_centtailty[node] >= degree_centtailty[degree_max_top5[4]]:
        color_map.append('red')
    else: 
        color_map.append('gray')      
nx.draw(A, node_color=color_map, with_labels=True)
plt.show()




eigenvector_centtailty = nx.eigenvector_centrality(A)
eigenvector_max_top5 = sorted(eigenvector_centtailty, key=eigenvector_centtailty.get, reverse=True)[:5]
print('前五家eigenvector最高')
for node in eigenvector_max_top5 :
    print(names.iloc[node])
color_map = []
for node in A:
    if eigenvector_centtailty[node] >= eigenvector_centtailty[eigenvector_max_top5[4]]:
        color_map.append('red')
    else: 
        color_map.append('gray')      
nx.draw(A, node_color=color_map, with_labels=True)
plt.show()

closeness_centtailty = nx.closeness_centrality(A)
closeness_max_top5 = sorted(closeness_centtailty, key=closeness_centtailty.get, reverse=True)[:5]
print('前十家closeness最高')
for node in closeness_max_top5:
    print(names.iloc[node])
color_map = []
for node in A:
    if closeness_centtailty[node] >= closeness_centtailty[closeness_max_top5[4]]:
        color_map.append('red')
    else: 
        color_map.append('gray')      
nx.draw(A, node_color=color_map, with_labels=True)
plt.show()


betweenness_centtailty = nx.betweenness_centrality(A)
betweenness_max_top5 = sorted(betweenness_centtailty, key=betweenness_centtailty.get, reverse=True)[:10]
print('前十家betweenness最高')
for node in betweenness_max_top5:
    print(names.iloc[node])

color_map = []
for node in A:
    
    if betweenness_centtailty[node] >= betweenness_centtailty[betweenness_max_top5[4]]:
        color_map.append('red')
    else: 
        color_map.append('gray')      
nx.draw(A, node_color=color_map, with_labels=True)
plt.show()


###########################

degree = {}

for node in A.nodes():
    neighbor_list = [n for n in A.neighbors(node)]
    degree[names.at[node,'names']] = len(neighbor_list)

degree_df = pd.DataFrame.from_dict(degree, orient='index', columns=['degree'])

def cal_estimate(data):
	fit = Fit(data, discrete=True, xmin = (0, 100))
	R, p=fit.distribution_compare('power_law', 'exponential', normalized_ratio = True)
	print(f'{data.name}, alpha = {fit.power_law.alpha}, xmin =  {fit.power_law.xmin}, D = {fit.power_law.D}')
	print(f'loglikelihood ratio = {R}, p-value = {p}')



def plot_powerlaw(data):
	fit = Fit(data, discrete=True, xmin = (0, 100))
	# plot_pdf(data, label="Data as PDF")
	fit.plot_pdf(label="threshold PDF")
	ax1 = fit.power_law.plot_pdf(label="Fitted PDF", ls=":")
	# x, y = pdf(data, ax = ax1)
	# ax1.scatter(x[:-1], y, color='r', s=1)
	# plt.legend(loc=3, fontsize=14);
	plt.show()


print(cal_estimate(degree_df['degree']))
plot_powerlaw(degree_df['degree'])