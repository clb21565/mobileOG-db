import pandas as pd
import re
import os
Keywords=pd.read_csv("/work/cascades/clb21565/MGE_Keywords2.csv")
for l in Keywords.index:
    kid=Keywords[Keywords.index==l]
    substrings=kid["Include"].str.split(",")
    Term=str(kid["Keyword Key"].values[0]).replace(",","_")
    a_ls=[]
    ls=[]
    os.chdir("/work/cascades/clb21565/phase-1_mgedbs/analysis/20210518_AutomatedCategories/")
    fo=open(Term+".tsv","w")
    headers=open("/work/cascades/clb21565/phase-1_mgedbs/analysis/20210518_AutomatedCategories/dataframe_to_parse/To_Parse.tsv",'r')
    for h in headers.readlines():
        TEST=any(substring.lower() in h.lower() for substring in list(substrings)[0])
        if TEST==True: 
            fo.write(h.rstrip()+"\t"+Term+"\n")
        else:
            continue
    fo.close()
