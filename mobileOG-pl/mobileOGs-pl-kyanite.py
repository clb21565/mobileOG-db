import pandas as pd
import os
from itertools import groupby
import argparse
## author : James Mullet, Connor Brown
#Parsing Command
parser=argparse.ArgumentParser(description='parse seqs to extract taxa')
parser.add_argument("--i", type=str, required=True,
                    help="Input clust file")
parser.add_argument("--o", type=str, required=True,
                    help="Output file")
parser.add_argument("-m", type=str, required=True,
                    help="Output file")
args=parser.parse_args()
path = "."
dir_list = os.listdir(path)
file_empty=os.stat(args.i).st_size == 0

if file_empty == True:
    print("Empty diamond output. No hits returned from diamond search.")

else:
#Reads Input File and Creates New Dataframe
    df_OUT=pd.read_csv(args.i,sep="\t",header=None)
    df_OUT.columns=['Sequence Title','Query Title','Pident', 'Bitscore', 'Subject Sequence Length', 'e-value', 'Query Sequence Length', 'Start of Alignment in Subject', 'End of Alignment in Query','Start of Alignment in Query', 'End of Alignment in Query']

    #Sequence Title Columns
    df_OUT['mobileOG ID'] = df_OUT['Sequence Title'].str.split('|').str[0]
    df_OUT['Gene Name'] = df_OUT['Sequence Title'].str.split('|').str[1]
    df_OUT['Best Hit Accession ID'] = df_OUT['Sequence Title'].str.split('|').str[2]
    df_OUT['Major mobileOG Category'] = df_OUT['Sequence Title'].str.split('|').str[3]
    df_OUT['Minor mobileOG Category'] = df_OUT['Sequence Title'].str.split('|').str[4]
    df_OUT['Source Database'] = df_OUT['Sequence Title'].str.split('|').str[5]
    df_OUT['Evidence Type'] = df_OUT['Sequence Title'].str.split('|').str[6]

    #Query Title Columns
    df_OUT['Contig/ORF Name'] = df_OUT['Query Title'].str.split(' ').str[0]
    df_OUT['ORF_Start_Stop_Strands'] = df_OUT['Query Title'].str.extract(r'\#.*?(.*?)# ID=')
    df_OUT['ORF_Start'] = df_OUT['ORF_Start_Stop_Strands'].str.split(' # ').str[0]
    df_OUT['ORF_End'] = df_OUT['ORF_Start_Stop_Strands'].str.split(' # ').str[1]
    df_OUT['Sense or Antisense Strand'] = df_OUT['ORF_Start_Stop_Strands'].str.split(' # ').str[2]
    df_OUT['Prodigal ID'] = df_OUT['Query Title'].str.extract(r'\#.*?ID=(.*?);')   
    df_OUT['Prodigal Designated Contigs'] = df_OUT['Prodigal ID'].str.split('_').str[0]
    df_OUT['Unique_ORF'] = df_OUT['Prodigal ID'].str.split('_').str[1]
    df_OUT['Partial Tag'] = df_OUT['Query Title'].str.extract(r'\;partial=(.*?);')
    df_OUT['Start Codon'] = df_OUT['Query Title'].str.extract(r'\;start_type=(.*?);')
    df_OUT['RBS Motif'] = df_OUT['Query Title'].str.extract(r'\;rbs_motif=(.*?);')
    df_OUT['RBS Spacer'] = df_OUT['Query Title'].str.extract(r'\;rbs_spacer=(.*?);')
    df_OUT['GC Content'] = df_OUT['Query Title'].str.extract(r'\;gc_cont=(.*?)$')
    df_OUT['Specific Contig'] = df_OUT['Contig/ORF Name'].apply(lambda r: '_'.join(r.split('_')[:-1]))
    df_OUT["Final Sample Name"] = df_OUT["mobileOG ID"].astype(str) + "_" + df_OUT["Specific Contig"].astype(str)

    df_OUT.to_csv("{}.mobileOG.Alignment.Out.csv".format(args.o))
    #ORF Isolation
    selected_columns = df_OUT[['Specific Contig','Unique_ORF']]
    df_ORF_Temp = selected_columns.copy()
    df_ORF_Temp.drop_duplicates(subset=['Specific Contig','Unique_ORF'], keep="first", inplace=True)
    df_ORF_Temp['Amount of Unique ORFs']=df_ORF_Temp.groupby(by='Specific Contig')['Unique_ORF'].transform('count')
    final_selected_columns = df_ORF_Temp[['Specific Contig','Amount of Unique ORFs']]
    df_ORF = final_selected_columns.copy()
    df_ORF['Amount of Unique ORFs']=df_ORF['Amount of Unique ORFs'].astype(int)
    df_ORF.drop_duplicates(subset=None, keep="first", inplace=True)
    df_ORF.reset_index()

    #MetaData Analysis
    Metadata=pd.read_csv(args.m)
    Insertion_Sequences=["ISFinder"]
    Integrative_Elements=["AICE","ICE","CIME","IME","immedb"]
    Plasmids=["COMPASS","PlasmidRefSeq"]
    Multiple=["ACLAME"]
    Bacteriophages=["pVOG","GPD"]
    keys=["Insertion sequences","Integrative elements","Plasmids","Multiple","Bacteriophages"]
    values=[Insertion_Sequences,Integrative_Elements,Plasmids,Multiple,Bacteriophages]
    Elements = dict(zip(keys, values))
    Subset_Metadata=Metadata[Metadata["mobileOG Entry Name"].isin(df_OUT["mobileOG ID"])]
    Subset_Metadata=Metadata[["mobileOG Entry Name","PlasmidRefSeq","COMPASS","pVOG","immedb","ICE","IME","CIME","AICE","ISFinder","GPD","ACLAME"]]
    Subset_Metadata_long=pd.melt(Subset_Metadata, id_vars=['mobileOG Entry Name'], value_vars=["GPD","PlasmidRefSeq","COMPASS","pVOG","immedb","ICE","IME","CIME","AICE","ISFinder","ACLAME"])
    Subset_Metadata_long_matches=Subset_Metadata_long[Subset_Metadata_long["value"]>0]
    def AnnotateTypes(mobileOG_DF):
        innerdf=mobileOG_DF.copy()
        for k in keys:
            E=Elements[str(k)]
            for EX in E:
                innerdf["variable"]=innerdf["variable"].replace(str(EX),str(k))
        return(innerdf)
    ProcessedMatches=AnnotateTypes(Subset_Metadata_long_matches)
    df_OUT1=df_OUT[["mobileOG ID","Specific Contig"]]
    Processed_DF_Merge=pd.merge(df_OUT1,ProcessedMatches,left_on=df_OUT1["mobileOG ID"], right_on=ProcessedMatches["mobileOG Entry Name"], left_index=False, right_index=False)
    Out=(Processed_DF_Merge[Processed_DF_Merge["value"]>0]).groupby(["Specific Contig","variable"]).count().reset_index()

    #Final Table
    df_Purity_Final = Out.pivot(index='Specific Contig', columns='variable')['value'].fillna(0)
    df_Purity_Final=df_Purity_Final.reset_index()

    if 'Insertion sequences' not in df_Purity_Final:
        df_Purity_Final.insert(0, 'Insertion sequences', '0.0')
    if 'Bacteriophages' not in df_Purity_Final:
        df_Purity_Final.insert(0, 'Bacteriophages', '0.0')
    if 'Integrative elements' not in df_Purity_Final:
        df_Purity_Final.insert(0, 'Integrative elements', '0.0')
    if 'Plasmids' not in df_Purity_Final:
        df_Purity_Final.insert(0, 'Plasmids', '0.0')
    if 'Multiple' not in df_Purity_Final:
        df_Purity_Final.insert(0, 'Multiple', '0.0')

    df_Purity_Final['Bacteriophages'] = df_Purity_Final['Bacteriophages'].astype(float)
    df_Purity_Final['Insertion sequences'] = df_Purity_Final['Insertion sequences'].astype(float)
    df_Purity_Final['Integrative elements'] = df_Purity_Final['Integrative elements'].astype(float)
    df_Purity_Final['Plasmids'] = df_Purity_Final['Plasmids'].astype(float)
    df_Purity_Final['Multiple'] = df_Purity_Final['Multiple'].astype(float)
    df_Purity_Final['Total Number of Hits'] = df_Purity_Final['Bacteriophages']  + df_Purity_Final['Multiple'] + df_Purity_Final['Plasmids'] + df_Purity_Final['Integrative elements'] + df_Purity_Final['Insertion sequences'] 
    df_Purity_Final['Total Number of Hits'] = df_Purity_Final['Total Number of Hits'].astype(float)
    df_Purity_Final['Percent Bacteriophages'] = (df_Purity_Final['Bacteriophages'] / df_Purity_Final['Total Number of Hits']) *100
    df_Purity_Final['Percent Insertion sequences'] = (df_Purity_Final['Insertion sequences'] / df_Purity_Final['Total Number of Hits']) *100
    df_Purity_Final['Percent Integrative elements'] = (df_Purity_Final['Integrative elements'] / df_Purity_Final['Total Number of Hits']) *100
    df_Purity_Final['Percent Plasmids'] = (df_Purity_Final['Plasmids'] / df_Purity_Final['Total Number of Hits']) *100
    df_Purity_Final['Percent Multiple'] = (df_Purity_Final['Multiple'] / df_Purity_Final['Total Number of Hits']) *100
    df_Purity_Final = df_Purity_Final.sort_values(by='Total Number of Hits', ascending=True)
    #df_Purity_Final.index = df_ORF.index
    #numbers = df_ORF[["Amount of Unique ORFs"]]
    #df_Purity_Final = df_Purity_Final.join(numbers)
    #first_column = df_Purity_Final.pop('Specific Contig')
    #df_Purity_Final.insert(0, 'Specific Contig', first_column)
    #second_column = df_Purity_Final.pop('Amount of Unique ORFs')
    #df_Purity_Final.insert(1, 'Amount of Unique ORFs', second_column)
    #df_Purity_Final.reset_index()
    Final_Out=pd.merge(df_Purity_Final,df_ORF, left_on=df_Purity_Final["Specific Contig"], right_on=df_ORF["Specific Contig"], left_index=False, right_index=False)
    Final_Out.rename(columns={'key_0':'Specific Contig'}, inplace=True)
    Final_Out.drop("Specific Contig_x", axis=1, inplace=True)
    Final_Out.drop("Specific Contig_y", axis=1, inplace=True)
    Final_Out.to_csv("{}.summary.csv".format(args.o))


