#!/bin/bash
#SBATCH -t 140:00:00
#SBATCH -p normal_q
#SBATCH -A prudenlab
#SBATCH -N 1 
#SBATCH -n 24

source activate biopy 
module load parallel/20180222

#grep -vf red_terms.txt uniprot_trembl_bacteria.dat > reduced_bacterial
#split -24 reduced_bacterial 

function generecovery() {
    n=$(basename "$1")
    python get_genes.py --i $1 --o $1.tmp
}

export -f generecovery
find . -maxdepth 1 -type f -name "x*" | parallel -j 24 generecovery {}
