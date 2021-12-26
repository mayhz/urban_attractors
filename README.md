#Urban attractors
This is the code for creatig results in the paper: Urban attractors: Discovering patterns in regions of attraction in cities https://journals.plos.org/plosone/article/comments?id=10.1371/journal.pone.0250204

This repo also provides the full datasets used in detecting urban attractors in Riyadh city. 

The data directory includes the following data sets:
* road_nw: the road network data. contains street_nodes.txt and street_edges.txt
* taz: the shapefile of Traffic Analysis Zones (TAZes) in taz_shp
* taz_od: The OD matrices. Contains 8 different files of origin-destination flow data. The one currently used in the published analysis is 0_1.txt.
* POI: Points of Interests types and locations in POI_cat.csv.

The code contains the code for creating features, clustering, and analyzing the results.
