# mobileOGs-db _v. beatrix 1.0_ 
## Description of the mobileOGs database
The mobileOGs database is a manually curated database of protein families mediating the integration/excision, replication/recombination/repair, stability/defense, or transfer of bacterial mobile genetic elements and phages as well as associated transcriptional regulators. There are also a large selection of phage structural genes and genes mediating lysis and lysogeny. 

## Usage Recommendations
An example shell script and an R script used for analysis are provided (here).
Recommended workflow:
1. Annotate open reading frames of contigs/scaffolds/genomes using ORF prediction software such as prodigal (recommended)
2. Search ORFs against diamond database. _ensure that complete headers are recovered from the mobileOGs by including -outfmt 6 sseqid or stitle_
3. Merge dataframe with mobileOG metadata
4. Calculate contig-element purity and choose cut-off value. _in my experience, values of 0.75 or greater are generally reliable, but follow-up is crucial to confirm the ID_  
Contig classifications are now ready for subsequent analysis. 

## Acknowledgements 
