# mobileOG-db 
## Release name: _beatrix_ 1.0 
## ![alt text](https://i.imgur.com/PpkWCsn.jpeg)
## Description of mobileOG-db
mobileOG-db is a manually curated database of protein families mediating the integration/excision, replication/recombination/repair, stability/defense, or transfer of bacterial mobile genetic elements and phages as well as the associated transcriptional regulators of these processes. There are also a large selection of phage structural genes. 

## Usage Recommendations (for annotating full length proteins)
An example shell script and an R script used for analysis are provided (here).
Recommended workflow:
1. Annotate open reading frames of contigs/scaffolds/genomes using ORF prediction software such as prodigal (recommended)
2. Search ORFs against diamond database. _ensure that complete headers are recovered from the mobileOGs by including -outfmt 6 sseqid or stitle_
3. Merge dataframe with mobileOG metadata
4. Calculate contig-element purity and choose cut-off value. _in my experience, values of 0.75 or greater are generally reliable, but follow-up is crucial to confirm the classification_  

## Citing Us
Manuscript currently in preparation. 

## Acknowledgements 
mobileOG-db was created by merging and analyzing the contents of six complete MGE databases. The databases, and their references, are linked below. 
1. ICEBerg (ICEs, AICEs, CIMEs, IMEs): 

Meng Liu, Xiaobin Li, Yingzhou Xie, Dexi Bi, Jingyong Sun, Jun Li, Cui Tai, Zixin Deng, Hong-Yu Ou, ICEberg 2.0: an updated database of bacterial integrative and conjugative elements, Nucleic Acids Research, Volume 47, Issue D1, 08 January 2019, Pages D660–D665, https://doi.org/10.1093/nar/gky1123

2. ACLAME (various):

Leplae R, Lima-Mendez G, Toussaint A. ACLAME: a CLAssification of Mobile genetic Elements, update 2010. Nucleic Acids Res. 2010 Jan;38(Database issue):D57-61. doi: 10.1093/nar/gkp938. Epub 2009 Nov 23. PMID: 19933762; PMCID: PMC2808911.

3. GutPhage Database (Bacteriophages derived from human gut metagenomes):

Camarillo-Guerrero LF, Almeida A, Rangel-Pineros G, Finn RD, Lawley TD. Massive expansion of human gut bacteriophage diversity. Cell. 2021 Feb 18;184(4):1098-1109.e9. doi: 10.1016/j.cell.2021.01.029. PMID: 33606979; PMCID: PMC7895897.

4. Prokaryotic viral orthologous groups (pVOG) (a collection of prokaryotic virus protein HMMs):


Grazziotin AL, Koonin EV, Kristensen DM. Prokaryotic Virus Orthologous Groups (pVOGs): a resource for comparative genomics and protein family annotation. Nucleic Acids Res. 2017;45(D1):D491-D498. doi:10.1093/nar/gkw975

5. COMPASS (plasmids):


Douarre PE, Mallet L, Radomski N, Felten A, Mistou MY. Analysis of COMPASS, a New Comprehensive Plasmid Database Revealed Prevalence of Multireplicon and Extensive Diversity of IncF Plasmids. Front Microbiol. 2020;11:483. Published 2020 Mar 24. doi:10.3389/fmicb.2020.00483

7. NCBI Plasmid RefSeq (plasmids): 


O'Leary NA, Wright MW, Brister JR, et al. Reference sequence (RefSeq) database at NCBI: current status, taxonomic expansion, and functional annotation. Nucleic Acids Res. 2016;44(D1):D733-D745. doi:10.1093/nar/gkv1189
