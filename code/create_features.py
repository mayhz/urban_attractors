
import numpy as np
from os import listdir
from os.path import isfile, join
import pandas as pd

def load_data(data_path = 'synthetic/'):
    """

    Parameters
    ----------
    data_path: str
        Path containing the  data, each file is a target TAZ, that contains inflow and distance from each intersection

    Returns
    -------
    dataset: DataFrame
        A dataframe containing target TAZ and its data
    TAZ_ids: list
        list of all TAZ Ids
    """
    onlyfiles = [ f for f in listdir(data_path) if isfile(join(data_path, f)) ]
    TAZ_ids = [f[:-4] for f in onlyfiles]
    dataframes_list=[]
    for f in onlyfiles:
        print("reading:",data_path+f)
        df=pd.read_csv(data_path+f)
        df['target_TAZ'] = f[:-4]  # get the id of the TAZ
        dataframes_list.append(df)
    dataset=pd.concat(dataframes_list)
    return dataset, TAZ_ids

def compute_distance_mean_std(dataset):
    """

    Parameters
    ----------
    dataset: list
        list of distances

    Returns
    -------
    mean : float
        mean
    std: float
        standard deviation
    """
    return np.mean(dataset), np.std(dataset)



def compute_spatial_dispersion(inflow_dataset):
    """

    Parameters
    ----------
    inflow_dataset: Pandas dataframe
        Dataframe containing the target's TAZ data

    Returns
    -------
    spatial_dispersion: float

    """

    # compute the center of mass

    inflow_dataset['x_center_of_mass'] = inflow_dataset.apply(lambda i: i['Flow'] * i['X'], axis=1)
    inflow_dataset['Y_center_of_mass'] = inflow_dataset.apply(lambda i: i['Flow'] * i['Y'], axis=1)

    inflow_dataset['Xc'] = (
            inflow_dataset['x_center_of_mass'].sum()
            / inflow_dataset['Flow'].sum()
    )

    inflow_dataset['Yc'] = (
            inflow_dataset['Y_center_of_mass'].sum()
            / inflow_dataset['Flow'].sum()
    )

    inflow_dataset['x_dist'] = inflow_dataset.apply(lambda i: i['Flow'] * np.square(i['X'] - i['Xc']), axis=1)
    inflow_dataset['y_dist'] = inflow_dataset.apply(lambda i: i['Flow'] * np.square(i['Y'] - i['Yc']), axis=1)

    spatial_dispersion = (
            np.sqrt(inflow_dataset['x_dist'].sum() + inflow_dataset['x_dist'].sum())
            / inflow_dataset['x_dist'].sum()
    )
    return spatial_dispersion


def create_features(outfile_name):
    """
    Loads the data and creates features

    """

    dataset,TAZ_ids = load_data(data_path="synthetic/")

    outfile = open(outfile_name, "w")
    outfile.write("TAZ_id,total_inflow,distance_mean,distance_cov,spatial_dispersion\n")
    for taz in TAZ_ids:
        taz_data = dataset[dataset['target_TAZ'] == taz]
        inflow_sum = taz_data['Flow'].sum()
        distances = taz_data['KM'].values
        dist_mean, dist_std = compute_distance_mean_std(distances)
        spatail_disp = compute_spatial_dispersion(inflow_dataset=taz_data)
        outfile.write(f"{taz},{inflow_sum},{dist_mean},{dist_std},{spatail_disp}\n")

    outfile.close()
    print(f"file: {outfile_name} containing features is created ")

    return

if __name__ == "__main__":

    create_features("features.csv")
    print ("Done!")


