'''makes the following enrichment table for each pair of classes:
                           |  having a given property    |  not having a given property
---------------------------------------------------------------------------------------
subset of  population      |           t1                |              t2
the rest of  population    |           t3                |              t4
'''
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
print(feature_list)   
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
#print (genetype_dict)
#print (genecond_dict)
#print feature_list  

feature_dict_pos= {}
feature_dict_neg= {}
n = len(feature_list)
print("getting pos and neg features")
for i in range(0,n):
    name = str(feature_list[i])
    #neg_name = str(feature_list[i]) + '_neg'
    #print pos_name
    for gene in genecond_dict:
        #print gene
        feature_cond = genecond_dict[gene]
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
        genetype1= genetype.split("_")[2]
        if genetype1 == "within":
            gene_list1 = genetype_dict[genetype]
            genetype2= genetype.split("_")[0] + "_" + genetype.split("_")[1] + "_between"
            try:
                gene_list2 = genetype_dict[genetype2]
                
            except(KeyError):
                print(genetype, " has no pair")
                gene_list2= []
                
            count1 = 0
            count2 = 0
            count3 = 0
            count4 = 0
            for gene in gene_list_pos:
                if gene in gene_list1: 
                    count1 = count1 + 1 #SM/pos gene type that is pos
                elif gene in gene_list2:
                    count3 = count3 + 1 #other genetype that is pos
    #print (count1)
            neg_list=[]
            for gene in gene_list_neg:
                if gene in gene_list1:
                    count2= count2+1 #SM/pos genetype is negative
                elif gene in gene_list2:
                    count4= count4+1 #other genetype is negative
    
            output.write('%s|%s\t%i\t%i\t%i\t%i\n' % (feature, genetype, count1, count2, count3, count4))
        else:
            pass

print('done!')
output.close()
matrix_file.close()            
