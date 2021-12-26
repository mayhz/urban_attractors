library(maptools)
require(rgdal)
library(reshape2)
library(maps)

library(ggplot2)
library(ggmap)
library(jpeg)
library(plyr) 

require("RColorBrewer")

#load Riyadh shapefile
Riyadh_TAZ=readShapeSpatial("riyadh_taz/riyahd_taz_wgs84.shp",IDvar="TAZ")
clusters=read.csv("/Users/May/Documents/workspace/Attractor/7to10_results/clean/4_with_distance_final.csv",sep=",",header=FALSE)

mycol<-brewer.pal(7, "Pastel1")
mycol[6]<-'plum4'
mycol[7]<-('white')


#Create a function to generate a continuous color palette
rbPal <- colorRampPalette(mycol)

######### cluster at a time
orig_col<-'plum4'
path='plots/attractors_maps/clean/'

for (i in 1:4)
{
  temp_clusters=clusters
  index <- clusters$V2==i
  current_cluster=clusters[index,]
  
  #temp_clusters$V3[index] <- 0
  
  colors<-rep('white',length(clusters$V1))
  
  
  rbPal <- colorRampPalette(c('blue','cyan'))
  
  #colors <- rbPal(length(clusters$V2))[as.numeric(cut(clusters$V2,breaks = length(clusters$V2)))]
  
  colors[index] <- rbPal(20)[as.numeric(cut(current_cluster$V3,breaks = 20))]
  
  pdf(width=10, height=10, file = paste(path,'cluster',i,".pdf",sep=""))
  plot(Riyadh_TAZ,col=colors ,lwd=0.2)
  dev.off()
}






#This adds a column of color values
# based on the y values
colors <- rbPal(length(clusters$V2))[as.numeric(cut(clusters$V2,breaks = length(clusters$V2)))]
clusters$colors<-colors

leg<-data.frame(l=unique(clusters$V2),col=unique(colors))
leg<-leg[with(leg, order(l)), ]
leg$len<-c(1:7)

freq<-count(clusters,'V2')$freq
leg$freq<-freq
for i in c(1:7)
leg$len[i]<-count(clusters$V2,leg$l[i])
leg$label<-c(1:7)
for (i in 1:7)
{
  leg$label[i]<-paste(leg$l[i] , ',',freq[i])
}

pdf(width=10, height=10, file = "k=6_test2.pdf")
plot(Riyadh_TAZ,col=colors ,lwd=0.2)
legend('bottomright',legend=leg$label[1:6],fill = as.character(leg$col[1:6]),cex=1.3,title="Clusters Counts")
dev.off()

slices <-leg$freq
pct <- round(slices/sum(slices)*100,2)
lbls <- paste(pct,"%",sep="") # ad % to labels
#lbls <-leg$l
pdf(width=10, height=10, file = "k=6_pie.pdf")
pie(slices,labels = lbls, col=as.character(leg$col),radius=0.9,main="Distribution of clusters") 
dev.off()




######### cluster at a time
orig_col<-'plum4'
path='plots/attractors_maps/complete_cityblock_k3/'

for (i in 1:4)
{
  mycol<-rep('white',4)
  mycol[i]<-orig_col
  print (i)
  print (mycol)
  rbPal <- colorRampPalette(mycol)
  colors <- rbPal(length(clusters$V2))[as.numeric(cut(clusters$V2,breaks = length(clusters$V2)))]
  print(length(rbPal))
  
  pdf(width=10, height=10, file = paste(path,'cluster',i,".pdf",sep=""))
  plot(Riyadh_TAZ,col=colors ,lwd=0.2)
  dev.off()
}
