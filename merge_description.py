"""
Merge tableforEnrichement output file with descriptions of GO annotations


Example key for GO annotatoin: /mnt/home/azodichr/00_SideProjects/07_OrganCREs_Sahra/03_GO/gene_association_tair_modified.txt-GO_BPtermlistfromEBI_modified.txt
Example tableforEnrichement file: /mnt/home/azodichr/00_SideProjects/07_OrganCREs_Sahra/03_GO/tableforEnrichment_STE_or_cat.txt.fisher.pqvalue.sig_score


"""


import os, sys
import pandas as pd

if len(sys.argv) <= 1:
    print(__doc__)
    exit()


for i in range (1,len(sys.argv),2):
	if sys.argv[i].lower() == "-table":
		table = sys.argv[i+1]
	if sys.argv[i].lower() == "-key":
		key = sys.argv[i+1]


k = pd.read_csv(key, header=None, sep='\t')	
k.columns = ['GO', 'gene', 'desc']

t = pd.read_csv(table, header=0, sep='\t')
t['GO'], t['enrich'] = t['feature'].str.split('|', 1).str


t = t.merge(right=k, how='left', left_on='GO', right_on='GO')
t = t.drop(['GO', 'enrich', 'gene'], axis=1)
save_name = table + '.desc'

t.to_csv(save_name, index=False, header=True, sep='\t')