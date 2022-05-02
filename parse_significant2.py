import sys, math

##
# This function should parse out features that are significant. It requires a
# table with features and associated p-values. The user specifies an alpha,
# and the script gives an output of the significant features.
##

print '''
-in      := input file
-a       := alpha level
-index   := The location of the adjusted p-vaqlue or q-value
-output  := The name of the output file
-GOfile  := List of Go terms and their function

'''
for i in range(0, len(sys.argv)):
    if sys.argv[i] == '-in':
        file1      = sys.argv[i+1]
    if sys.argv[i] == '-a':
        alpha      = float(sys.argv[i+1])
    if sys.argv[i] == '-index':
        index      = int(sys.argv[i+1])
    if sys.argv[i] == '-output':
        output     = sys.argv[i+1]
    if sys.argv[i] == '-GOfile':
        EC_list = sys.argv[i+1] #list of GOterms- goterm: name of function
table = open(file1, 'r')
out1 = open(output, 'w') # output file

#ara = open(EC_list, 'r')
#ec_list =[]
##function_list = []
#dict_ec = {} #Go term dictionary with function
#line1 = ara.readline()
#while line1:
#    d = line1.strip().split("\t")
#    p = d[0].strip() #to make sure that all spaces are removed
#    ec_list.append(p) 
#    for i in d[1:]:
#        function_str = "_".join(d)
#    dict_ec[p] = function_str
#    line1 = ara.readline()

# Skip the header to the output
next(table)

for line in table:
    tab1 = line.strip().replace("'", "").split('\t')
    enrich = str(tab1[5])
    pvalue = float(tab1[index]) # the adjusted p value or q value for the feature
    if pvalue == float(0):
        print (pvalue)
        pvalue == float(1e-100)
        if pvalue <= alpha:
            if enrich == "+":
                score = - (math.log10(pvalue))
                out1.write('%s\t%s\t%s\t%s\n' %(tab1[0], enrich, pvalue, score)) # Writes the name of the feature to the table file
            elif enrich == "-":
                score = math.log10(pvalue)
                out1.write('%s\t%s\t%s\t%s\n' %(tab1[0], enrich, pvalue, score))
    else:
        pvalue == pvalue
        if pvalue <= alpha:
            if enrich == "+":
                score = - (math.log10(pvalue))
                out1.write('%s\t%s\t%s\t%s\n' %(tab1[0], enrich, pvalue, score)) # Writes the name of the feature to the table file
            elif enrich == "-":
                score = math.log10(pvalue)
                out1.write('%s\t%s\t%s\t%s\n' %(tab1[0], enrich, pvalue, score))