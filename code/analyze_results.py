import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plot_cluster_sizes(data):
    """
    plots number of TAZes in each cluster found
    Parameters
    ----------
    data: Dataframe
        Containing the cluster ids and features of each TAZ

    """
    data['number_TAZ']=1
    data_count=data.groupby("cluster").count().reset_index()
    sns.catplot(data=data_count,x='cluster',y='number_TAZ',kind='bar')
    fname="cluster_sizes.pdf"
    plt.savefig(fname)
    print(f"plot {fname} created")

def plot_clusters_features(data,
                           features_names=['total_inflow',
                                                'distance_mean',
                                                'distance_cov',
                                                'spatial_dispersion']):
    """
    plots the features of each cluster found

    Parameters
    ----------
    data: Dataframe
        Containing the cluster ids and features of each TAZ

    """
    for f in features_names:
        sns.catplot(data=data, x='cluster', y=f, kind='bar')
        filename = f"{f}_dist_per_cluster.pdf"
        plt.tight_layout()
        plt.savefig(filename)
        print(f"plot {filename} created")
        plt.clf()


def plot_features_distributions(data,
                                features_names=['total_inflow',
                                                'distance_mean',
                                                'distance_cov',
                                                'spatial_dispersion']):
    """

    Parameters
    ----------
        data: Dataframe
            Containing features of each TAZ
        features_names: list (str)
            List of feature names to plot

    Returns
    -------


    """
    for f in features_names:
        data[f].hist(bins=50)
        plt.xlabel(f)
        plt.ylabel("frequency")
        filename=f"{f}_distribution.pdf"
        plt.tight_layout()
        plt.savefig(filename)
        print(f"plot {filename} created")
        plt.clf()

if __name__=='__main__':
    #load results
    cluster_results = pd.read_csv("cluster_results.csv")
    #plot sizes of lcusters
    plot_cluster_sizes(cluster_results)
    #plot feature distribution of each cluster
    plot_clusters_features(cluster_results)
    #plot features distributions
    plot_features_distributions(cluster_results)

