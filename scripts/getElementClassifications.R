# here is reproducible R code for classifying the contents of mobileOG-db as being derived from plasmids, phages, IGEs, TEs, or CEs
# this will eventually be incorporated directly into mobileOGdb metadata. 
# not all of these packages are necessarry. at least data.table, dplyr, and tidyr are 
library(rstatix)
library(tidyr)
library(data.table)
library(plyr)
library(dplyr)
library(ggplot2)
library(readxl)
library(pals)
library(gggenes)
library(ggpubr)
library(gridExtra)
library(stringr)
library(stringdist)
library(ggbeeswarm)
library(vegan)
library(Hmisc)

`%notin%` <- Negate(`%in%`)



mobileOGs=fread("mobileOG-db-beatrix-1.6/mobileOG-db-beatrix-1.6-All.csv")
mobileOGs_classes=mobileOGs[,c("mobileOG Entry Name","Major mobileOG Category","Minor mobileOG Categories","ACLAME","immedb","GPD",
            "pVOG","ICE","AICE","CIME","IME","ISFinder","PlasmidRefSeq","COMPASS")]

TE=mobileOGs_classes%>%subset(ISFinder!=0)
TE$MGE_Class="Insertion Sequence (IS)"
IGE=mobileOGs_classes%>%subset(AICE!=0|ICE!=0|CIME!=0|immedb!=0|IME!=0)%>%subset(ISFinder==0)
IGE$MGE_Class="Integrative Element (IGE)"
Ph=mobileOGs_classes%>%subset(GPD!=0|pVOG!=0)
Ph$MGE_Class="Phage"
plasmidic=mobileOGs_classes%>%subset(COMPASS!=0|PlasmidRefSeq!=0)%>%
  filter(`mobileOG Entry Name`%notin%c(IGE$`mobileOG Entry Name`))%>%
  subset(ISFinder==0)
plasmidic$MGE_Class="Plasmid"
CE=mobileOGs_classes%>%subset(`Major mobileOG Category`=="transfer"&
                                grepl("conjugati",`Minor mobileOG Categories`))
CE$MGE_Class="Conjugative Element (CE)"

merged=rbind(TE,IGE,Ph,plasmidic,CE)

ACLAME=mobileOGs_classes%>%filter(`mobileOG Entry Name`%notin%merged$`mobileOG Entry Name`)

ACLAME$MGE_Class="Only detected in ACLAME"

merged=rbind(merged,ACLAME)



merged[,c("mobileOG Entry Name","MGE_Class")]%>%
  group_by(`mobileOG Entry Name`)%>%
       mutate(MGE_Class = paste((MGE_Class), collapse=","))%>%ungroup()

length(unique(merged$`mobileOG Entry Name`))



out=merged%>%group_by(`mobileOG Entry Name`) %>%
  dplyr::summarize(MGE_Class = paste(unique(MGE_Class),collapse=','))%>%
  ungroup()

out%>%write.csv("mobileOG_class_information.csv",row.names = FALSE)
