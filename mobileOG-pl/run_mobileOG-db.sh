#!/bin/bash
#SBATCH --job-name=mobileOG-db
#SBATCH --time 10:00:00                         # wall clock limit
#SBATCH -p mit_normal               # partition selection
#SBATCH -n 20                                # tasks (essentially threads)

# source activate mobileOG-db

# ./mobileOGs-pl-kyanite.sh -i contig_11_real_one.fasta -d mobileOG-db-beatrix-1.6.dmnd -m mobileOG-db-beatrix-1.6-All.csv -k 1 -e 1e-20 -p 50 -q 40

# ./mobileOGs-pl-kyanite.sh -i contig_11_real_one.fasta -d mobileOGdb_90-2.0.dmnd -m 250512-draft-source-label-v3.1.tsv -k 1 -e 1e-20 -p 50 -q 40

./mobileOGs-pl-kyanite.sh -i updated_training_phage_plasmids.fasta -d mobileOGdb_90-2.0.dmnd -m 250512-draft-source-label-v3.1.tsv -k 1 -e 1e-20 -p 50 -q 40

# wget https://zenodo.org/records/15035032/files/250525-mobileOG-db-2.0-md.v1.1.tsv
# wget https://zenodo.org/records/15035032/files/250512-draft-source-label-v3.1.tsv
# wget https://zenodo.org/records/14725479/files/mobileOGdb_90-2.0.fasta
# wget https://zenodo.org/records/15035011/files/250316-mobileOG-db_2.0_updated-metadata.tsv
# diamond makedb --in mobileOGdb_90-2.0.fasta -d mobileOGdb_90-2.0