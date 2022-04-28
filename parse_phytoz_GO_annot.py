import sys, os

phyt_file= open(sys.argv[1], 'r')

gene_dict={}

def Union(lst1, lst2): 
    final_list = list(set(lst1) | set(lst2)) 
    return final_list 

header=phyt_file.readline()
for line in phyt_file:
	Golist=[]
	L= line.strip().split('\t')
	locus= L[1]
	for i in L:
		if i.startswith("GO:"):
			if i not in Golist:
				Golist.append(i)
			else:
				pass
	if locus not in gene_dict:
		gene_dict[locus]=Golist
	else:
		firstlst= gene_dict[locus]
		fin_list= Union(firstlst, Golist)
		gene_dict[locus]=fin_list
		
print(gene_dict)

output= open(str(sys.argv[1])+'_parsed.txt','w')

for key in gene_dict:
	data= gene_dict[key]
	for d in data:
		output.write('%s\t%s\n' % (d, key))
	
output.close()
phyt_file.close()