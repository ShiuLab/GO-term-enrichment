#parses smart table downloaded from tomtocyc with pathway, enzymes of pathway, compounds of pathway, and synonyms as headers
#assumes table has a header
#creates a table with information for each gene: gene, pathway, pathID, synonym, evidence
import os, sys, itertools
pathway_file_all = open(sys.argv[1], 'r') # tab-delimited file from tomatocyc with pathway and genes in pathway from all tomato pathways
gene_index = int(sys.argv[2]) #what index the genes are in the plantcyc file
path_index = int(sys.argv[3]) #pathway name index
pathID_index = int(sys.argv[4]) #path ID index
#evidence_file = open(sys.argv[4], 'r') #file with evidence codes, ie. tomatocyc_genes_all_evidences.txt, where gene is 1st column, evidence is 3rd column
output = open((str(sys.argv[1]))+'.parsed.txt', 'w')

def clear_spaces(string):
	string = string.strip()
	while "  " in string:
		string = string.replace("  "," ")
	string = string.replace(" ","")
	return string
            
pathID_list= []
pthwy_dict= {}
gene_dict={}
def get_gene_pathway(inp, Dgene, Dpwy):
    for line in itertools.islice(inp, 2, None): #start at row 2
        L2 = line.strip().split('\t')
        L2_len = len(L2)
        if L2_len >= gene_index+1:
            pathway = L2[path_index]
            pathway= pathway.replace('<i>','')
            pathway= pathway.replace('</i>','')
            pathway= pathway.replace('<sup>','')
            pathway= pathway.replace('</sup>','')
            pathway= pathway.replace('"', '')
            pathway= pathway.replace(' ','_')
            pathID= clear_spaces(L2[pathID_index])
            Dpwy[pathID]=pathway
            if L2[gene_index] != '':
                genes = L2[gene_index]
                genes = clear_spaces(genes)
                gene_list = genes.strip().replace('"','').split('//')            
                gene_list = list(dict.fromkeys(gene_list)) ## removing duplicates in list
                if pathID not in Dgene:
                        Dgene[pathID] = gene_list
                else:
                        print (pathID, "pathway duplicated")

get_gene_pathway(pathway_file_all, gene_dict, pthwy_dict)

print (gene_dict, pthwy_dict)

output.write("pathID\tgene\tpathway_name\n")
for pathID in gene_dict:
    gene_list = gene_dict[pathID]
    path= pthwy_dict[pathID]
    for gene in gene_list:
        output.write("%s\t%s\t%s\n" % (pathID, gene, path))

pathway_file_all.close()
output.close()
