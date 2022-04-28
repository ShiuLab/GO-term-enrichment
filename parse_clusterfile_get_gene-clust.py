## get clusters for specific genes
## INPUTS:
## a comma separate list of genes that you are interested in
## full cluster file
## OUTPUT:
## gene:cluster file with clusters containing your genes of interest

import sys, os
genelist= sys.argv[1].split(",")
clusterfile= open(sys.argv[2],'r')
output= open(sys.argv[3],'w')

#function to remove quotes and space
def clear_space(string): #returns tab-delimited
	string = string.strip()
	while "  " in string:
		string = string.replace("  "," ")
	string = string.replace(" ","")
	while '"' in string:
		string = string.replace('"','')
	return (string)

#get genes in cluster file
def get_genes(inp):
	inp.readline()
	D={}
	for line in inp:
		L= line.strip().split('\t')
		gene= L[0].split('.')[0].lower()
		gene= clear_space(gene)
		cluster= int(L[1])
		if cluster not in D:
			D[cluster]=[gene]
		else:
			D[cluster].append(gene)
	return D
	
clustd= get_genes(clusterfile)

print("number of clusters found in file",len(clustd.keys()))

output.write("gene\tcluster\n")
for clust in clustd:
	genes= clustd[clust]
	for g in genelist:
		g= g.strip().split('.')[0].lower()
		g= clear_space(g)
		#print(g)
		if g in genes:
			for g1 in genes:
				output.write('%s\t%s\n' % (g1,clust))
		else:
			pass
			
output.close()
clusterfile.close()