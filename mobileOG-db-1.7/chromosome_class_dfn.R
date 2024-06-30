## Code used to acquire the "chromosome, hitcher, accessory, or unknown" class. Corresponding data files can be acquired here: (zenodo link). 

library(tidyr)
library(data.table)
library(plyr)
library(dplyr)
library(gridExtra)
library(stringr)
library(stringdist)

`%notin%` <- Negate(`%in%`)

chrom_clusters=fread("Chrom_and_MGE_protclusts80_cluster.tsv",sep="\t",header=FALSE)
colnames(chrom_clusters)=c("cluster_rep","cluster_member")
retired_seqs=fread("240623-retired-mobileOGs.csv")
chrom_mges=chrom_clusters%>%subset(grepl("^mge",cluster_member))%>%count(cluster_rep)
chrom_mges=chrom_clusters%>%filter(cluster_rep%in%chrom_mges$cluster_rep)

dmnd_result=fread("chrom-mobileOG-mapped-2.tsv",sep="\t",header=FALSE)
dmnd_result=dmnd_result%>%mutate(mobileOG=gsub("\\|(.*?)$","",dmnd_result$V2))%>%filter(mobileOG%notin%retired_seqs$`mobileOG Entry Name`)

chromosomes_with_alignments=chrom_clusters%>%filter(cluster_rep%notin%chrom_mges$cluster_rep)%>%filter(cluster_member%in%dmnd_result$V1)
mges_with_alignments=chrom_mges%>%filter(cluster_member%in%dmnd_result$V1)

# chrom_clusters%>%filter(cluster_member%in%dmnd_result$V1)#check no missing data - success
# dmnd_result%>%filter(V1%notin%chrom_clusters$cluster_member)#check no missing data - success

remaining=chromosomes_with_alignments

recombinases_to_get=fread("recombinases-to-get.txt",sep="\t",header=FALSE)
strs=unique(recombinases_to_get$V1)
rxs=unlist(strsplit(strs, ","))%>%unique()
pfam_metadata=fread("pfamA.txt",sep="\t")[,c(1,2,3,4,5,6,7,8)]

colnames(pfam_metadata)=c("pfam","pfam_name","extended_name_idk","description","author","database","modeltype","description_2")
pfam_metadata=pfam_metadata%>%filter(pfam_name%in%rxs)

recombs=fread("C:/Users/Connor/Downloads/mobileog_tool/chrom-recombs.txt.txt",sep="$")[,-4]
yrs=fread("C:/Users/Connor/Downloads/mobileog_tool/chroms_trdb.txt",sep="$")[,-4]
pfams=fread("C:/Users/Connor/Downloads/mobileog_tool/chr_and_chrmge_vs_pfam",sep="\t",header=FALSE)

colnames(pfams)=c("query","target","fident",
                           "alnlen","mismatch","gapopen",
                           "qstart","qend","tstart","tend",
                           "evalue","bits")
pfams$pfam=gsub("\\.(.*?)$","",pfams$target)
pfams=merge(pfams,pfam_metadata,by="pfam")

pfam_match=(pfams%>%filter(query%in%remaining$cluster_member))[,c("query")]
yr_match=(yrs%>%filter(target_name%in%remaining$cluster_member))[,c("target_name")]
rc_match=(recombs%>%filter(target_name%in%remaining$cluster_member))[,c("target_name")]
unique_to_get=c(pfam_match$query,yr_match$target_name,rc_match$target_name)%>%unique()

recombs=remaining%>%filter(cluster_member%in%unique_to_get)

recombs%>%write.table("240628-chromosomal-recombinases.tsv",sep="\t",row.names = FALSE,quote = FALSE) ## write recombinases to TSV file so that they may be added to new mobileOG-db recombinase class. 
resultCHROMCLASS=remaining%>%filter(cluster_rep%notin%recombs$cluster_rep)
resultCHROMCLASS%>%write.table("240628-resulting-chroms-final.tsv",row.names = FALSE,quote=FALSE,sep="\t")
