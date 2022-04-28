#script to parse squash-cucmber best match to get clusters with negative class
import sys, os
neg_class = open(sys.argv[1], 'r') #.BLAST.parsed file with negative class
start_dir = sys.argv[2] #start directory with .BLAST.parsed files of positive classes
end = str(sys.argv[3]) #specifiy what the file with positive values ends with

#get negative class
empty_list=[]
def get_genes(inp, alist):
    header= inp.readline()
    for line in inp:
        L =line.strip().split('\t')
        if len(L) >= 2:
            cuke_gene = L[0]
            if cuke_gene not in alist:
                alist.append(cuke_gene)
            
    return(alist)
    
neg_list= get_genes(neg_class, empty_list)
print (len(neg_list), "number of negative genes")

#get positive classes
for file in os.listdir(start_dir):
    if file.endswith(end):
        name= file.strip().split(end)[0]
        print (name)
        empty_list2=[]
        inp1= open(str(start_dir)+'/'+ file, 'r')
        pos_list= get_genes(inp1, empty_list2)
        print (len(pos_list), "number of positive genes")
        output = open(str(name)+"_cluster.txt", 'w')
        output.write("gene\tcluster\n")
        for gene in pos_list:
            output.write('%s\t%s\n' % (gene, name))
        for gene in neg_list:
            output.write('%s\tNON-DEG\n' % (gene))
        output.close()
        
neg_class.close()
        
        
        