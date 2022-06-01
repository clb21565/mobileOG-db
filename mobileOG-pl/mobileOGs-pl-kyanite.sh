#!/bin/bash

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


################## Code###################
for sample in $samples
do
prodigal -i ${sample} -p meta -a ${sample}.faa
diamond blastp -q ${sample}.faa --db ${DIAMOND} --outfmt 6 stitle qtitle pident bitscore slen evalue qlen sstart send qstart qend -k $KVALUE -o ${sample}.tsv -e $ESCORE --query-cover $QUERYSCORE --id $PIDENTVALUE
python mobileOGs-pl.py --o ${sample} --i ${sample}.tsv -m ${METADATA}
done

