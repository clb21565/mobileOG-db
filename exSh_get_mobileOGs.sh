#!/bin/bash
#SBATCH -t 140:00:00
#SBATCH -p k80_q
#SBATCH -A prudenlab
#SBATCH -N 1 
#SBATCH -n 32

sampledir='/work/cascades/clb21565/VCN/VRCA/OPERA/out'
outdir='/work/cascades/clb21565/VCN/VRCA/OPERA/mobileOG_out'
databases='/work/cascades/clb21565/WW_Analysis/databases'
database='20210613_draft.dmnd'

mkdir $outdir 

source activate prodigal

#cd ${sampledir}
#samples=`ls *.fna | awk '{split($_,x,".fasta_circular.fna"); print x[1]}' | sort | uniq`
samples='coassembly'
for sample in $samples
do
#prodigal -i ${sample}.fasta_circular.fna -a ${sample}.faa -p meta
prodigal -i circular_HSP_contigs.fna -a coassembly.faa -p meta
done

source activate biopy

for sample in $samples
do
diamond blastp -q ${sample}.faa -d ${databases}/$database -o ${outdir}/${sample}.tsv -f 6 qseqid sseqid slen qlen evalue bitscore length pident mismatch positive gaps qtitle stitle -e 0.0000000001 --max-target-seqs 1 -p 32
done 
