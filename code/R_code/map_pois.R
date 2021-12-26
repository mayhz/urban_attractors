#from PO coordinates, map them to each TAZ ID based in the shape file
library(maptools)
require(rgdal)
library(sp)

#read in data, and turn it into a SpatialPointsDataFrame
setwd('/Users/mayalhazzani/dev/attractors/R_code/')
poi_data_orig <- read.csv("POI_type_and_subtype.csv")
locations<-poi_data_orig
coordinates(locations) <- c("x", "y")


Riyadh_TAZ=readShapeSpatial("Tracts (TAZ)/riyahd_taz_wgs84.shp",IDvar="TAZ")

locationsSP <- SpatialPoints(locations, proj4string = CRS(proj4string(Riyadh_TAZ)))

#assign TAZ id for each data point
poi_data_orig$TAZ <- over(locationsSP, Riyadh_TAZ)$TAZ

#write to file
write.table(poi_data_orig, file = "ADA_poi_TAZ.csv",quote = FALSE,sep = ",",col.names = TRUE)
