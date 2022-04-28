# parse phytozome annotation so that formate is gene: all data for that gene
# python parse_phytozome_ann.py <phytozome annotation file> <pfam description file> 
#	<GO description file> <integer for pfam index> <integer for go index> <string to split pfam/GO - default is space>

import sys, os
import pandas as pd

# INPUTS
#DEFAULT
split_by=' '
#REQUIRED
for i in range (1,len(sys.argv),2):
	if sys.argv[i] == '-ann_file': 
		ann_file_name= sys.argv[i+1]
		ann_file= open(ann_file_name,'r')
	if sys.argv[i] == '-pfam_file':
		pfam_file=open(sys.argv[i+1],'r')
	if sys.argv[i] == '-go_file':
		go_file= open(sys.argv[i+1],'r')
	if sys.argv[i] == '-pfam_ind':
		pfam_ind= int(sys.argv[i+1])
	if sys.argv[i] == '-go_ind':
		go_ind= int(sys.argv[i+1])
#OPTIONAL
	if sys.argv[i] == '-split_by':
		split_by= str(sys.argv[i+1])

def clear_quotes(string): #returns string without quotes
	string = string.strip()
	while '"' in string:
		string = string.replace('"',"")
	return string
	
def get_ann(inp, D):
	header= inp.readline().strip().split("\t")
	for line in inp:
		L= line.strip().split("\t")
		data2=[]
		gene= L[0]
		data= L[1:]
		
		if gene not in D.keys():
			for i in data:
				i= clear_quotes(i)
				data2.append([i])
			D[gene]=data2
			#print(data2)
		else:
			for j in data:
				ind= data.index(j)
				j= clear_quotes(j)
				if j in D[gene][ind]:
					pass
				else:
					D[gene][ind].append(j)
# 						try:
# 							x.append(j)
# 						except(IndexError):
# 							D[gene].insert(ind, j)
	return D, header

D={}
ann_D, header= get_ann(ann_file, D)

print (ann_D, header)

#get pfam dictionary
def get_pfam(inp2, D2):
	header= inp2.readline().strip().split("\t")
	for line in inp2:
		L= line.strip().split("\t")
		pfam=L[0]
		pfamdat=L[1:]
		D2[pfam]=pfamdat
	return(D2)
	
D2={}
pfam_D= get_pfam(pfam_file, D2)
print(pfam_D)

# pfam description
for gene in ann_D:
	datal= ann_D[gene]
	datal_len= len(datal)
	new_dat=[]
	for y in datal[pfam_ind]:
			yl= y.split(split_by)
			print(yl)
			for z in yl:
				if z not in new_dat:
					new_dat.append(z)
				else:
					pass
				if z in pfam_D.keys():
					pfam_des=pfam_D[z]
					pfamstr= ";".join(pfam_des)
				else:
					pfamstr="NA"
				if len(datal)==datal_len:
					datal.append([pfamstr])
				else:
					print(datal[datal_len])
					if pfamstr not in datal[datal_len]:
						datal[datal_len].append(pfamstr)
					else:
						pass
					
	datal[pfam_ind]=new_dat
						#plistind=data1.index(pfamstr)
						#datal[plistind].append(pfamstr)

print (ann_D)

#get GO dictionary
def get_go(inp3, D3):
	header= inp3.readline().strip().split("\t")
	for line in inp3:
		L= line.strip().split("\t")
		goID=L[0]
		go=L[1]
		D3[goID]=go
	return(D3)

D3={}	
GO_D= get_go(go_file, D3)
print(GO_D)

#GO description
for gene in ann_D:
	datal= ann_D[gene]
	datal_len= len(datal)
	new_dat=[]
	for y in datal[go_ind]:
			yl= y.split(split_by)
			print(yl)
			for z in yl:
				if z not in new_dat:
					new_dat.append(z)
				else:
					pass
				if z in GO_D.keys():
					go_des=GO_D[z]
				else:
					go_des="NA"
				if len(datal)==datal_len:
					datal.append([go_des])
				else:
					print(datal[datal_len])
					if go_des not in datal[datal_len]:
						datal[datal_len].append(go_des)
					else:
						pass
	datal[go_ind]=new_dat
print (ann_D)
# write out

out= open(str(ann_file_name)+"_parsed.txt","w")

headstr= "\t".join(header[1:])
out.write("gene\t"+headstr+"\tpfam_descr\tgo_descr"+"\n")
for gene in ann_D:
	out.write(gene+"\t")
	datafin= ann_D[gene]
	for d in datafin:
		if len(d)> 1:
			dstr= ",".join(d)
		else:
			dstr= d[0]
		out.write(dstr+"\t")
	out.write("\n")
	
ann_file.close()
out.close()
	