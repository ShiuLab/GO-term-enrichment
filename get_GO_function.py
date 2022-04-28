#get Go term function for significant GO terms

import sys

sig_file = open(sys.argv[1], 'r') #significant file from fishers exact
go_func = open(sys.argv[2], 'r') #file with GO term and function
func = str(sys.argv[3]) # is your functions from biological process (BP) or Mol function (MF)
type1 = int(sys.argv[4]) # 1= this is the sig_file where GOnumber_SM, 2= just a go enrichment file, GO number without _SM
output = open(str(sys.argv[1])+".Goterm-"+func+".txt", "w")

dict_gofunc = {} #Go term dictionary with function
line1 = go_func.readline()
while line1:
    d = line1.strip().split("\t")
    p = d[0].strip() #to make sure that all spaces are removed 
    for i in d[1:21]:
        function_str = "_".join(d)
   
    dict_gofunc[p] = function_str
    line1 = go_func.readline()

print (dict_gofunc)
go_func.close()

# Skip the header to the output
next(sig_file)
# parse sig_file

if type1 == 1:
    for line in sig_file:
        info = line.strip().split("\t")
        path = info[0]
        data = info[1:]
        data_str= '\t'.join(data)
        pathway = path.split('_')[0]
        clust = path.split('_')[1]
        if pathway in dict_gofunc.keys():
            func_str = dict_gofunc[pathway]
            output.write('%s\t%s\t%s\t%s\n' % (pathway, func_str, clust, data_str)) 
elif type1 == 2:
    for line in sig_file:
        info = line.strip().split("\t")
        path = info[0]
        data = info[1:]
        data_str= '\t'.join(data)
        if path in dict_gofunc.keys():
            func_str = dict_gofunc[path]
            output.write('%s\t%s\t%s\n' % (path, func_str, data_str))
else:
    print("need type 1 or 2")
    sys.exit()
sig_file.close()
go_func.close()
output.close()