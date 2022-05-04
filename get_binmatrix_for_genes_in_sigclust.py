"""
script by Bethany Moore
PURPOSE:
given a cluster file, pathway file, and significant enrichment file, gets binary matrix of genes vs. cluster where 1= gene is \
significantly enriched and 0= gene not enriched in a given cluster. Gene's pathway also written as second column.
INPUT:
REQUIRED:
-cl = file with enrichment for significant clusters (from parse_enrich_get_sig_clust.py: format is filename + .fisher.pqvalue)... 
	if you want all clusters use -cl ALL
-dir = directory with cluster files where file contains: gene \t cluster
-path = file with gene, pathways: path1//path2//
OPTIONAL:
-genes = list of genes you want to extract. This option only gets a matrix that contains clusters with this list of genes
-pval = p-value cutoff for cluster significance
-qval = q-value cutoff for cluster significance
OUTPUT:
binary matrix: filename_binmatrix.txt
"""
import sys, os

GENE_LIST=[]
QVAL=""
PVAL=""

for i in range (1,len(sys.argv),2):
	if sys.argv[i] == '-cl': 
		sig_clust= sys.argv[i+1]   
		if sig_clust == "ALL":
			pass
		else:
			sig_clust_file= open(sig_clust,'r') # file with enrichment for significant clusters
	if sys.argv[i] == '-dir':
		clustdir= sys.argv[i+1] # directory with cluster files where file contains: gene \t cluster
	if sys.argv[i] == '-path':
		path_file= open(sys.argv[i+1],'r') # file with gene, pathways: path1//path2//
	if sys.argv[i] == '-genes':
		GENE_LIST= sys.argv[i+1].strip().split(',')
		GENE_LIST= [i.lower() for i in GENE_LIST]
	if sys.argv[i] == '-qval':
		QVAL= float(sys.argv[i+1])
	if sys.argv[i] == '-pval':
		PVAL= float(sys.argv[i+1])

print(GENE_LIST)


def clear_quotes(string): #returns string without quotes
	string = string.strip()
	while '"' in string:
		string = string.replace('"',"")
	return string

def get_sig_clusts(inp, D, PVAL, QVAL):
	header= inp.readline()
	for line in inp:
		L= line.strip().split('\t')
		fileinfo= L[0]
		clust= L[2]
		pval= L[8]
		qval= L[9]
		clust=clear_quotes(clust)
		clust= str(clust)
		print(clust)
		if PVAL != "":
			if float(pval) <= PVAL:
				if fileinfo not in D.keys():
					D[fileinfo]=[clust]
				else:
					D[fileinfo].append(clust)
		elif QVAL != "":
			if float(qval) <= QVAL:
				if fileinfo not in D.keys():
					D[fileinfo]=[clust]
				else:
					D[fileinfo].append(clust)
		else:
			if fileinfo not in D.keys():
				D[fileinfo]=[clust]
			else:
				D[fileinfo].append(clust)
			
	return D
	
D1={}
if sig_clust != "ALL":
	clust_dict= get_sig_clusts(sig_clust_file, D1, PVAL, QVAL)
	print(clust_dict)
	sig_clust_file.close()

def get_path_dict(inp, D):
	header= inp.readline().strip().split('\t')
	header_len= len(header)
	header_len2= header_len-2
	for line in inp:
		L= line.strip().split('\t')
		gene= L[0].split('.')[0].lower()
		gene= clear_quotes(gene)
		enzyme= [L[1]]
		if len(L)==header_len:
			data= L[2:]
		else:
			data=[]
			for i in range(header_len2):
				data.append("NA")
		data2= enzyme+data
		if gene not in D.keys():
			D[gene]=data2
		else:
			print(gene," duplicate gene")
			
	return D, header

D2={}
path_dict, pheader= get_path_dict(path_file, D2)
print(path_dict)
path_file.close()

gene_dict={}
clust_fin_list=[]
all_gene_list=[]
if sig_clust == "ALL":
	for file in os.listdir(clustdir):
		print(file)
		geneclust_file = open(clustdir+"/"+str(file))
		geneclust_dict={}
		header= geneclust_file.readline()
		if file.endswith("_default_node.txt") or file.endswith("_defaultnode.txt") or file.endswith("_defaultnode_mod.txt"):
			print(file)
			clust= str(file.split("_default")[0])
			print(clust)
			for line in geneclust_file:
				print(line)
				L= line.strip().split('\t')
				gene= L[0].split('.')[0].lower()
				gene= clear_quotes(gene)
				if clust not in geneclust_dict.keys():
					geneclust_dict[clust]=[gene]
				else:
					geneclust_dict[clust].append(gene)
		else:
			for line in geneclust_file:
				L= line.strip().split('\t')
				gene= L[0].split('.')[0].lower()
				gene= clear_quotes(gene)
				clust= str(L[1])
				if clust not in geneclust_dict.keys():
					geneclust_dict[clust]=[gene]
				else:
					geneclust_dict[clust].append(gene)
		#print(geneclust_dict)
		geneclust_file.close()
		for key in geneclust_dict.keys():
			genelist= geneclust_dict[key]
			#cluster_fin=str(file)+"_"+str(key)
			cluster_fin=str(key)
			if len(GENE_LIST)== 0:
				if cluster_fin not in clust_fin_list:
					clust_fin_list.append(cluster_fin)
				for gene in genelist:
					if gene not in gene_dict.keys():
						gene_dict[gene]=[cluster_fin]
					else:
						gene_dict[gene].append(cluster_fin)
					if gene not in all_gene_list:
						all_gene_list.append(gene)
					else:
						pass
			else:
				for gene in genelist:
					if gene in GENE_LIST:
						if cluster_fin not in clust_fin_list:
							clust_fin_list.append(cluster_fin)
						for gene in genelist:
							if gene not in gene_dict.keys():
								gene_dict[gene]=[cluster_fin]
							else:
								if cluster_fin not in gene_dict[gene]:
									gene_dict[gene].append(cluster_fin)
								else:
									pass
							if gene not in all_gene_list:
								all_gene_list.append(gene)
							else:
								pass
					else:
						pass
		
else:
	for file in clust_dict.keys():
		print(file)
		if file in os.listdir(clustdir):
			clust_list= clust_dict[file]
			print(clust_list)
			geneclust_file = open(clustdir+"/"+str(file))
			geneclust_dict={}
			header= geneclust_file.readline()
			for line in geneclust_file:
				L= line.strip().split('\t')
				gene= L[0].split('.')[0].lower()
				gene= clear_quotes(gene)
				clust= str(L[1])
				if clust not in geneclust_dict.keys():
					geneclust_dict[clust]=[gene]
				else:
					geneclust_dict[clust].append(gene)

			geneclust_file.close()
			for clust in clust_list:
				if clust in geneclust_dict.keys():
					print(clust)
					genelist= geneclust_dict[clust]
					cluster_fin=str(file)+"_"+str(clust)

					if len(GENE_LIST)== 0:
						if cluster_fin not in clust_fin_list:
							clust_fin_list.append(cluster_fin)
						for gene in genelist:
							if gene not in gene_dict.keys():
								gene_dict[gene]=[cluster_fin]
							else:
								gene_dict[gene].append(cluster_fin)
							if gene not in all_gene_list:
								all_gene_list.append(gene)
							else:
								pass
					else:
						for gene in genelist:
							if gene in GENE_LIST:
								if cluster_fin not in clust_fin_list:
									clust_fin_list.append(cluster_fin)
								for gene in genelist:
									if gene not in gene_dict.keys():
										gene_dict[gene]=[cluster_fin]
									else:
										if cluster_fin not in gene_dict[gene]:
											gene_dict[gene].append(cluster_fin)
										else:
											pass
									if gene not in all_gene_list:
										all_gene_list.append(gene)
									else:
										pass
							else:
								pass
						
						
print(gene_dict)

output= open(str(sig_clust)+"_binmatrix.txt","w")
headerstr1= "\t".join(pheader)
headerstr2= "\t".join(clust_fin_list)
output.write('%s\t%s\n' % (headerstr1,headerstr2))
pheadlen=len(pheader)-1

for gene in all_gene_list:
	gclust_list= gene_dict[gene]
	output.write("%s\t" % gene)
	if gene in path_dict.keys():
		paths= path_dict[gene]
		#print(paths)
		pathstr= "\t".join(paths)
	else:
		path1=[]
		for i in range(pheadlen):
			path1.append("NA")
		pathstr= "\t".join(path1)
	output.write("%s\t" % pathstr)
	for clust in clust_fin_list:
		if clust in gclust_list:
			output.write("1\t")
		else:
			output.write("0\t")
	output.write("\n")

output.close()
