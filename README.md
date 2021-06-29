# mobileOG-db | Release name: beatrix-1.0 

## ![alt text](https://i.imgur.com/XMuXfit.jpeg)

## Description of mobileOG-db
mobileOG-db (for mobile orthologous groups) is a manually curated database of protein families mediating the integration/excision, replication/recombination/repair, stability/defense, or transfer of bacterial mobile genetic elements and phages as well as the associated transcriptional regulators of these processes. There are also a large selection of phage structural genes. mobileOG-db was created in a process involving more than 15,000 unique manual curation events, with 714 references and 1,116 manual functional annotations at present.  

## Description of the mobileOG-db categories
It is helpful for annotating mobile genetic elements to delineate their genes into distinctive functional modules. We identified a core set of categories, that comprise key steps of the mobile genetic element "lifestyle." 
These include 
(1) replication/recombination/repair of element nucleic acid; 
(2) stability/transfer/defense; 
(3) transfer through conjugation or natural competence; 
(4) excision/integration; 
(5) associated transcriptional regulators; 
(6) phage structural proteins.   

### Interpreting mobileOG protein headers
### ![alt_text](https://i.imgur.com/cXBPHE7.png)

mobileOG headers contain helpful information about the sequence origin, mobileOG category, element type, and annotation strategy employed in recovering the sequence, in a semi-colon separated format. Users can split this header (see example R script) to extract metadata associated with the protein sequence to aid annotation efforts.

## Usage Recommendations (for annotating full length proteins)
An example shell script and an R script used for analysis are provided (here).
Recommended workflow:
1. Annotate open reading frames of contigs/scaffolds/genomes using ORF prediction software such as prodigal (recommended)
2. Search ORFs against diamond database. _ensure that complete headers are recovered from the mobileOGs by including -outfmt 6 sseqid or stitle_
3. Merge dataframe with mobileOG metadata
4. Calculate contig-element purity and choose cut-off value. _in my experience, values of 0.75 or greater are generally reliable, but follow-up is crucial to confirm the classification_  

**Some caveats.**  

In general, it is recommended that a successful MGE detection should have multiple hits to multiple modules, all tending to agree on a consensus element type. See R scripts for tentative annotation recommendations. 

Excision/integration module hits that also have a replication tag might be housekeeping genes _xerC/xerD_ or others. Likewise, replication/recombination/repair modules alone should not be interpreted as probably MGEs.

Hits to T4SS systems in the conjugation module are not necesarrily indicative of MGEs. Paralogs are associated with virulence in some organisms.  

## Downloads 

[Stable fasta download link](https://code.vt.edu/clb21565/mobileog-db/-/raw/master/mobileOG-db_beatrix-1.0-alpha.fasta.gz) 

## Citing Us
Manuscript currently in preparation. 

## Acknowledgements 
To create mobileOG-db, we analyzed 10,776,212 proteins derived from 6 different databases of complete MGE sequences. The references to these databases are below. 

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

6. NCBI Plasmid RefSeq (plasmids): 


O'Leary NA, Wright MW, Brister JR, et al. Reference sequence (RefSeq) database at NCBI: current status, taxonomic expansion, and functional annotation. Nucleic Acids Res. 2016;44(D1):D733-D745. doi:10.1093/nar/gkv1189
