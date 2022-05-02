import sys, os, math

go_function_file = open(sys.argv[1], 'r') #file with Go and function: GO_BPtermlistfromEBI
pathway_file = open(sys.argv[2], 'r') # file with gene and pathway #SMvsOther_classes_file.txt_SM_pathways_names2.txt.parsed.txt_genefile.txt
gene_gos_file = open(sys.argv[3], 'r') #Metabolism_Go-terms_genes2.txt
gofun_list =[]
output = open(str(sys.argv[3])+'.function.txt', 'w')
#function_list = []
dict_gofun = {} #Go term dictionary with function
line1 = go_function_file.readline()
while line1:
    d = line1.strip().replace(" ","\t").split("\t")
    p = d[0] #to make sure that all spaces are removed
    gofun_list.append(p) 
    for i in d[1:]:
        function_str = "_".join(d)
    dict_gofun[p] = function_str
    line1 = go_function_file.readline()
 
#print (dict_gofun)
dict_gene={}   
for line in gene_gos_file:
    if line.startswith("AT"):
        L = line.strip().split('\t')
        gene = L[0]
        type1 = L[1]
        go = L[2:]
        if gene not in dict_gene:
            dict_gene[gene]=[type1,go]
        
#print (dict_gene)

path_dict= {}
def get_pathway(inp, D):
    for line in inp:
        if line.startswith('AT'):
            L= line.strip().split('\t')
            gene = L[0]
            if len(L) >= 3:
                path = L[2:]
            if gene not in D:
                D[gene]= path

get_pathway(pathway_file, path_dict)
print (path_dict)            

output.write('gene\ttype\tGOterm\n')
for gene in dict_gene:
    data = dict_gene[gene]
    new_list = []
    type1 = data[0]
    gos = data[1]
    #print (gene, type1)
    output.write('%s\t%s\t' %(gene, type1))
    if gene in path_dict.keys():
        paths = path_dict[gene]
        path_str = ', '.join(paths)
        output.write('%s\t' %(path_str))
    else:
        output.write('NA\t')
    if type1 == 'other':
        output.write('NA\n')
    else:
        for go in gos:
            if go in dict_gofun.keys():
                function = dict_gofun[go]
                #new_list = []
                #new_list.append(go)
                new_list.append(function)
                #go_str = '_'.join(new_list)
                #go_list.append(go_str)
            else:
                new_list.append(go)
    print (new_list)
    go_str2 = ', '.join(new_list)
    print (go_str2)
    output.write(go_str2+'\n')
    
        