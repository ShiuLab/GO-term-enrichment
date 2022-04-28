##make sure gene file is converted using mac2unix!!!!
#python gene2GOterm.py ../2-specialized_metab_project/pos-neg_genesets/secondary_metabolites-TAIRannot-glucosin.txt gene_association_tair_modified.txt GO_BPtermlistfromEBI_modified.txt 
import sys, os

gene_list = sys.argv[1] #contains gene ofinterest
assoc = open(sys.argv[2], 'r') #gene_association.tair 
#go_annot = open(sys.argv[2], 'r') #contains gene and GO term
output = str(gene_list)+".Goterm.txt" #gene of interest: GO and function 

### make gene list from data
gene_list_open = open(gene_list, 'r')

expre_gen =[]

#def add_cluster_to_dict(cluster_result, dict_cluster):
for line in gene_list_open:
    if line.startswith("AT"):
        info = line.strip().replace('"','').split("\t")
        gene = info[0]
        #pvalue = info[1]
        expre_gen.append(gene)

print (expre_gen)

gene_list_open.close()

ec_list =[]

#AraCyc ### make gene and go-term dictionary
genler_list = []
pathway = [] #GO term list

assoc_dict = {}
def get_assoc (inp, assoc_dict):
    for line in inp:
        if line.startswith('TAIR'):
            L3 = line.strip().split('\t')
            if L3[4].startswith('GO'):
                go = L3[4]
                if L3[10].startswith('AT'):
                    genelist = L3[10]
                    gene = genelist.split('|')[0]
                    if gene not in assoc_dict:
                        assoc_dict[gene] = [go]
                    else:
                        if go not in assoc_dict[gene]:
                            assoc_dict[gene].append(go)
                        else:
                            print(go, "GO already associated")

get_assoc(assoc, assoc_dict)

print (assoc_dict)
# for gene-GOpathway file
# def add_go_to_dict(go_annot, dict):
#     for line in go_annot:
#         info = line.strip().split("\t")
#         gene = info[1]
#         pathway = info[0]
#         if gene.startswith("AT"):
#             if gene not in dict:
#                 dict[pathway] = [gene]
#             else:
#                 dict[pathway].append(gene)

    
# dict = {} #dictionary should be GOterm:genes                        
# add_go_to_dict(go_annot, dict)
# go_annot.close()
assoc.close()

output_open = open(output, 'w')
output_open.write("Gene\tGOterms\n")
for gene in assoc_dict:
    if gene in expre_gen:
        go_list = assoc_dict[gene]
        datastr = ",".join(go_list)
        output_open.write("%s\t%s\n" % (gene, datastr))
        
# for go in dict:
#     gene_list_for_go = dict[go]
#     for gene in expre_gen:
#         if gene in gene_list_for_go:
#             if gene not in D:
#                 D[gene] = [go]
#             else:
#                 D[gene].append(go)
# 
# print (D)
# print (len(D.keys()))
# output_open = open(output, 'w')
# output_open.write("Gene\tGOterms\n")
# for gene in D:
#     go_list = D[gene]
#     datastr = ",".join(go_list)
#     output_open.write("%s\t%s\n" % (gene, datastr))

output_open.close()
gene_list_open.close()
#go_annot.close()