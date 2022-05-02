import sys, os

obo = open(sys.argv[1], 'r') #gene_ont_obo
assoc = open(sys.argv[2], 'r') #gene_association.tair 

output = open("Metabolism_Go-terms_genes2.txt", 'w')

go_dict = {}
def get_GO (inp, go_dict):
    for line in inp:
        if line.startswith('id:'):
            L = line.strip().split(' ')
            go = L[1]
            
        if line.startswith('is_a:'):
            L2 = line.strip().split(' ')
            parent = str(L2[1])
            
            if go not in go_dict:
                go_dict[go] = [parent]
            else:
                go_dict[go].append(parent)
            #print go_dict 
        else:
            pass   
        
get_GO(obo, go_dict)           

assoc_dict = {}
def get_assoc (inp, assoc_dict):
    for line in inp:
        if line.startswith('TAIR'):
            L3 = line.strip().split('\t')
            if L3[4].startswith('GO'):
                go = L3[4]
                if L3[9].startswith('AT'):
                    gene = L3[9]
            
                    if gene not in assoc_dict:
                        assoc_dict[gene] = [go]
                    else:
                        assoc_dict[gene].append(go)

get_assoc(assoc, assoc_dict)

print assoc_dict

primary_list= []
secondary_list= []           
                                    
for go in go_dict:
    go_list = go_dict[go]
    for parent in go_list:
        if parent == 'GO:0019748':
            secondary_list.append(go)
        if parent == 'GO:0044238':
            primary_list.append(go)
            
print secondary_list
print primary_list            

for term in secondary_list:
    for go in go_dict:
        go_list = go_dict[go]
        for parent in go_list:
            if parent == term:
                secondary_list.append(go)   
                
for term in primary_list:
    for go in go_dict:
        go_list = go_dict[go]
        for parent in go_list:
            if parent == term:
                primary_list.append(go)  
                


prim = '\t'.join(str(i) for i in primary_list)
prim_len = len(primary_list)
sec = '\t'.join(str(i) for i in secondary_list)
sec_len = len(secondary_list)

print (primary_list, prim_len)
print (secondary_list, sec_len)

#output.write("primary metabolism GO\t%s\t%s\n" % (prim_len, prim))
#output.write("seconday metabolism GO\t%s\t%s\n" % (sec_len, sec))

gene_primary = []
gene_secondary = []
primary_dict = {}
secondary_dict = {}

for gene in assoc_dict:
    go_list = assoc_dict[gene]
    for go in go_list:
        if go in primary_list:
            gene_primary.append(gene)
            if gene not in primary_dict:
                primary_dict[gene] = [go]
            else:
                primary_dict[gene].append(go)
        if go in secondary_list:
            gene_secondary.append(gene)
            if gene not in secondary_dict:
                secondary_dict[gene] = [go]
            else:
                secondary_dict[gene].append(go)
        else:
            pass

gene_primary2 = []
gene_secondary2 = []
for gene in gene_primary:
    if gene in gene_secondary:
        pass
    else:
        if gene not in gene_primary2:
            gene_primary2.append(gene)
        
for gene in gene_secondary:
    if gene in gene_primary:
        pass
    else:
        if gene not in gene_secondary2:
            gene_secondary2.append(gene)
output.write("gene\ttype\tGOterm\n")

for gene in gene_primary2:
    if gene in primary_dict.keys():
        go_data = primary_dict[gene]
        go_data_str = '\t'.join(go_data)
        output.write('%s\tprimary\t%s\n' % (gene, go_data_str))

for gene in gene_secondary:
    if gene in secondary_dict.keys():
        go_data2 = secondary_dict[gene]
        go_data_str2 = '\t'.join(go_data2)
        output.write('%s\tsecondary\t%s\n' % (gene, go_data_str2)) 

prim_gene = '\t'.join(str(i) for i in gene_primary2)
prim_gene_len = len(gene_primary)
prim_gene_len2 = len(gene_primary2)
sec_gene = '\t'.join(str(i) for i in gene_secondary2)
sec_gene_len = len(gene_secondary)
sec_gene_len2 = len(gene_secondary2)

output.write("primary metabolism genes\t%s\t%s\t%s\n" % (prim_gene_len, prim_gene_len2, prim_gene))
output.write("seconday metabolism genes\t%s\t%s\t%s\n" % (sec_gene_len, sec_gene_len2, sec_gene))       