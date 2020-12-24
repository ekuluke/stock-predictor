
# takes a csv file from barchart.com/stocks/ nasdaq indices and prases it to get a list of symbols

import pandas as pd
import sys
def rm_arbitary(df):
    remove_words=["Corp", "Inc", "Ltd", "Company"]
    re = r'\b(?:{})\b'.format('|'.join(remove_words))
    print(re)
    df.iloc[:,1] = df.iloc[:,1].str.replace(re, '')
    print(df.iloc[:,1])
    return df
 
df = pd.read_csv(sys.argv[1], usecols=[0,1])
df = rm_arbitary(df)

   
df.to_csv("symbols&names-of" + sys.argv[1], index=False)

