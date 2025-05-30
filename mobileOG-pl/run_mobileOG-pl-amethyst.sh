#!/bin/bash
#SBATCH --job-name=mobileOG-db
#SBATCH --time 10:00:00                         # wall clock limit
#SBATCH -p define_your_partition               # partition selection
#SBATCH -n 20                                # tasks (essentially threads)

##### This is a sample script to show how to run mobileOG-pl #####
##### This assumes you have already downloaded the conda environment - see UsageGuidance.md for details #####

### Clone GitHub ###
git clone https://github.com/clb21565/mobileOG-db

### Download Files - Use the updated version of the database and metadata (ensure you use the correct paths) ###
wget https://zenodo.org/records/14725479/files/mobileOGdb_90-2.0.fasta # mobileOG-db v2.0 database (required)
wget https://zenodo.org/records/15035032/files/250512-draft-source-label-v3.1.tsv # mobileOG-db v2.0 class labels (required)
wget https://zenodo.org/records/15035032/files/250525-mobileOG-db-2.0-md.v1.1.tsv # mobileOG-db v2.0 metadata (optional)

### Create the diamond database ###
diamond makedb --in mobileOGdb_90-2.0.fasta -d mobileOGdb_90-2.0

### Run mobileOG-pl (Use whatever version and parameters you wish to use) ###
./mobileOGs-pl-amethyst.sh -i test.fasta -d mobileOGdb_90-2.0.dmnd -m 250512-draft-source-label-v3.1.tsv -k 1 -e 1e-20 -p 60 -q 60
