##### mobileOG-pl v2 #####
##### Load Packages #####
import pandas as pd
import os
from itertools import groupby
import argparse

##### Authors : James I. Mullet, Connor L. Brown #####

##### Define Arg Parse Script #####
def parse_args():
    parser = argparse.ArgumentParser(description='parse sequences to obtain hits')
    parser.add_argument('--i', type=str, required=True, help='Path to the blast input files')
    parser.add_argument('--o', type=str, required=True, help='file name')
    parser.add_argument('--m', type=str, required=True, help='Path to the metadata file')
    return parser.parse_args()

##### Load Metadata File #####
def load_metadata(metadata_file):
    metadata_df=pd.read_csv(metadata_file,sep="\t")
    metadata_df = metadata_df.rename(columns={'mobileOG': 'mobileOG_ID'})

    metadata_df['suggested_label']=metadata_df['suggested_label'].str.replace('conjugative element','conjugative_element')

    # filtered_df=metadata_df[metadata_df['Evidence']=='HC-pLLM']
    # filtered_df=filtered_df[filtered_df['Database']!='phage']
    return metadata_df

##### Load Blast Output File #####
def load_blast_input(input_blast_file):
    # Check to make sure file is not empty #
    file_empty=os.stat(input_blast_file).st_size == 0
    if file_empty == True:
        print("Empty diamond output. No hits returned from diamond search.")
    
    # Read Input File and Creates Dataframe #
    else:
        # Load File #
        df_OUT=pd.read_csv(input_blast_file,sep="\t",header=None,names=['sequence_title','query_title','pident', 'bitscore', 'subject_sequence_length', 'e_value', 'query_sequence_length', 'start_of_alignment_in_subject', 'end_of_alignment_in_subject','start_of_alignment_in_query', 'end_of_alignment_in_query'])

        # Extract data from sequence_title column #
        sequence_col_names =['mobileOG_ID','gene_name','best_hit_accession_ID','major_mobileOG_category','minor_mobileOG_category','source_database','evidence_type']
        df_OUT[sequence_col_names] = df_OUT['sequence_title'].str.split("|",expand=True)
        
        # Extract data from query_title column #
        query_col_names_temp =['protein_identifier','start','stop','strand','attributes']
        df_OUT[query_col_names_temp] = df_OUT['query_title'].str.split(" # ",expand=True)

        # Need to do this twice due to naming of query_title #
        split_attributes=df_OUT['attributes'].str.split(';',expand=True)
        # attribute_dict=split_attributes.applymap(lambda x:x.split('=')[1] if '=' in x else None)
        attribute_dict=split_attributes.apply(lambda col: col.map(lambda x: x.split('=')[1] if '=' in x else None))

        attribute_dict.columns =['prodigal_ID','partial_tag','start_codon','rbs_motif','rbs_spacer','gc_content']

        # Merge blast df with attributes dict #
        merged_df=pd.concat([df_OUT,attribute_dict],axis=1)
        merged_df=merged_df.drop(columns=['attributes'])
        merged_df['prodigal_designated_contigs'] = merged_df['prodigal_ID'].str.split('_').str[0]
        merged_df['unique_ORF'] = merged_df['prodigal_ID'].str.split('_').str[1]
        merged_df['specific_contig'] = merged_df['protein_identifier'].apply(lambda r: '_'.join(r.split('_')[:-1]))
        
    return merged_df

##### Count number of ORFs per contig/genome #####
def count_ORFs(blast_input):
    # Subset blast input file #
    mini_blast_input_temp = blast_input[['specific_contig','unique_ORF']]
    mini_blast_input=mini_blast_input_temp.drop_duplicates(subset=['specific_contig','unique_ORF'], keep="first")

    # Count number of unique ORFs per genome/contig #
    mini_blast_input['number_of_unique_ORFs']=mini_blast_input.groupby('specific_contig')['unique_ORF'].transform('count')
    df_ORF=mini_blast_input.drop(columns=['unique_ORF'])
    df_ORF['number_of_unique_ORFs']=df_ORF['number_of_unique_ORFs'].astype(int)
    df_ORF.drop_duplicates(subset=None, keep="first", inplace=True)

    return df_ORF

##### Merge metadata and mobileOG-db results #####
def merge_output(blast_input,metadata_df):
    
    # Merge the metadata and mobileOG-db output #
    temp_df=pd.merge(blast_input,metadata_df,how='inner',on='mobileOG_ID')
    
    # Remove unnecessary columns #
    mini_df=temp_df[['specific_contig','mobileOG_ID','Name','Major mobileOG Category','suggested_label']]

    # Group the protein hits per MGE type #
    grouped_df=mini_df.groupby('specific_contig')['suggested_label'].value_counts().reset_index(name='protein_counts')

    # Obtain the total protein hits per contig/genome #
    grouped_df['total_protein_hits']=grouped_df.groupby('specific_contig')['protein_counts'].transform("sum")

    # Obtain percent of proteins from each MGE class #
    grouped_df['percent'] = (grouped_df['protein_counts'] / grouped_df['total_protein_hits'])*100
    
    # Ensure all contigs/genomes contain all MGE categories - set count at 0 if not present #
    MGE_classes=['virus','plasmid','conjugative_element','recombination']
    
    contigs = grouped_df['specific_contig'].unique()

    all_combinations = pd.MultiIndex.from_product(
        [contigs,MGE_classes],
        names=['specific_contig','suggested_label']
    )

    updated_grouped_df = grouped_df.set_index(['specific_contig','suggested_label']).reindex(all_combinations,fill_value=0).reset_index()

    long_df = updated_grouped_df.melt(id_vars=['specific_contig','suggested_label'],value_vars=['protein_counts','percent'],var_name='data_type',value_name='data_value')

    long_df['grouped_name'] =  long_df['data_type'] +'_'+ long_df['suggested_label']

    cleaned_df=long_df.pivot(index='specific_contig',columns='grouped_name',values='data_value').fillna(0).astype(float)
    # cleaned_df = grouped_df.pivot(index=['specific_contig','total_protein_hits'],columns='suggested_label',values='counts').fillna(0).astype(int)
    cleaned_df.columns.name = None
    cleaned_df=cleaned_df.reset_index()

    return cleaned_df

##### Main function call #####
def main():
    ### Define variables ###
    args = parse_args()
    input_blast_file=args.i
    filename=args.o
    metadata_file=args.m

    ### Load Metadata File ###
    metadata_df=load_metadata(metadata_file)
    # metadata_df.to_csv('temp_metadata.csv',index=False)
    # print(metadata_df)

    ### Load Blast Input ###
    blast_input=load_blast_input(input_blast_file)
    # print(blast_input)

    # Save blast output #
    subsetted_filename = f'{filename}.mobileOG.Alignment.Out.csv'
    blast_input.to_csv(subsetted_filename,index=False)

    ### Count ORFs per contig ###
    orf_output=count_ORFs(blast_input)
    # print(orf_output)

    ### Merge metadata and mobileOG output files ###
    cleaned_df=merge_output(blast_input,metadata_df)
    print(cleaned_df)

    # Save blast output #
    subsetted_overview_filename = f'{filename}_temp_summary.csv'
    cleaned_df.to_csv(subsetted_overview_filename,index=False)

if __name__ == "__main__":
    main()
