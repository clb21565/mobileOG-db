# Description:

mobileOG-pl. v. kyanite is a preliminary mobile genetic element annotation pipeline using the mobile orthologous groups database (https://mobileogdb.flsi.cloud.vt.edu/). It takes a set of contigs or long reads as input and produces:

1)	Open reading frames using prodigal
2)	Alignment summaries to a mobile orthologous groups database file using diamond
3)	Element-mapping data summarizing matches to proteins from different element classes. 

This pipeline helps depict the frequency of MGE proteins found in contigs using mobileOGs-db. It classifies protein hit into each of the major MGE category based on mobileOG-db classification of each element. mobileOG-pl can be used as the basis for detection of any major class of bacterial MGE (i.e., plasmid, bacteriophage, insertion sequence, or integrative element) and can be complemented with other tools to achieve a fine-grained element classification. 


# Quick-start guide:
## Dependencies: 

python 3.7 with pandas, argparse, itertools

prodigal 

diamond 0.9.24 or greater

1.	 Install Conda environment:

	conda create -n mobileOG-db

	conda activate mobileOG-db

	conda install -c conda-forge biopython

	conda install -c bioconda prodigal
	
	conda install -c bioconda diamond
	
	conda install -c anaconda pandas

2.	 Download mobileOG-db (From Website)
	
		Database (mobileOG-db-beatrix-1.X.All.faa)
	
		Metadata (mobileOG-db-beatrix-1.X.All.csv)
	
		Code (mobileOGs-pl.sh and mobileOGs-pl.py)-
	
		
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
	
	-m, --metadata |  Metadata used to compare to samples
	
	-p, --pidentvalue |  Percent of Identical Matches of samples to metadata
	
	-q, --queryscore |  Percent of query coverage to sample
