import pandas as pd
import os
from itertools import groupby
import argparse

parser=argparse.ArgumentParser(description='parse seqs to extract taxa')
parser.add_argument("--i", type=str, required=True,
                    help="Input clust file")
parser.add_argument("--o", type=str, required=True,
                    help="Output file")
parser.add_argument("--h", type=float, required=True,
                    help="Input Hits variable")
parser.add_argument("--p", type=float, required=True,
                    help="Input Purity Variable")
args=parser.parse_args()

path = "."
dir_list = os.listdir(path)

df_OUT=pd.read_csv(args.i,sep="\t")
df_OUT.columns=['Sequence Title', 'Query Title', 'Bitscore', 'Subject Sequence Length', 'e-value', 'Query Sequence Length', 'Start of Alignment in Subject', 'End of Alignment in Query'
,'Start of Alignment in Query', 'End of Alignment in Query']

#Sequence Title Columns
df_OUT['Tentative Sequence Name'] = df_OUT['Sequence Title'].str.split('|').str[0]
df_OUT['UniProtID'] = df_OUT['Sequence Title'].str.split('|').str[2]
df_OUT['Plasmid or Phage'] = df_OUT['Sequence Title'].str.split('|').str[5]

#Query Title Columns
df_OUT['Contig/ORF Name'] = df_OUT['Query Title'].str.split(' ').str[0]

#ORF/Contig Extracted Columns
df_OUT['ORF'] = df_OUT['Contig/ORF Name'].str.split('_').str[1]
df_OUT['Specific Contig'] = df_OUT['Contig/ORF Name'].str.split('_').str[0] + "_" + df_OUT['Contig/ORF Name'].str.split('_').str[1]
df_OUT["Final Sample Name"] = df_OUT["Tentative Sequence Name"].astype(str) + "_" + df_OUT["Specific Contig"].astype(str)

#Purity Dataframe
df_Purity = df_OUT[['Specific Contig','Plasmid or Phage']].copy()
df_Purity = pd.melt(df_Purity, id_vars=['Specific Contig'], value_vars=['Plasmid or Phage']).groupby(['Specific Contig', 'value']).size().reset_index().rename(columns={'value': 'Category',0: 'Frequency'})
df_Purity_Final = df_Purity.pivot(index='Specific Contig', columns='Category')['Frequency'].fillna(0)
df_Purity_Final.sort_values(by='Specific Contig', ascending=False)
df_Purity_Final['Bacteriophage'] = df_Purity_Final['Bacteriophage'].astype(float)
df_Purity_Final['Insertion sequences'] = df_Purity_Final['Insertion sequences'].astype(float)
df_Purity_Final['Integrative elements'] = df_Purity_Final['Integrative elements'].astype(float)
df_Purity_Final['Plasmid'] = df_Purity_Final['Plasmid'].astype(float)
df_Purity_Final['Various'] = df_Purity_Final['Various'].astype(float)
df_Purity_Final['Total Number of Hits'] = df_Purity_Final['Bacteriophage'] + df_Purity_Final['Insertion sequences'] + df_Purity_Final['Integrative elements'] + df_Purity_Final['Plasmid'] + df_Purity_Final['Various']
df_Purity_Final['Total Number of Hits'] = df_Purity_Final['Total Number of Hits'].astype(float)
df_Purity_Final['Percent Bacteriophage'] = (df_Purity_Final['Bacteriophage'] / df_Purity_Final['Total Number of Hits']) *100
df_Purity_Final['Percent Insertion sequences'] = (df_Purity_Final['Insertion sequences'] / df_Purity_Final['Total Number of Hits']) *100
df_Purity_Final['Percent Integrative elements'] = (df_Purity_Final['Integrative elements'] / df_Purity_Final['Total Number of Hits']) *100
df_Purity_Final['Percent Plasmid'] = (df_Purity_Final['Plasmid'] / df_Purity_Final['Total Number of Hits']) *100
df_Purity_Final['Percent Various'] = (df_Purity_Final['Various'] / df_Purity_Final['Total Number of Hits']) *100

#Filter Dataframe
filterdf = df_Purity_Final[df_Purity_Final['Total Number of Hits'] > args.h]
filterdf = filterdf.loc[(df_Purity_Final['Percent Bacteriophage'] + df_Purity_Final['Percent Various']> float(args.p)) | (df_Purity_Final['Percent Insertion sequences'] + df_Purity_Final['Percent Various']> float(args.p)) | (df_Purity_Final['Percent Integrative elements'] + df_Purity_Final['Percent Various']> float(args.p)) | (df_Purity_Final['Percent Plasmid'] + df_Purity_Final['Percent Various']> float(args.p)) | (df_Purity_Final['Percent Various']> float(args.p))]
filterdf = filterdf.reset_index()
filterdf = pd.melt(filterdf, id_vars=['Specific Contig'], value_vars=['Percent Bacteriophage', 'Percent Insertion sequences','Percent Integrative elements','Percent Plasmid','Percent Various']).groupby(['Specific Contig','Category','value']).size().to_frame(name='').reset_index()
filterdf = filterdf.loc[filterdf.groupby('Specific Contig')['value'].idxmax()]
filterdf['Category'] = filterdf['Category'].str.split(n=1).str[1]
filterdf.to_csv("{}.csv}.format(args.o))