import scipy
import numpy as np
import pandas as pd



def stat_sig_test(overlap,a,b,universe):
    import scipy.stats
    table=[[overlap,a],[b,universe]]
    oddsratio,p_value=scipy.stats.fisher_exact(table,alternative ='greater')
    return p_value


def pois_and_motifs(motif_df, pattern):
    # 2: plot the percentage each subtype share in each cluster  =======================

    df = pd.read_csv("/Users/May/Documents/workspace/Attractor/POI/Final_POI_counts.csv")[
        ['TAZ', 'subtype', 'subtype_count']]
    subtype_total = df.groupby('subtype').sum().reset_index()[['subtype', 'subtype_count']]
    subtype_total.columns = [['subtype', 'subtype_total']]

    motif_df = pd.merge(df, motif_df, on='TAZ')

    motif_total = motif_df.groupby('subtype').sum().reset_index()
    motif_total = pd.merge(motif_total, subtype_total, on='subtype')

    # significance test
    pvals = []
    total_a = np.sum(motif_total['subtype_count'])
    universe = 12254

    for type in motif_total['subtype'].values:
        overlap = motif_total[motif_total['subtype'] == type]['subtype_count']
        a = total_a - overlap

        b = motif_total[motif_total['subtype'] == type]['subtype_total']
        b = b - overlap
        p_value = stat_sig_test(overlap, a, b, universe)
        pvals.append(p_value)
    motif_total['pvalues'] = pvals