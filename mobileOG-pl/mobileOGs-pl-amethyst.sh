#!/bin/bash
# mobileOG-pl v2 #

#Parsing Command
POSITIONAL=()
while [[ $# -gt 0 ]]; do
  key="$1"

    case $key in
    -i|--input)
      samples="$2"
      shift
      shift
      ;;
    -k|--kvalue)
      KVALUE="$2"
      shift # past argument
      shift # past value
      ;;
    -e|--escore)
      ESCORE="$2"
      shift # past argument
      shift # past value
      ;;
    -p|--pidentvalue)
      PIDENTVALUE="$2"
      shift # past argument
      shift # past value
      ;;
    -d|--db)
      DIAMOND="$2"
      shift # past argument
      shift # past value
      ;;
    -q|--queryscore)
      QUERYSCORE="$2"
      shift # past argument
      shift # past value
      ;;
    -m|--metadata)
      METADATA="$2"
      shift # past argument
      shift # past value
      ;;
     esac
done

set -- "${POSITIONAL[@]}"
if [[ -n $1 ]]; then
    echo "Last line of file specified as non-opt/last argument:"
    tail -1 "$1"
fi


################## Code ###################
for sample in $samples
do
  echo "Begin processing $sample"

  ##### Convert Nucleotide Sequences to Proteins #####
  prodigal -i ${sample} -p meta -a ${sample}.faa

  ##### Blast Proteins against mobileOG-db v2.0 #####
  diamond blastp -q ${sample}.faa --db ${DIAMOND} --outfmt 6 stitle qtitle pident bitscore slen evalue qlen sstart send qstart qend -k $KVALUE -o ${sample}.tsv -e $ESCORE --query-cover $QUERYSCORE --id $PIDENTVALUE

  ##### Parse Blast Results to obtain hits to mobileOG-db #####
  python mobileOGs-pl-amethyst.py --o ${sample} --i ${sample}.tsv --m ${METADATA}
  
  echo "Finished processing $sample"
done
