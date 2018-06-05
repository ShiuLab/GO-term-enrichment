import sys, os
#python cluster_enrichment_031814_2.py clusterfile Go-annotfile outputfile
cluster_result = sys.argv[1] #contains gene: cluster
go_annot = open(sys.argv[2], 'r') #contains GO term: gene or pathway info- gene:pathway
#genenum= int(sys.argv[3]) #number of genes in total for A. thaliana this is 27511


### make gene and cluster dictionary
cluster_result_open = open(cluster_result, 'r')
line = cluster_result_open.readline()
line = cluster_result_open.readline()
expre_gen =[]
dict_cluster = {}
#clear spaces
def clear_space(string): #returns tab-delimited
	string = string.strip()
	while "  " in string:
		string = string.replace("  "," ")
	string = string.replace(" ","_")
	return (string)

#make dictionary with cluster as key and genes as items for each cluster:
while line:
    info = line.strip().replace('"','').split('\t')
    if len(info) >= 2:
        gene = info[0]
        
        gene= gene.split('.')[0] #added for cucumber genes
        #genel2= (genel[0],genel[1])
        #print (genel2)
        #gene= '.'.join(genel2)
        
        cluster = info[1]
        cluster = clear_space(cluster)
        if gene not in expre_gen:
            expre_gen.append(gene)
        else:
            pass
        if cluster in dict_cluster:
            if gene not in dict_cluster[cluster]:
                dict_cluster[cluster].append(gene)
            else:
                pass
        else:
            dict_cluster[cluster] = [gene]
        line = cluster_result_open.readline()
    else:
        line = cluster_result_open.readline()

#print (dict_cluster)

#AraCyc ### make gene and go-term dictionary
genler_list = []
pathway = [] #GO term list


def add_go_to_dict(go_annot, dict, expre_gen):
    for line in go_annot:
        info = line.strip().split("\t")
        if len(info) >= 2:
            gene = info[1] # gene ID
            pathway = info[0] # GO term
            pathway = clear_space(pathway)
            #if gene in expre_gen:
            if gene not in genler_list:
                genler_list.append(gene)
            #for GO in pathway:
            if gene in expre_gen:
                if pathway in dict:
                    if gene not in dict[pathway]:
                        dict[pathway].append(gene)
                else:
                    dict[pathway] = [gene]
            else:
                pass
dict = {} #dictionary should be GOterm:genes                        
add_go_to_dict(go_annot, dict, expre_gen)
#print (dict)
print ("number of path genes", len(dict.keys()))
print ("number of cluster genes", len(expre_gen))
## make table for enrichment comparing clusters and GO terms, how many clusters represent 'x' GO term?
output_table = open('tableforEnrichment_%s' % cluster_result, 'w') # output is GOterm_cluster#, inclust-inGO, inclust-notGO, notclust-inGO, notclust-notGO
genenum= len(expre_gen) #to compare just genes in your genelist (not all genes), use this genenumber
for item in dict:
    #item:GO-ID
    gene_list_for_go = dict[item]
    #print gene_list_for_go
    for i in dict_cluster.keys():
        cluster_list = dict_cluster[i]
        
        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0
        for j in cluster_list:
            if j in gene_list_for_go:
                count1 = count1 + 1
            else:
                count2 = count2 + 1
        count3 = len(gene_list_for_go) - count1
        count4 = genenum - (count1 + count2 + count3) #number is based on the # of genes from cluster file- in this case 20998
        output_table.write('%s|%s\t%i\t%i\t%i\t%i\n' % (item, i, count1, count2, count3, count4))
output_table.close()
#print gene_list_for_go