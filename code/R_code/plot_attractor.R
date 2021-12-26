#load librires
# NOTE: To install any library use the command: install.packages("librabay name")
library(maptools)
require(rgdal)
library(reshape2)-
library(maps)
library(mapdata)

library(ggmap)
library(jpeg)
library(plyr) 
library(ggplot2)
#for distance plotting
library(sp)
library(rgeos)

################################# INPUT ############################################
TAZ_ID<-14
####################################################################################
#load Riyadh shapefile
Riyadh_TAZ=readShapeSpatial("/Users/mayalhazzani/Documents/ODs_network/city_dynamics_riyadh_travel_demand/riyadh_taz/riyahd_taz_wgs84.shp",IDvar="TAZ")
#get the TAZ center location
polys<-Riyadh_TAZ@polygons
TAZ_centers<-as.data.frame(matrix(nrow = length(polys), ncol = 3))
names(TAZ_centers) <- c("ID","longitude", "latitude")
TAZ_center<-c(polys[[TAZ_ID[1]]]@labpt[1],polys[[TAZ_ID[1]]]@labpt[2])
TAZ_center<-data.frame("lon"=TAZ_center[1],"lat"=TAZ_center[2])

#Map center
loc<-c(46.723652,24.70)
#load map from Google
myMap <- get_map(location=loc,zoom=10,maptype="satellite")
#myMap <- gmap(loc,zoom=10,maptype="satellite")

#==================== To plot distance  ======================
# create spatialPoint object
coordinates(TAZ_center) <- ~ lon + lat
proj4string(TAZ_center) <- CRS("+init=epsg:4326")

# reproject to Google Mercator (meters)
TAZ_center.mrc <- spTransform(TAZ_center, CRS = CRS("+init=epsg:3857"))

# concentric rings (in miles):
dist.km <-  c(5,10,15,20)

# create a dataframe with the circle coordinates
circ.df <- do.call(rbind,
                   lapply(dist.km,function(n){
                     circ <- gBuffer(TAZ_center.mrc, width = n * 1000, quadsegs=20)
                     circ.wgs <- spTransform(circ, CRS=CRS("+init=epsg:4326"))
                     coords <- lapply(circ.wgs@polygons, function(x) {x@Polygons[[1]]@coords})
                     data.frame(x=coords[[1]][,1], y=coords[[1]][,2], distance=n)
                   }))

# text positions
text.pos <- cbind(aggregate( y ~ distance, data=circ.df, FUN=min), x=TAZ_center$lon, row.names = NULL)

#============================================================

#read TAZ data
mydata = read.csv("ODs_network/sets/14_freq.csv",header=TRUE)

#Save the plot
pdf(paste("spatial/",TAZ_ID,".pdf",sep=","),width=10, height=6)

#Plot the heatmap
ggmap(myMap,extent = "device")+ # background map
  geom_density2d(data = mydata,aes(x=mydata$x,y=mydata$y), size = 0.6,color="blue",alpha=0.4) + #countour
  stat_density2d(data = mydata,aes(x=mydata$x,y=mydata$y, fill = ..level.., alpha = ..level..), size = 0.001,bins = 26, geom = "polygon") + #heatmap
  scale_fill_gradient(low = "green", high = "red") + #heat scale colors
  scale_alpha(range = c(0, 0.5), guide = FALSE)+ #heat scale range
  geom_point(aes(x = TAZ_center$lon, y = TAZ_center$lat),color="blue",pch=13,size=3,alpha=0.2)+ # TAZ center
  geom_path(data=circ.df, aes(x=circ.df$x, y=circ.df$y, group=distance), alpha=0.2,size=4,color="black")+#distance circles
  geom_text(data=text.pos, aes(x=text.pos$x, y=text.pos$y, label=paste0(distance," KM")),size=2) #distance text

#clear Device
dev.off()
