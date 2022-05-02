#get matrix for sig and non sig clusters with SM or PM genes

import sys, os

start_dir = sys.argv[1]
all_genes_file = open(sys.argv[2], 'r')

#get all genes!
all_genes_list= []
header = all_genes_file.readline()
for line in all_genes_file:
    L= line.strip().split('\t')
    gene= L[0]
    all_genes_list.append(gene)
    
SMsig=[]
SMnotsig=[]
PMsig=[]
PMnotsig=[]
unknown_list=[]
def get_sig_clust(inp, SMsig, PMsig, SMnotsig, PMnotsig, unkn):
    
    for line in inp:
        L = line.strip().split('\t')
        #print (L)
        clust = L[0]
        sign = L[5]
        q = float(L[7])
        clusttype= clust.split('_')[0]
        clust1= clust.split('_')[1]
        if sign == '+' and q < 0.05:
            if clusttype == 'SM':
                SMsig.append(clust1)
            elif clusttype == 'PM':
                PMsig.append(clust1)
            else:
                pass
        else:
            if clusttype == 'SM':
                SMnotsig.append(clust1)
            elif clusttype == 'PM':
                PMnotsig.append(clust1)
            else:
                unkn.append(clust)
                
        
    return SMsig, PMsig, SMnotsig, PMnotsig, unkn
        

D={}
def get_gene_clust(inp2, D):
    header = inp2.readline()
    
    for line in inp2:
        L2= line.strip().split('\t')
        gene=L2[0]
        clust=L2[1]
        if clust not in D:
            D[clust]= [gene]
        else:
            D[clust].append(gene)
        all_genes_list.append(gene)
    
    return D
            
gene_dict1= {}
name_list=[]
count = 1
for file in os.listdir(start_dir):
   if file.startswith("genelist_"):
       if file.endswith("-AT_all-genes.txt"):
            
            clustgene_file = open(file, 'r')
            #all_genes = get_gene_clust(clustgene_file, D)[0]
            D = get_gene_clust(clustgene_file, D)
            #print (all_genes)
            #print (len(all_genes))
            #print (D)
            name= file.strip().split('.header.txt')[0]
            print (name)
            name_list.append(name)
            clustgene_file.close()
            for file2 in os.listdir(start_dir):
               if file2.endswith('.fisher.pqvalue'):
                   file2a= file2.strip().split('.')[0]
                   filename= file2a.split('Enrichment_')[1]
                   #print (filename)
                   if filename == name:
                       fish_file =open(file2, 'r')
                       SMsig, PMsig, SMnotsig, PMnotsig, unknown_list = get_sig_clust(fish_file, SMsig, PMsig, SMnotsig, PMnotsig, unknown_list)
                       #print (SMsig, PMsig, SMnotsig, PMnotsig)
                       fish_file.close()
                       for cluster in D:
                            
                            genes = D[cluster]
                            if cluster in SMsig:
                                for gene in genes:
                                        if gene not in gene_dict1:
                                            gene_dict1[gene]= [('1', '1')]
                                        else:
                                            gene_dict1[gene].append(('1', '1'))
            #gene_dict2[gene]= 1
                            elif cluster in PMsig:
                                    for gene in genes:
                                        if gene not in gene_dict1:
                                            gene_dict1[gene]= [('2', '2')]
                                        else:
                                            gene_dict1[gene].append(('2', '2'))
            #gene_dict2[gene]= 2
                            elif cluster in SMnotsig:
                                for gene in genes:
                                    if gene not in gene_dict1:
                                        gene_dict1[gene]= [('0', '1')]
                                    else:
                                        gene_dict1[gene].append(('0', '1'))
                                    
            #gene_dict2[gene]= 1
                            elif cluster in PMnotsig:
                                for gene in genes:
                                    if gene not in gene_dict1:
                                        gene_dict1[gene]= [('0', '2')]
                                    else:
                                        gene_dict1[gene].append(('0', '2'))

            #gene_dict2[gene]= 2
                            
                            else:
                                for gene in genes:
                                    if gene not in gene_dict1:
                                        gene_dict1[gene]= [('0', '0')]
                                    else:
                                        gene_dict1[gene].append(('0', '0'))
                                
            if count <= 3:
                for gene in all_genes_list:
                    if gene not in gene_dict1:
                        gene_dict1[gene] = [('0', '0')]
                    elif len(gene_dict1[gene]) < count:
                        gene_dict1[gene].append(('0', '0'))
                    elif len(gene_dict1[gene]) == count:
                        pass
                    else:
                        print (gene, gene_dict1[gene])
            else:
                pass                            
            count = count +1
            print (count)
            #gene_dict2[gene]= 0
        
#print(gene_dict1)

output= open('categorical_sig.clust.matrix.txt', 'w')
output.write('gene\t')
for i in name_list:
    output.write('sig_cluster_%s\tnonsig_cluster_%s\t' % (i, i))
output.write('\n')

for gene in gene_dict1:
    datalist= gene_dict1[gene]
    new_list= []
    for data in datalist:
        string= data[0]
        string2= data[1]
        new_list.append(string)
        new_list.append(string2)
    
    datastr= '\t'.join(new_list)
    output.write('%s\t%s\n' % (gene, datastr))
clustgene_file.close()
output.close()
