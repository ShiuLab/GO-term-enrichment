"example input: python parse_GO_obo-annot2.py go.obo gene_association.tair"
import sys, os

obo = open(sys.argv[1], 'r') #gene_ont_obo
assoc = open(sys.argv[2], 'r') #gene_association.tair 
go_input = open(sys.argv[3], 'r') #list of terms you want
output = open(str(sys.argv[3])+"_included_genes.txt", 'w')
output2 = open(str(sys.argv[3])+"_excluded_genes.txt", 'w')

go_lista=[]
def get_GO_input (inp, go_input_list):
    for line in inp:
        if line.startswith('GO:'):
            L1 = line.strip().split('\t')
            go = L1[0]
            go_input_list.append(go)
    return (go_input_list)

go_input_list= get_GO_input(go_input, go_lista)
print (go_input_list, len(go_input_list))
go_dict = {}
def get_GO (inp, go_dict):
    for line in inp:
        if line.startswith('id:'):
            L = line.strip().split(' ')
            go = L[1]
            
        if line.startswith('relationship:'):
            L2 = line.strip().split(' ')
            comment = str(L2[1])
            
            if comment == "has_part":
                child = str(L2[2])
                if go not in go_dict:
                    go_dict[go] = [child]
                else:
                    go_dict[go].append(child)
            elif comment == "part_of":
                child2 = str(L2[2])
                if go not in go_dict:
                    go_dict[go] = [child2]
                else:
                    go_dict[go].append(child2)
            else:
                pass
             
        else:
            pass   
        
get_GO(obo, go_dict)           
#print (go_dict)
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
                        assoc_dict[gene].append(go)

get_assoc(assoc, assoc_dict)

print (assoc_dict)

primary_list= []
secondary_list= []           
                                    

for go in go_dict:
    go_list = go_dict[go]
    if go in go_input_list:
        secondary_list.append(go)
        for child in go_list:
            secondary_list.append(child)
    else:
        for child2 in go_list:
            if child2 in go_input_list:
                secondary_list.append(child2) 
    
for go in go_input_list:
    if go not in secondary_list:
        secondary_list.append(go)        
            
print (len(secondary_list), secondary_list)

exclu_gene_list = []
inclu_gene_list = []    
for gene in assoc_dict:
    go_assoc_list = assoc_dict[gene]
    for go in go_assoc_list:
        if go in secondary_list:
            if gene not in exclu_gene_list:
                exclu_gene_list.append(gene)
        else:
            inclu_gene_list.append(gene)
            
final_list= []
for gene in inclu_gene_list:
    if gene in exclu_gene_list:
        pass
    else:
        if gene not in final_list:
            final_list.append(gene)

output.write("gene\tGOterms\n")
for gene in final_list:
    if gene in assoc_dict.keys():
        go_assoc_list2 = assoc_dict[gene]
        go_assoc_str= ' '.join(go_assoc_list2)
        output.write('%s\t%s\n' % (gene, go_assoc_str))
        
for gene in exclu_gene_list:
    if gene in assoc_dict.keys():
        go_assoc_list2 = assoc_dict[gene]
        go_assoc_str= ' '.join(go_assoc_list2)
        output2.write('%s\t%s\n' % (gene, go_assoc_str))    