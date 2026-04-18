import pandas as pd
import os
import argparse

# Parsing Command
parser = argparse.ArgumentParser(description='parse seqs to extract taxa')
parser.add_argument("--i", type=str, required=True,
                    help="Input clust file")
parser.add_argument("--o", type=str, required=True,
                    help="Output file")
parser.add_argument("-m", type=str, required=True,
                    help="Metadata file")
args = parser.parse_args()

file_empty = os.stat(args.i).st_size == 0

if file_empty:
    print("Empty diamond output. No hits returned from diamond search.")

else:
    # Reads Input File and Creates New Dataframe
    cols = ['Sequence Title', 'Query Title', 'Pident', 'Bitscore',
            'Subject Sequence Length', 'e-value', 'Query Sequence Length',
            'Start of Alignment in Subject', 'End of Alignment in Subject',
            'Start of Alignment in Query', 'End of Alignment in Query']
    df_OUT = pd.read_csv(args.i, sep="\t", header=None, names=cols, dtype=str)

    # Sequence Title Columns - vectorized split in one pass
    seq_cols = ['mobileOG ID', 'Gene Name', 'Best Hit Accession ID',
                'Major mobileOG Category', 'Minor mobileOG Category',
                'Source Database', 'Evidence Type']
    df_OUT[seq_cols] = df_OUT['Sequence Title'].str.split('|', expand=True).iloc[:, :7]

    # Query Title Columns
    df_OUT['Contig/ORF Name'] = df_OUT['Query Title'].str.split(' ', expand=True).iloc[:, 0]
    df_OUT['ORF_Start_Stop_Strands'] = df_OUT['Query Title'].str.extract(r'\#.*?(.*?)# ID=')

    orf_parts = df_OUT['ORF_Start_Stop_Strands'].str.split(' # ', expand=True)
    df_OUT['ORF_Start'] = orf_parts[0]
    df_OUT['ORF_End'] = orf_parts[1]
    df_OUT['Sense or Antisense Strand'] = orf_parts[2]

    df_OUT['Prodigal ID'] = df_OUT['Query Title'].str.extract(r'\#.*?ID=(.*?);')
    df_OUT['Prodigal Designated Contigs'] = df_OUT['Prodigal ID'].str.split('_', expand=True).iloc[:, 0]
    df_OUT['Unique_ORF'] = df_OUT['Prodigal ID'].str.split('_', expand=True).iloc[:, 1]
    df_OUT['Partial Tag'] = df_OUT['Query Title'].str.extract(r'\;partial=(.*?);')
    df_OUT['Start Codon'] = df_OUT['Query Title'].str.extract(r'\;start_type=(.*?);')
    df_OUT['RBS Motif'] = df_OUT['Query Title'].str.extract(r'\;rbs_motif=(.*?);')
    df_OUT['RBS Spacer'] = df_OUT['Query Title'].str.extract(r'\;rbs_spacer=(.*?);')
    df_OUT['GC Content'] = df_OUT['Query Title'].str.extract(r'\;gc_cont=(.*?)$')

    # Critical bottleneck fix: replace row-wise apply with vectorized rsplit
    df_OUT['Specific Contig'] = df_OUT['Contig/ORF Name'].str.rsplit('_', n=1).str[0]
    df_OUT["Final Sample Name"] = df_OUT["mobileOG ID"] + "_" + df_OUT["Specific Contig"]

    df_OUT.to_csv("{}.mobileOG.Alignment.Out.csv".format(args.o), index=False)

    # ORF Isolation - simplified: nunique replaces drop_duplicates + groupby transform
    df_ORF = (df_OUT.groupby('Specific Contig')['Unique_ORF']
                    .nunique()
                    .reset_index(name='Amount of Unique ORFs'))

    # MetaData Analysis
    Metadata = pd.read_csv(args.m, dtype=str)

    Insertion_Sequences = ["ISFinder"]
    Integrative_Elements = ["AICE", "ICE", "CIME", "IME", "immedb"]
    Plasmids = ["COMPASS", "PlasmidRefSeq"]
    Multiple = ["ACLAME"]
    Bacteriophages = ["pVOG", "GPD"]
    keys = ["Insertion sequences", "Integrative elements", "Plasmids", "Multiple", "Bacteriophages"]
    values = [Insertion_Sequences, Integrative_Elements, Plasmids, Multiple, Bacteriophages]
    Elements = dict(zip(keys, values))

    # Original line 75 was overwritten by line 76; we keep only the column subset
    meta_cols = ["mobileOG Entry Name", "PlasmidRefSeq", "COMPASS", "pVOG", "immedb",
                 "ICE", "IME", "CIME", "AICE", "ISFinder", "GPD", "ACLAME"]
    Subset_Metadata = Metadata[meta_cols]

    value_vars = ["GPD", "PlasmidRefSeq", "COMPASS", "pVOG", "immedb",
                  "ICE", "IME", "CIME", "AICE", "ISFinder", "ACLAME"]
    Subset_Metadata_long = pd.melt(
        Subset_Metadata,
        id_vars=['mobileOG Entry Name'],
        value_vars=value_vars
    )

    Subset_Metadata_long['value'] = pd.to_numeric(Subset_Metadata_long['value'], errors='coerce')
    Subset_Metadata_long_matches = Subset_Metadata_long[Subset_Metadata_long["value"] > 0]

    # Replace nested loops with a flat mapping dictionary + vectorized replace
    flat_map = {ex: k for k, v in Elements.items() for ex in v}
    ProcessedMatches = Subset_Metadata_long_matches.copy()
    ProcessedMatches["variable"] = ProcessedMatches["variable"].replace(flat_map)

    df_OUT1 = df_OUT[["mobileOG ID", "Specific Contig"]]
    Processed_DF_Merge = pd.merge(
        df_OUT1, ProcessedMatches,
        left_on="mobileOG ID", right_on="mobileOG Entry Name"
    )

    Out = (Processed_DF_Merge[Processed_DF_Merge["value"] > 0]
           .groupby(["Specific Contig", "variable"])
           .size()
           .reset_index(name='value'))

    # Final Table
    df_Purity_Final = Out.pivot(index='Specific Contig', columns='variable', values='value').fillna(0)
    df_Purity_Final = df_Purity_Final.reset_index()

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
    df_Purity_Final['Total Number of Hits'] = (
        df_Purity_Final['Bacteriophages'] + df_Purity_Final['Multiple'] +
        df_Purity_Final['Plasmids'] + df_Purity_Final['Integrative elements'] +
        df_Purity_Final['Insertion sequences']
    )
    df_Purity_Final['Total Number of Hits'] = df_Purity_Final['Total Number of Hits'].astype(float)

    total = df_Purity_Final['Total Number of Hits']
    df_Purity_Final['Percent Bacteriophages'] = (df_Purity_Final['Bacteriophages'] / total * 100).fillna(0)
    df_Purity_Final['Percent Insertion sequences'] = (df_Purity_Final['Insertion sequences'] / total * 100).fillna(0)
    df_Purity_Final['Percent Integrative elements'] = (df_Purity_Final['Integrative elements'] / total * 100).fillna(0)
    df_Purity_Final['Percent Plasmids'] = (df_Purity_Final['Plasmids'] / total * 100).fillna(0)
    df_Purity_Final['Percent Multiple'] = (df_Purity_Final['Multiple'] / total * 100).fillna(0)

    df_Purity_Final = df_Purity_Final.sort_values(by='Total Number of Hits', ascending=True)

    # Merge with ORF counts using clean 'on=' syntax
    Final_Out = pd.merge(df_Purity_Final, df_ORF, on="Specific Contig")
    Final_Out.to_csv("{}.summary.csv".format(args.o), index=False)
