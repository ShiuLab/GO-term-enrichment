#this script gets an enrichment table for each cluster file
import os, sys

start_dir = sys.argv[1]
classes_file = open(sys.argv[2], "r")

genetype_dict={}
def get_genetype(inp, D):
    for line in inp:
        if line.startswith('locus'):
            pass
        if line.startswith('gene'):
            pass
        else:
            L2 = line.strip().split('\t')
            gene = L2[0]
            gen_type = L2[1]
            if gen_type not in genetype_dict:
                genetype_dict[gen_type] = [gene]
            else:
                genetype_dict[gen_type].append(gene)
                
get_genetype(classes_file, genetype_dict)
print (genetype_dict)
for genetype in genetype_dict:
    if genetype == "SM":
        gene_list2nd = genetype_dict[genetype]
    else:
        gene_listother = genetype_dict[genetype]
gene_num= len(gene_list2nd)+len(gene_listother)
print(gene_num)

def add_data_to_dict(inp,D):
    for line in inp:
        line.strip().replace('"','')
        if line.startswith("AT"):
            L = line.strip().split("\t")
            gene = L[0]
            clust = L[1]
            if clust not in D:
                D[clust] = [gene]
            else:
                D[clust].append(gene)


#loop through directory to add each filename
title_list = []
for dir in os.listdir(start_dir):
        if dir.startswith('._'):
            pass
        elif dir.startswith('get'):
            pass
        else:
            dir2 = start_dir + "/" + dir
            for file in os.listdir(dir2): 
                #print(file)
                if file.startswith("genelist"):
                        name_list = file.strip().split("_")
                        name= ".".join(name_list[1:4])
                        title_list.append(name)
title_list.sort()
title_str = "\t".join(title_list)
print (title_list)

#loop through directory for each file to add input
D2= {}
for x in title_list:
    for dir in os.listdir(start_dir):
        if dir.startswith('._'):
            pass
        elif dir.startswith('get'):
            pass
        else:
            dir2 = start_dir + "/" + dir
            for file in os.listdir(dir2): 
                if file.startswith("genelist"):
                        name_list = file.strip().split("_")
                        name= ".".join(name_list[1:4])
                        D={}
                        if x == name:
                            print (x)
                            inp = open(dir2 + "/" + file)
                            add_data_to_dict(inp,D)
                            inp.close()
                            #print (D)
                            output = open(dir2 + "/" + str(name)+".enrichment_table.txt","w")
                            #print (output)
                            #output.write("gene\tcluster\tgene_number\n")
                            for clust in D:
                                gene_list_pos = D[clust]
                                gene_list_pos_len = len(gene_list_pos)
                                count1 = 0
                                count2 = 0
                                count3 = 0
                                count4 = 0
                                for gene in gene_list_pos:
                                    if gene in gene_list2nd: 
                                        count1 = count1 + 1 #gene is in cluster, and is SM gene
                                    else:
                                        count2 = count2 + 1 #gene is in cluster, not an SM gene
                                count3 = len(gene_list2nd) - count1 #gene is an SM gene, not in cluster
                                count4 = gene_num - (count1 + count2 + count3) #gene is not Sm gene and not in cluster: gene num is based on the # of genes from classes file
                                final_name = str(name)+"_"+str(clust)
                                output.write('%s\t%i\t%i\t%i\t%i\n' % (final_name, count1, count2, count3, count4))
                            output.close()
