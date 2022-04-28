import sys, os, math, operator

#Default q
qval= 0.05
for i in range (1,len(sys.argv),2):
	if sys.argv[i] == '-in':
		fisherfile = sys.argv[i+1] # pqvalue file (output of fishers- .pqvalue)
	if sys.argv[i] == '-q':
		qval= float(sys.argv[i+1])

fisherfile1= open(fisherfile,'r')
out = str(fisherfile)
oup=open("%s.sig_%.2f" % (out,qval) ,"w" )
oup.write("file\tpathway\tcluster\tpos-pos\tpos-neg\tneg-pos\tneg-neg\tenrich\tpval\tqval\n")
feature_list=[]

#dict_neg={}
for line in fisherfile1:
    x = line.strip().split('\t')
    a = x[5]
    q = float(x[7])
    feature = str(x[0])
    if feature not in feature_list:
        feature_list.append(feature)
    if a == '+' and q <= qval:
        xstr= "\t".join(x)
        oup.write("%s\n" % (xstr))
    else:
        pass

# dict_pos_sorted = sorted(dict_pos.items(), key=operator.itemgetter(1), reverse=True) #sorts based on values
# for key in dict_pos_sorted:
#     data= dict_pos_sorted[key]
#     datastr= "\t".join(data)
#     oup.write("%s\t%s\n" % (key, datastr))

    