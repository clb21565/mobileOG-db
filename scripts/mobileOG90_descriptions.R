# here is reproducible code for creating file mobileOG90_metadata.tsv containing product descriptions for https://github.com/clb21565/mobileOG-db/issues/3
# TL;DR - use manual annotations to provide product descriptions. If the the manual annotations are too long, use the eggnog description feature. If that is too long, truncate to a max of 50 characters. 
# For genes with no name (i.e., those from the keyword search dataset of mobileOG-db, use the mobileOG Entry Name
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
pfams=fread("mobileOG-db-beatrix-1.6/mobileOG-db_1.6.orthology_assignments.tsv")

#protclusts90_cluster.tsv is the output of mmseqs on the 'all' faa file of mobileOGdb1.6: 
  #mmseqs easy-cluster $1 protclusts90 protclust90.tmp -a --min-seq-id 0.90 -c 0.8 --cov-mode 0

protclusts90=fread("protclusts90_cluster.tsv",sep="\t",header=FALSE)
colnames(protclusts90)=c("cluster_rep","cluster_member")

protclusts90$cluster_rep=trimws(gsub("\\|(.*?)$","",protclusts90$cluster_rep))
protclusts90$cluster_member=trimws(gsub("\\|(.*?)$","",protclusts90$cluster_member))

mobileOG_reps=mobileOGs%>%filter(`mobileOG Entry Name`%in%protclusts90$cluster_rep)
length(unique(mobileOG_reps$`Manual Annotation`))

mobileOG_reps=merge(mobileOG_reps,pfams,by.x="mobileOG Entry Name",by.y="mobileOG Entry Name")
mobileOG_reps=mobileOG_reps[,c("mobileOG Entry Name","Name","Manual Annotation","Description","PFAMs")]

MA_too_long=mobileOG_reps%>%subset(nchar(`Manual Annotation`)>50)
MA_OK=mobileOG_reps%>%subset(nchar(`Manual Annotation`)<=50)
MA_OK$`Product Description`=MA_OK$`Manual Annotation`
MA_too_long$`Product Description`=trimws(MA_too_long$Description)

mobileOG_reps=rbind(MA_OK,MA_too_long)
rm(MA_OK,MA_too_long)


PD_too_long=mobileOG_reps%>%subset(nchar(`Product Description`)>50)
PD_OK=mobileOG_reps%>%subset(nchar(`Product Description`)<=50)

PD_too_long$`Product Description`=trimws(gsub("\\.(.*?)$","",PD_too_long$`Product Description`))

mobileOG_reps=unique(rbind(PD_OK,PD_too_long,PD_too_long))

PD_too_long=mobileOG_reps%>%subset(nchar(`Product Description`)>50)
#PD_too_long%>%count(Name,`Product Description`,`Product Description2`,sort=TRUE)%>%write.csv("221026_minimal_set_to_edit.csv") #a minimal number of sequences were manually curated to improve product descriptions

#annotations changed in the minimal manual curation edits are in 221026_minimal_set_to_edit_edited along with what they were modified to

edited=fread("221026_minimal_set_to_edit_edited.csv")

tmp=merge(PD_too_long,unique(edited[,c("Product Description","Product Description2")]),
          by.x="Product Description",by.y="Product Description",allow.cartesian = TRUE)

tmp=tmp[,c("mobileOG Entry Name", "Name","Manual Annotation","Description","PFAMs","Product Description2")]
colnames(tmp)=colnames(PD_too_long)
PD_too_long=tmp


mobileOG_reps=rbind(PD_OK,PD_too_long)
rm(PD_too_long,tmp,PD_OK)

mobileOG_reps=mobileOG_reps%>%subset(`Product Description`!="-")

nameisid=mobileOG_reps%>%subset(is.na(`Name`)|Name=="NA:Keyword")
nameisname=mobileOG_reps%>%subset(!is.na(Name)&Name!="NA:Keyword")
nameisid$Name=nameisid$`mobileOG Entry Name`
mobileOG_reps=rbind(nameisid,nameisname)


mobileOG_OKs=mobileOG_reps%>%subset(grepl("NA:",`Product Description`)==FALSE)
mobileOG_NAs=mobileOG_reps%>%subset(grepl("NA:",`Product Description`))
mobileOG_NAs$`Product Description`=mobileOG_NAs$Description

OK=mobileOG_NAs%>%subset(nchar(`Product Description`)<=50)


toolong=mobileOG_NAs%>%subset(nchar(`Product Description`)>50)
toolong$`Product Description`=substr(toolong$`Product Description`, start = 1, stop = 50)

mobileOG_reps=rbind(OK,toolong,mobileOG_OKs)
mobileOG_reps=mobileOG_reps%>%subset(`Product Description`!="-")
mobileOG_reps[,c("mobileOG Entry Name","Name","Product Description")]%>%
  write.table("mobileOG90_metadata.tsv",
              sep="\t",
              row.names = FALSE,
              quote=FALSE,
              fileEncoding = "UTF-8")
