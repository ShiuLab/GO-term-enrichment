# convert gene IDs from pathway file to new gene IDs

import sys,os

blast_result= open(sys.argv[1],'r')
path_result= open(sys.argv[2],'r')
out= open(str(sys.argv[2])+"_newID.txt", "w")

# get dictionary for gene IDs
def getIDs(inp,D):
	header= inp.readline()
	for line in inp:
		L=line.strip().split("\t")
		gene1= L[0]
		gene2= L[2]
		if gene1 not in D:
			D[gene1]=[gene2]
		else:
			D[gene1].append(gene2)
	return D
	
D={}
geneID_D= getIDs(blast_result,D)
print(geneID_D)

header= path_result.readline()
out.write("pathway_name\tgene2\tpathID\tgene1\n")
for line in path_result:
	L=line.strip().split("\t")
	pID= L[0]
	gene=L[1]
	pname= L[2]
	if gene in geneID_D.keys():
		genes= geneID_D[gene]
		for g in genes:
			out.write(pname+"\t"+g+"\t"+pID+"\t"+gene+"\n")
			
blast_result.close()
path_result.close()
out.close()