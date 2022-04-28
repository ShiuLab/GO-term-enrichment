import sys, os

obo = open(sys.argv[1], 'r') #gene_ont_obo

output = open("go.obo.v1.2_parsed.txt", 'w')

def clear_space(string): #returns _ connected
	while "  " in string:
		string = string.replace("  "," ")
	string = string.replace(" ","_")
	return string

go_dict = {}
def get_GO (inp, go_dict):
    for line in inp:
        #count=0
        if line.startswith('id:'):
            L = line.strip().split(' ')
            go = str(L[1])
            if go not in go_dict:
            	go_dict[go]=[]
            
        if line.startswith('name:'):
            L2 = line.strip().split(': ')
            func = str(L2[1])
            func=clear_space(func)
            go_dict[go].append(func)
            
        if line.startswith('namespace:'):
            L3 = line.strip().split(': ')
            #print(L3)
            cat = str(L3[1])
            cat=clear_space(cat)
            go_dict[go].append(cat)

        
get_GO(obo, go_dict)  

print(go_dict)

output.write("GOID\tGO function\tGO category\n")
for go in go_dict:
	if go.startswith("GO"):
		data= go_dict[go]
		datastr= "\t".join(data)
		output.write('%s\t%s\n' % (go,datastr))
	else:
		pass
	
output.close()
obo.close()