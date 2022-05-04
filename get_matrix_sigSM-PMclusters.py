#get matrix for sig and non sig clusters with SM or PM genes

import sys, os

fish_file = open(sys.argv[1], 'r')
clustgene_file = open(sys.argv[2], 'r')

SMsig=[]
SMnotsig=[]
PMsig=[]
PMnotsig=[]
def get_sig_clust(inp, SMsig, PMsig, SMnotsig, PMnotsig):
    
    for line in inp:
        L = line.strip().split('\t')
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
                pass
                
        
    return SMsig, PMsig, SMnotsig, PMnotsig
        
SMsig, PMsig, SMnotsig, PMnotsig = get_sig_clust(fish_file, SMsig, PMsig, SMnotsig, PMnotsig)
print (SMsig, PMsig, SMnotsig, PMnotsig)
fish_file.close()
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
            
get_gene_clust(clustgene_file, D)
print (D)
gene_dict1= {}
gene_dict2= {}
for cluster in D:
    genes = D[cluster]
    if cluster in SMsig:
        for gene in genes:
            gene_dict1[gene]= ['1', '1']
            #gene_dict2[gene]= 1
    elif cluster in PMsig:
        for gene in genes:
            gene_dict1[gene]= ['2', '2']
            #gene_dict2[gene]= 2
    elif cluster in SMnotsig:
        for gene in genes:
            gene_dict1[gene]= ['0', '1']
            #gene_dict2[gene]= 1
    elif cluster in PMnotsig:
        for gene in genes:
            gene_dict1[gene]= ['0', '2']
            #gene_dict2[gene]= 2
    else:
        for gene in genes:
            gene_dict1[gene]= ['0', '0']
            #gene_dict2[gene]= 0
        
print(gene_dict1, gene_dict2)

output= open(sys.argv[2]+'.sig.clust.matrix', 'w')
output.write('gene\tsig_cluster\tnonsig_cluster\n')
for gene in gene_dict1:
    datalist= gene_dict1[gene]
    datastr= '\t'.join(datalist)
    output.write('%s\t%s\n' % (gene, datastr))
clustgene_file.close()
output.close()
