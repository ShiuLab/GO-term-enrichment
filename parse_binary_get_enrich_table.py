import sys, os

matrix_file = open(sys.argv[1], 'r') # binary matrix file with all features and genetype comparisons: binary_matrix-domain_matrix.txt_comparisons.txt
output = open(sys.argv[1] + '_enrichment_table.txt', 'w')
#gene_type = str(sys.argv[2]) #pos class

genetype_dict ={}
genecond_dict ={}
feature_list = []
line = matrix_file.readline()
x = line.strip().split('\t')
feature_list = x[2:]
    
print("getting genes")
def get_genes(inp, D, D2, feature_list):
    header= inp.readline()
    for line in inp:
            L2 = line.strip().split('\t')
            gene = L2[0]
            gen_type = L2[1]
            cond = L2[2:]
            if gen_type not in genetype_dict:
                genetype_dict[gen_type] = [gene]
            else:
                genetype_dict[gen_type].append(gene)
            if gene not in genecond_dict:
                genecond_dict[gene] = cond
            else:
                pass
       
get_genes(matrix_file, genetype_dict, genecond_dict, feature_list)
gene_num = len(genecond_dict.keys()) 
#281print (gene_num)
#print genetype_dict
#print genecond_dict
#print feature_list  

feature_dict_pos= {}
feature_dict_neg= {}
n = len(feature_list)
print("getting pos and neg features")
for i in range(0,n-1):
    name = str(feature_list[i])
    #neg_name = str(feature_list[i]) + '_neg'
    #print pos_name
    for gene in genecond_dict:
        #print gene
        feature_cond = genecond_dict[gene]
        try:
            feature_cond2 = feature_cond[i]
            #print feature_cond2
            if feature_cond2 == '1':
                #print feature_cond2
                if name not in feature_dict_pos:
                    feature_dict_pos[name] = [gene]
                else:
                    feature_dict_pos[name].append(gene)
            elif feature_cond2 == '0':
                if name not in feature_dict_neg:
                    feature_dict_neg[name] = [gene]
                else:
                    feature_dict_neg[name].append(gene)
            else:
                pass
        except IndexError:
            pass
        
#print (feature_dict_neg)
#print (feature_dict_pos)

## make table for enrichment
print ("getting enrichment and writing")
for feature in feature_dict_pos:
    gene_list_pos = feature_dict_pos[feature]
    if feature in feature_dict_neg:
        gene_list_neg = feature_dict_neg[feature]
    else:
        gene_list_neg= []
    ##print (len(gene_list_pos))
    #gene_num = len(gene_list_pos)+len(gene_list_neg)
    gene_list_pos_len = len(gene_list_pos)
    #print gene_list_for_go
    for genetype in genetype_dict:
        gene_list2nd = genetype_dict[genetype]
        # if genetype == gene_type:
        #     gene_list2nd = genetype_dict[genetype]
        # else:
        #     gene_listother = genetype_dict[genetype]
        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0
        for gene in gene_list_pos:
            if gene in gene_list2nd: 
                count1 = count1 + 1 #SM/pos gene type that is pos
            else:
                count2 = count2 + 1 #other genetype that is pos
    #print (count1)
        neg_list=[]
        for gene in gene_list_neg:
            if gene in gene_list2nd:
                neg_list.append(gene)
        #print (len(neg_list))
        #count3 = len(gene_list2nd) - count1 #SM/pos genetype- pos = SM not in feature
        count3= len(neg_list)
    #print (count3)
        #print (gene_num)
        count4 = gene_num - (count1 + count2 + count3) #number is based on the # of genes from cluster file- in this case 20998

        output.write('%s_%s\t%i\t%i\t%i\t%i\n' % (feature, genetype, count1, count2, count3, count4))

output.close()
matrix_file.close()            
