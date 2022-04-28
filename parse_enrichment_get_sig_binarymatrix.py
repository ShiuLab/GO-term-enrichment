#script gets binary matrix with significant path clusters at p<0.05. for q value change q = float(x[6]) to q = float(x[7])
import sys, os, math, operator

start_dir= sys.argv[1] #directory with .fisher.pqvalue files
oup = open(start_dir + "/sig_path_enriched_clusters_binarymatrix.txt", "w")
enrich = sys.argv[2] # 1 for pos (+) enrich only, 2 for both + and -
sec_dir= sys.argv[3] #directory with original cluster files
all_genes = open(sys.argv[4], 'r') # file with all genes, ie. Sl.allgenes.v2.5.txt

all_gene_list= []
for line in all_genes: #get all genes
    if line.startswith("gene"):
        pass
    else:
        L = line.strip().split('\t')
        gene = L[0]
        if gene not in all_gene_list:
            all_gene_list.append(gene)
        else:
            pass

feature_list=[]
def get_sigs(fisherfile, dict_pos, dict_neg):
    for line in fisherfile:
        x = line.strip().split('\t')
        a = x[5]
        q = float(x[7])
        feature = str(x[0])
        if feature not in feature_list:
            feature_list.append(feature)
        if a == '+' and q < 0.05:
            try:
                score = float(-(math.log10(q)))
            except:
                ValueError
                score = float(-(math.log10(1e-300)))
            if feature not in dict_pos:
                dict_pos[feature] = score
            else:
                print (feature, "already in pos dict")

        elif a == '-' and q < 0.05:
            try:
                score = float(math.log10(q))
            except:
                ValueError
                score = float(math.log10(1e-300))
            if feature not in dict_neg:
                dict_neg[feature] = score
            else:
                print (feature, "already in neg dict")
    
        else:
            pass
    
    return (dict_pos, dict_neg)
          
#loop through and get significant dictionarys
gene_D = {}
title_list= []
for file in os.listdir(start_dir):
    if file.endswith(".fisher.pqvalue"):
        name1= file.strip().split("Enrichment_")[1]
        name= name1.strip().split(".fisher")[0]
        fisherfile = open(start_dir + "/" + file, 'r') # pqvalue file (output of fishers- .pqvalue)
        dict_pos={}
        dict_neg={}
        new_pos, new_neg = get_sigs(fisherfile, dict_pos, dict_neg)
        #print (new_pos, new_neg)
        path_list= []
        clust_list = []
        for i in new_pos.keys():
            path= i.split("_")[0]
            cluster= i.split("_")[1]
            path_list.append(path)
            clust_list.append(cluster)
            string= "%s_%s-%s" % (name, path, cluster)
            title_list.append(string)
        
        for file2 in os.listdir(sec_dir):
            if file2 == name:
                print (file2)
                inp_file= open(sec_dir + "/" + file2, 'r')
                clust_gene_list=[]
                fileclust_list=[]
                for line in inp_file:
                    L= line.strip().split('\t')
                    gene = L[0]
                    clust_gene_list.append(gene)
                    if gene not in all_gene_list:
                        all_gene_list.append(gene)
                    clust = L[1]
                    fileclust_list.append(clust)
                    
                    for x in clust_list:
                        if clust == x:
                            result= 1
                        else:
                            result= 0
                        if gene not in gene_D:
                            gene_D[gene]= [result]
                        else:
                            gene_D[gene].append(result)
                
                clustlength= len(clust_list)
                for gene in all_gene_list:
                    if gene in clust_gene_list:
                        pass
                    else:
                        result_list= []
                        for i in range(clustlength):
                            result_list.append('NA')
                        print ("result_list", len(result_list), "cluster_list", clustlength)
                        if gene not in gene_D:
                            gene_D[gene]= result_list
                        else:
                            for result in result_list:
                                gene_D[gene].append(result)
                        
        # if enrich == 1:
        #     print ("positive enrichment only")
        # else:
        #     print ("doing negative enrichment")
        #     for i in new_neg.keys():
        #         path= i.split("_")[0]
        #         cluster= i.split("_")[1]
        #         path_list.append(path)
        #         clust_list.append(cluster)
        #         string= "%s_%s-%s-neg" % (name, path, cluster)
        #         title_list.append(string)
        #     for file2 in os.listdir(sec_dir):
        #         if file2 == name:
        #             inp_file= open(sec_dir + "/" + file2, 'r')
        #             for line in inp_file:
        #                 L= line.strip().split('\t')
        #                 gene = L[0]
        #                 clust = L[1]
        #                 for x in clust_list:
        #                     if clust == x:
        #                         result= 1
        #                     else:
        #                         result= 0
        #                     if gene not in gene_D:
        #                         gene_D[gene]= [result]
        #                     else:
        #                         gene_D[gene].append(result)


print (gene_D)
print (title_list)
#write output

title_str= "\t".join(title_list)
oup.write("gene\t%s\n" % (title_str))
title_len= len(title_list)
print (title_len, "Number of enriched clusters in pathways")
for gene in gene_D.keys():
    data = gene_D[gene]
    datastr= '\t'.join(str(x) for x in data)
    oup.write("%s\t%s\n" % (gene, datastr))
    