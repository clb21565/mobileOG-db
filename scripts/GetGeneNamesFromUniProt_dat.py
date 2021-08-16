import re
import argparse

parser=argparse.ArgumentParser(description='parse seqs to extract taxa')
parser.add_argument("--i", type=str, required=True,
                    help="Input clust file")
parser.add_argument("--o", type=str, required=True,
                    help="Output file")
args=parser.parse_args()

file=open(args.i,"r")
fo = open('{}.tsv'.format(args.o),'w')
for l in file.readlines():
    if l.startswith("ID"):
        ID=l.split()[1]
        #fo.write(ID+"\t")
    if (l.startswith("GN") & bool(re.findall("\\=",l))==True):
        GN=l.split()[1]
        fo.write(ID+"\t")
        out=(GN).rstrip()+"\n"
        fo.write(out)   
