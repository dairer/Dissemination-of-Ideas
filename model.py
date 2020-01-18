import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import seaborn.apionly as sns
import matplotlib.animation
import random
# Create Graph
np.random.seed(2)
from random import randint
import matplotlib.cm as cmx
import matplotlib.colors as colors


class indicidual:
    def __init__(self, trait_1, trait_2, trait_3, trait_4, trait_5):
        self.trait_1 = trait_1
        self.trait_2 = trait_2
        self.trait_3 = trait_3
        self.trait_4 = trait_4
        self.trait_5 = trait_5

    def my_colour(self):
        return (((self.trait_1+self.trait_2+self.trait_3+self.trait_4+self.trait_5)%1))
    def my_size(self):
        # size from 0-5
        return(self.trait_1+self.trait_2+self.trait_3+self.trait_4+self.trait_5)*2
    def my_sum(self):
        return(self.trait_1+self.trait_2+self.trait_3+self.trait_4+self.trait_5)


num_individuals = 200



individuals = [indicidual(random.random(),
                          random.random(),
                          random.random(),
                          random.random(),
                          random.random()) for n in range(num_individuals)]






#start with 25 nodes randomly connected
num_edges = 200
G = nx.gnm_random_graph(n=num_individuals, m=num_edges,  seed=None, directed=False)

#colour edges based on their group affiliation
#there are two groups A and B
A = random.choices(list(G.nodes()), k=12)


jet = cm = plt.get_cmap('jet')
cNorm  = colors.Normalize(vmin=0, vmax=1)
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
print (scalarMap.get_clim())


# Build plot
fig, ax = plt.subplots()

def update(num):

    ax.clear()

    # if two individuals are connected the compare traits, pick trait at random,
    # who evers is stronger, ie larger value, is inherited by the other



    edges = [e for e in G.edges()]

    for e in edges:
        # pick trait at random
        rand_train = 'trait_'+str(randint(1, 5))
        val_0_trait = getattr(individuals[e[0]], rand_train)
        val_1_trait = getattr(individuals[e[1]], rand_train)

        # see who has the strongest trait, ie closest to 0 or 5
        if val_0_trait > 2.5 and val_1_trait > 2.5:
            if val_0_trait > val_1_trait:
                # update 1s val to half way between the values
                setattr(individuals[e[1]], rand_train, val_1_trait+(val_0_trait - val_1_trait)/2)
            else:
                setattr(individuals[e[0]], rand_train, val_0_trait+(val_1_trait - val_0_trait)/2)
        elif val_0_trait < 2.5 and val_1_trait < 2.5:
            if val_0_trait < val_1_trait:
                # update 1s val to half way between the values
                setattr(individuals[e[1]], rand_train, val_1_trait-(val_1_trait - val_0_trait)/2)
            else:
                setattr(individuals[e[0]], rand_train, val_0_trait-(val_0_trait - val_1_trait)/2)
        elif val_0_trait < 2.5 and val_1_trait > 2.5:
            #see which is more extreme
            if 5-val_1_trait < val_0_trait:
                # val 1 is more extreme
                setattr(individuals[e[0]], rand_train, val_0_trait+(val_1_trait - val_0_trait)/2)
            else:
                # val 0 is more extreme
                setattr(individuals[e[1]], rand_train, val_1_trait-(val_1_trait - val_0_trait)/2)
        elif val_0_trait > 2.5 and val_1_trait < 2.5:
            #see which is more extreme
            if 5-val_0_trait < val_1_trait:
                # val 0 is more extreme
                setattr(individuals[e[1]], rand_train, val_1_trait+(val_0_trait - val_1_trait)/2)
            else:
                # val 1 is more extreme
                setattr(individuals[e[0]], rand_train, val_0_trait-(val_0_trait - val_1_trait)/2)



    # add edges between most simialr individuals
    for n in G.nodes():
        for h in G.nodes():
            if n is not h:
                if abs(individuals[n].my_sum() - individuals[h].my_sum()) < 0.2:
                    G.add_edge(n,h)
                if G.has_edge(n,h) and abs(individuals[n].my_sum() - individuals[h].my_sum()) > 0.2:
                    G.remove_edge(n,h)

    # add random edges
    noise = [(random.randint(0,num_individuals-1), random.randint(0,num_individuals-1)) for x in range(random.randint(1,5))]
    G.add_edges_from(noise)

    edge_width = [(2*abs(individuals[i[0]].my_sum()-individuals[i[1]].my_sum())) for i in G.edges()]
    cols = [scalarMap.to_rgba(individuals[i].my_colour()) for i in range(num_individuals)]



    nx.draw(G,pos=nx.spring_layout(G, k=1.5),  node_size=50, node_color=cols, width= edge_width, alpha=0.5)

    ax.set_xticks([])
    ax.set_yticks([])


ani = matplotlib.animation.FuncAnimation(fig, update, frames=2, interval=250, repeat=True)
plt.show()
