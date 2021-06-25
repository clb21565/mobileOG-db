```{r}
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

`%notin%` <- Negate(`%in%`)

fancy_scientific <- function(l) {
     # turn in to character string in scientific notation
     l <- format(l, scientific = TRUE)
     # quote the part before the exponent to keep all the digits
     l <- gsub("^(.*)e", "'\\1'e", l)
 # remove + after exponent, if exists. E.g.: (3x10^+2 -> 3x10^2)
    l <- gsub("e\\+","e",l)
     # turn the 'e+' into plotmath format
     l <- gsub("e", "%*%10^", l)
 # convert 1x10^ or 1.000x10^ -> 10^
 l <- gsub("\\'1[\\.0]*\\'\\%\\*\\%", "", l)
     # return this as an expression
     parse(text=l)
}

cleanup = theme(panel.grid.major = element_blank(), 
                panel.grid.minor = element_blank(), 
                panel.background = element_blank(),
                axis.text.x=element_text(color='black',size=14),
                axis.text.y=element_text(color='black',size=14),
                panel.border=element_rect(color='black', fill=NA),
                axis.line = element_line(color ="black"),
                axis.title=element_text(size=14),
                plot.title=element_text(size=(rel(2)), hjust=0.5),
                strip.text.x = element_text(size = 14, colour = "black"),
                legend.position='top',
                legend.title=element_blank(),
                legend.text=element_text(color='black',size=14))

BLUEcleanup = theme(panel.grid.major = element_line(color="black",size=0.2), 
                panel.grid.minor = element_line(color="black",size=0.2), 
                panel.background = element_rect(fill="lightblue"),
                axis.text.x=element_text(color='black',size=14),
                axis.text.y=element_text(color='black',size=14),
                panel.border=element_rect(color='black', fill=NA),
                axis.line = element_line(color ="black"),
                axis.title=element_text(size=14),
                plot.title=element_text(size=(rel(2)), hjust=0.5),
                strip.text.x = element_text(size = 14, colour = "black"),
                legend.position="NA",
                legend.title=element_blank(),
                legend.text=element_text(color='black',size=14))


SAMPLE_KEY=fread("/work/cascades/clb21565/sample_key.csv")
```

```{r}
#pth="/work/cascades/clb21565/phase-1_mgedbs/analysis/20210601/out"
analyzeDiamondOuts=function(pth){

setwd(pth)

ls=list.files(".",pattern=".tsv")
cns <- scan(text=("qseqid sseqid slen qlen evalue bitscore length pident mismatch positive gaps qtitle stitle"), what="")

#df="/work/cascades/clb21565/phase-1_mgedbs/analysis/20210601/out/o3.faa.tsv"
  innerfx=function(df){
    tempdf=fread(as.character(df))
    
    colnames(tempdf)=cns
    pdf=tempdf
    pdf=separate(pdf,qtitle,
                 into=c("orf_info","partial",
                        "start_type","rbs",
                        "rbsspacer","gc_content"),sep="\\;")
    pdf=separate(pdf,orf_info,into=c("orf","start","stop","strand","ID"),sep="\\#")
     
    pdf$contig=gsub("opera_contig_","TEMP$",pdf$qseqid)
    pdf=separate(pdf,contig,into=c("contig","ORF_Number"),sep="\\_")
    pdf$contig=gsub("TEMP\\$","opera_contig_",pdf$contig)
    tempdf=pdf
    tempdf$Sample=gsub(".tsv","",as.character(df))
    #tempdf$Sample=gsub(".fasta_circular.fna.faa.tsv","",tempdf$Sample)
    return(tempdf)
  }
  out=ldply(lapply(ls,innerfx))
  return(out)}

processSamples=function(DMD){
 # DMD=dmds
  
  sls=unique(DMD$Sample)
  
  processMobileOGs=function(S){
  
  #S="circular.faa.tsv"
  diamond_out=DMD%>%subset(Sample==as.character(S))
  
  ls=unique(diamond_out$contig)

  innerfx=function(ctgnm){
    ctg=diamond_out%>%subset(contig==as.character(ctgnm))  
    ctg$NameTest=grepl("nm=",ctg$stitle)
    named=ctg%>%subset(NameTest==TRUE)
    named$name=gsub("nm=|\\;","",str_extract(named$stitle,"nm=(.*?)\\;"))
    named$name
    unnamed=ctg%>%subset(NameTest==FALSE)
    unnamed$name=gsub("cat=|\\;","",str_extract(unnamed$stitle,"cat=(.*?)\\;"))
    out=rbind(named,unnamed)
    out$type=gsub("type=|\\;","",str_extract(out$stitle,"type=(.*?)\\;"))
    out$stitle=gsub("cat=|\\;","",str_extract(out$stitle,"cat=(.*?)\\;"))
    out$UqID=paste(out$Sample,out$contig)
  return(out)}
  
  final_out=ldply(lapply(ls,innerfx))
  
  return(final_out)}
  
  fo=ldply(lapply(sls,processMobileOGs))
  
  return(fo)}

getElementPurity=function(Dmd_Out){
  Dmd_Out$UqID=paste(Dmd_Out$Sample,Dmd_Out$contig)
  
  PotentialMGEs=unique(Dmd_Out$UqID)
  innerfx=function(uqid){
    idf=Dmd_Out%>%subset(UqID==as.character(uqid))
    element_cts=idf%>%count(UqID,type,sort=TRUE)
    total_ctg_hits=idf%>%count(UqID,sort=TRUE)
    colnames(total_ctg_hits)=c("UqID","Total_CTG_Hits")
    MergedCts=merge(element_cts,total_ctg_hits)
    MergedCts$element_purity=(MergedCts$n/MergedCts$Total_CTG_Hits)
    return(MergedCts)
    }
    
    out_classifications=ldply(lapply(PotentialMGEs,innerfx))
    return(out_classifications)
}
```

```{r}
dpth="/work/cascades/clb21565/VCN/VRCA/OPERA/mobileOG_out"
DOs=analyzeDiamondOuts(dpth)
DOs=DOs%>%processSamples()
DOs$Sample=gsub(".tsv","",DOs$Sample)
# 
# DOs_sample_specific=DOs%>%
#   subset(Sample!="coassembly.tsv"&Sample!="rushCtgs.tsv")%>%
#   filter(grepl("opera",Sample)!=TRUE)

#Purities=DOs_sample_specific%>%getElementPurity()
Purities=DOs%>%getElementPurity()
```

```{r}
#Pure_Elements
Pure_Elements=Purities%>%
  subset(element_purity>0.75&Total_CTG_Hits>1)
Pure_Plasmids=Purities%>%
  subset(element_purity>0.75&Total_CTG_Hits>1)%>%
  subset(type=="Plasmids")
Pure_Phages=Purities%>%
  subset(element_purity>0.75&Total_CTG_Hits>1)%>%
  subset(type=="Bacteriophages")

Pure_Phages
```

```{r}
Phages=DOs%>%filter(UqID%in%Pure_Phages$UqID)
Phages$TYPE="Bacteriohage"
PhageIndividuals=merge(Phages,SAMPLE_KEY,by.x="Sample",by.y="Sample_name")
PhageIndividuals

Plasmids=DOs%>%filter(UqID%in%Pure_Plasmids$UqID)
Plasmids$TYPE="Plasmid"
PlasmidIndividuals=merge(Plasmids,SAMPLE_KEY,by.x="Sample",by.y="Sample_name")
PlasmidIndividuals

merged=rbind(PlasmidIndividuals,PhageIndividuals)

# ItemCts=merged%>%count(Sample,TYPE)
# TotalCts=merged%>%count(Sample)
# colnames(ItemCts)=gsub("^n$","n_type",colnames(ItemCts))
# merged_cts=merge(ItemCts,TotalCts)
# merged_cts$percent=((merged_cts$n_type)/merged_cts$n)
# merged_cts=merge(merged_cts,SAMPLE_KEY,by.x="Sample",by.y="Sample_name")

list_df=merged[,c("contig","TYPE","Sample")]


sampleList=unique(merged$Sample)

printSampledfs=function(s){
  tdf=list_df%>%subset(Sample==as.character(s))
  tdf_pl=tdf%>%subset(TYPE=="Plasmid")
  tdf_ph=tdf%>%subset(TYPE=="Phage")
  ph_fn=paste(as.character(unique(tdf$Sample)),".phage.txt",sep="")
  pl_fn=paste(as.character(unique(tdf$Sample)),".plasmid.txt",sep="")
  unique((tdf_pl$contig))%>%write.table(pl_fn,quote = FALSE,row.names=FALSE,col.names=FALSE)
  unique((tdf_ph$contig))%>%write.table(ph_fn,quote = FALSE,row.names=FALSE,col.names=FALSE)
  }

lapply(sampleList,printSampledfs)
```
