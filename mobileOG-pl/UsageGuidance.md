Description:
mobileOG-pl. v. kyanite is a preliminary mobile genetic element annotation pipeline using the mobile orthologous groups database (https://mobileogdb.flsi.cloud.vt.edu/). It takes a set of contigs or long reads as input and produces:
1)	Open reading frames using prodigal
2)	Alignment summaries to a mobile orthologous groups database file using diamond
3)	Element-mapping data summarizing matches to proteins from different element classes. 

mobileOG-pl can be used as the basis for detection of any major class of bacterial MGE (i.e., plasmid, bacteriophage, insertion sequence, or integrative element) and can be complemented with other tools to achieve a fine-grained element classification.  

Dependencies: 
python 3.7 with pandas, argparse, itertools
prodigal 
diamond 0.9.24 or more greater

Quick-start guide:

conda create -n mobileOG-db
conda activate mobileOG-db
conda install -c conda-forge biopython

mkdir mobileOG-db_workdir
cd mobileOG-db_workdir

PATH_TO_DOWNLOAD=download link
wget $PATH_TO_DOWNLOAD 
DOWNLOADED_ZIP=downloaded zip file
unzip $DOWNLOADED_ZIP

conda install -c conda-forge biopython
conda install -c conda-forge biopython


1. Install Conda environment with Pandas and ArgParse:
2. Download mobileOG-db (From Website)
	Database (mobileOG-db_beatrix-1.4.faa)
	Metadata (mobileOG-db-beatrix1.4.csv)
	Code (mobileOGs-pl.sh and mobileOGs-pl.py)

mkdir mobileOG-db_workdir
cd mobileOG-db_workdir

PATH_TO_DOWNLOAD=download link
wget $PATH_TO_DOWNLOAD 
DOWNLOADED_ZIP=downloaded zip file
unzip $DOWNLOADED_ZIP

3. Make Diamond Database:
diamond makedb --in mobileOG-db_beatrix-1.4.faa -d mobileOG-db_beatrix-1.4.dmnd

4. Run Code:
conda activate mobileOG-db
./mobileOGs-pl.sh -i <contigs> -k 15 -e 1e-20 -p 90 -q 90
