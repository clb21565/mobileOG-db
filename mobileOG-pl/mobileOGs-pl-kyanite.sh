#!/bin/bash

usage() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -i, --input         Input nucleotide FASTA file (required)"
    echo "  -o, --out           Output directory (default: current directory)"
    echo "  --faa               Input protein FASTA file (pre-predicted by prodigal)."
    echo "                      When provided, prodigal prediction is skipped."
    echo "  -k, --kvalue        Number of Diamond alignments to report"
    echo "  -e, --escore        Maximum E-score"
    echo "  -p, --pidentvalue   Percent of identical matches"
    echo "  -d, --db            Diamond database"
    echo "  -q, --queryscore    Percent of query coverage"
    echo "  -m, --metadata      mobileOG-db metadata (csv file) used to compare to samples"
    echo "  -h, --help          Show this help message"
    exit 0
}

#Defaults
OUTDIR="."

#Parsing Command
POSITIONAL=()
while [[ $# -gt 0 ]]; do
  key="$1"

    case $key in
    -h|--help)
      usage
      ;;
    -i|--input)
      samples="$2"
      shift
      shift
      ;;
    -o|--out)
      OUTDIR="$2"
      shift
      shift
      ;;
    --faa)
      FAA="$2"
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

if [[ -z "$samples" ]]; then
    echo "Error: -i/--input is required. Use -h for help." >&2
    exit 1
fi

mkdir -p "$OUTDIR"

################## Code###################
for sample in $samples
do
  BASENAME=$(basename "$sample")
  if [[ -n "$FAA" ]]; then
    sample_faa="$FAA"
  else
    sample_faa="${OUTDIR}/${BASENAME}.faa"
    prodigal -i ${sample} -p meta -a ${sample_faa}
  fi
  diamond blastp -q ${sample_faa} --db ${DIAMOND} --outfmt 6 stitle qtitle pident bitscore slen evalue qlen sstart send qstart qend -k $KVALUE -o ${OUTDIR}/${BASENAME}.tsv -e $ESCORE --query-cover $QUERYSCORE --id $PIDENTVALUE
  python mobileOGs-pl-kyanite.py --o ${OUTDIR}/${BASENAME} --i ${OUTDIR}/${BASENAME}.tsv -m ${METADATA}
done

