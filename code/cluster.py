import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage,dendrogram, fcluster

def plot_elbow(Z,fname):
    """
    Plots the elbow curve
    Parameters
    ----------
    Z: numpy array
        Linkage that results from using scipy.cluster.hierarchy.linkage
    fname: str
        File name to store the plot
    """
    # plots avg distance between clusters
    last = Z[-20:, 2]  # gets the distance
    last_rev = last[::-1]
    idxs = np.arange(1, len(last) + 1)
    plt.plot(idxs, last_rev, '-o')
    plt.xlabel("Number of clusters")
    plt.ylabel("distance")
    plt.savefig(fname)
    print(f"elbow plot created in : {fname}")

def get_hierarchical_linkage(features,method='complete',distance='correlation'):
    """

    Parameters
    ----------
    features: numpy array
        features of each TAZ
    method: str
        method to cluster complete, single, or average
    distance: str
        the distance function to use

    Returns
    -------
   Z: numpy array
        Linkage that results from using scipy.cluster.hierarchy.linkage

    """
    Z = linkage(features, method, distance)
    return Z

def cluster_data(Z,k):
    """

    Parameters
    ----------
    Z: numpy array
        Linkage that results from using scipy.cluster.hierarchy.linkage
    k: int
        Number of clusters


    Returns
    -------
    clusters: list
        cluster id of each TAZ
    """
    clusters = fcluster(Z, k, criterion='maxclust')
    return clusters

if __name__=='__main__':
    features_data = pd.read_csv('features.csv')
    features_data=features_data.dropna()
    features=features_data.drop('TAZ_id',axis=1).values
    Z=get_hierarchical_linkage(features,method='complete',distance='correlation')
    #elbow plow
    plot_elbow(Z,fname="elbow.pdf")
    #cluster
    clusters=cluster_data(Z=Z,k=3)
    features_data['cluster']=clusters
    #write to file
    outfilename="cluster_results.csv"
    features_data.to_csv(outfilename,index=False)
    print(f"cluster results created in {outfilename}")
