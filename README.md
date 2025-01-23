# mobileOG-db 2.0 | Janurary 2025 pre-release notes
Hi there, thanks for using mobileOG-db 1.6. We're quite excited to introduce you to mobileOG-db 2.0, but, first we wanted to drop a pre-release so folks can try it out and provide any feedback they might have. The newest version can be accessed on [zenodo](https://zenodo.org/records/14725479). 

Major changes in mobileOG-db 2.0:
1) **Removed problematic protein families** (e.g., transcriptional regulators with limited functional annotations and chaperone proteins)
2) **Expanded coverage of environmental sequences** through protein large language model searches of IMG/VR and IMG/PR
3) **Increased curation of recombinase names**
4) **Unambiguous element class labels** of plasmid, conjugative element, recombination, and phage.

   
Overall, we increased the database size by about 10-fold with the most dramatic increase being to phage protein sequences. 

# mobileOG-db | Release name: beatrix-1.6

## ![alt text](https://i.imgur.com/XMuXfit.jpeg)
## Description of mobileOG-db
mobileOG-db (for mobile orthologous groups) is a manually curated database of protein families mediating the integration/excision, replication/recombination/repair,
stability/defense, or transfer of bacterial mobile genetic elements and phages as well as the associated transcriptional regulators of these processes. mobileOG-db was created
in a process involving more than 15,000 unique manual curation events, with 1,558 references and 2,444 unique manual functional annotations at present.

## mobileOG-db now on prokksee: visualize the presence of mobileOGs on contigs or whole genomes 
![Untitled-1-01](https://user-images.githubusercontent.com/35241700/205512402-a1dccc53-3e7c-4dda-b540-55ddfe995548.png)


Thanks to Dr. Jason Grant for his work getting mobileOG-db available on https://proksee.ca/



## Try mobileOG-pl, a pipeline to detect and categorize bacterial mobile genetic elements from contigs or long reads. 
https://github.com/clb21565/mobileOG-db/blob/main/mobileOG-pl/UsageGuidance.md

## Downloads 
The current version of the database can be browsed accessed through its website: 
https://mobileogdb.flsi.cloud.vt.edu/

## Contact Us

connorleebrown@gmail.com, mobileogdbsupport@vt.edu

## Citing Us

Brown CL, Mullet J, Hindi F, Stoll JE, Gupta S, Choi M, Keenum I, Vikesland P, Pruden A, Zhang L. mobileOG-db: a Manually Curated Database of Protein Families Mediating the Life Cycle of Bacterial Mobile Genetic Elements. Appl Environ Microbiol. 2022 Aug 29:e0099122. doi: 10.1128/aem.00991-22. Epub ahead of print. PMID: 36036594.

## Acknowledgements 
To create mobileOG-db, we analyzed 10,776,212 proteins derived from 8 different databases of complete MGE sequences. The references to these databases are below. 

**1. ICEBerg (ICEs, AICEs, CIMEs, IMEs):**

Meng Liu, Xiaobin Li, Yingzhou Xie, Dexi Bi, Jingyong Sun, Jun Li, Cui Tai, Zixin Deng, Hong-Yu Ou, ICEberg 2.0: an updated database of bacterial integrative and conjugative elements, Nucleic Acids Research, Volume 47, Issue D1, 08 January 2019, Pages D660–D665, https://doi.org/10.1093/nar/gky1123

**2. ACLAME (various):**

Leplae R, Lima-Mendez G, Toussaint A. ACLAME: a CLAssification of Mobile genetic Elements, update 2010. Nucleic Acids Res. 2010 Jan;38(Database issue):D57-61. doi: 10.1093/nar/gkp938. Epub 2009 Nov 23. PMID: 19933762; PMCID: PMC2808911.

**3. GutPhage Database (Bacteriophages derived from human gut metagenomes):**

Camarillo-Guerrero LF, Almeida A, Rangel-Pineros G, Finn RD, Lawley TD. Massive expansion of human gut bacteriophage diversity. Cell. 2021 Feb 18;184(4):1098-1109.e9. doi: 10.1016/j.cell.2021.01.029. PMID: 33606979; PMCID: PMC7895897.

**4. Prokaryotic viral orthologous groups (pVOG) (a collection of prokaryotic virus protein HMMs):**


Grazziotin AL, Koonin EV, Kristensen DM. Prokaryotic Virus Orthologous Groups (pVOGs): a resource for comparative genomics and protein family annotation. Nucleic Acids Res. 2017;45(D1):D491-D498. doi:10.1093/nar/gkw975

**5. COMPASS (plasmids):**


Douarre PE, Mallet L, Radomski N, Felten A, Mistou MY. Analysis of COMPASS, a New Comprehensive Plasmid Database Revealed Prevalence of Multireplicon and Extensive Diversity of IncF Plasmids. Front Microbiol. 2020;11:483. Published 2020 Mar 24. doi:10.3389/fmicb.2020.00483

**6. NCBI Plasmid RefSeq (plasmids):**

O'Leary NA, Wright MW, Brister JR, et al. Reference sequence (RefSeq) database at NCBI: current status, taxonomic expansion, and functional annotation. Nucleic Acids Res. 2016;44(D1):D733-D745. doi:10.1093/nar/gkv1189

**7. **immedb (integrative elements):****

Jiang,X., Hall,A.B., Xavier,R.J. and Alm,E.J. (2019) Comprehensive analysis of chromosomal
mobile genetic elements in the gut microbiome reveals phylum-level niche-adaptive
gene pools. PLoS One, 14, e0223680.

**8. ISfinder (insertion sequences):**

Siguier P, Perochon J, Lestrade L, Mahillon J, Chandler M. ISfinder: the reference centre for bacterial insertion sequences. Nucleic Acids Res. 2006 Jan 1;34(Database issue):D32-6. doi: 10.1093/nar/gkj014. PMID: 16381877; PMCID: PMC1347377.
