# November 2022 Update - Getting Element Classifications for Individual mobileOGs
We have now added reproducible [R code](https://github.com/clb21565/mobileOG-db/blob/main/scripts/getElementClassifications.R) for producing element labels for mobileOGs using just the metadata (.csv) file. The resulting metadata can be accessed [here](https://drive.google.com/file/d/1tm1JfQ1uorvbJVKULSDWleq6r_pfpxZh/view?usp=share_link). This metadata file can be used to provide classification to contigs, as in the figure here: 

![image](https://user-images.githubusercontent.com/35241700/200654054-c8eae8f2-e73a-4000-ab07-c08667b436fe.png)


# Description:

mobileOG-pl. v. kyanite is a lightweight mobile genetic element annotation pipeline using the mobile orthologous groups database (https://mobileogdb.flsi.cloud.vt.edu/). It takes a set of contigs or long reads as input and produces:

1)	Open reading frames using prodigal
2)	Alignment summaries to a mobile orthologous groups database file using diamond
3)	Element-mapping data summarizing matches to proteins from different element classes. 

This pipeline reports the presence of MGE proteins in a set of contigs using mobileOG-db annotations. It provides protein hit classifications as being putatively derived from plasmid, phage, insertion sequences, and/or integrative genomic element. Thus, mobileOG-pl can be used as the basis for detection of any major class of bacterial MGE and can be complemented with other tools to achieve a fine-grained element classification. 



# Quick-start guide:
## Dependencies: 

python 3.6.15 with pandas, argparse, itertools

prodigal 

diamond 0.9.24 or greater

1.	 Install Conda environment:

	conda create -n mobileOG-db python=3.6.15

	conda activate mobileOG-db

	conda install -c conda-forge biopython

	conda install -c bioconda prodigal
	
	conda install -c bioconda diamond
	
	conda install -c anaconda pandas

2.	 Download mobileOG-db (From Website)
	
		Database (mobileOG-db-beatrix-1.X.All.faa)
	
		Metadata (mobileOG-db-beatrix-1.X.All.csv)
	
		Code (mobileOGs-pl-kyanite.sh and mobileOGs-pl-kyanite.py)
	
		
	mkdir mobileOG-db_workdir
	cd mobileOG-db_workdir
	
	chmod +x mobileOGs-pl-kyanite.sh
	
	PATH_TO_DOWNLOAD=download link

	wget $PATH_TO_DOWNLOAD 

	DOWNLOADED_ZIP=downloaded zip file

	unzip $DOWNLOADED_ZIP

3. 	Make Diamond Database:

	diamond makedb --in mobileOG-db-beatrix-1.X.All.faa -d mobileOG-db-beatrix-1.X.dmnd

4. 	Run Code (example of stringent settings):

	conda activate mobileOG-db
	
	./mobileOGs-pl-kyanite.sh -i test.fasta -d mobileOG-db-beatrix-1.X.dmnd -m mobileOG-db-beatrix-1.X.All.csv -k 15 -e 1e-20 -p 90 -q 90
	
5. 	Usage:

	-i, --input | Input Fasta File
	
	-k , --kvalue | Number of Diamond Alignments to Report
	
	-e, --escore | Maximum E-score
	
	-d, --db | Diamond Database
	
	-m, --metadata |  mobileOG-db metadata (csv file) used to compare to samples
	
	-p, --pidentvalue |  Percent of Identical Matches of samples to metadata
	
	-q, --queryscore |  Percent of query coverage to sample
