import sys, os, math, operator

fisherfile = open(sys.argv[1], 'r') # pqvalue file (output of fishers- .pqvalue)
out = str(sys.argv[1])
oup=open("%s.sig_score" % out ,"w" )

feature_list=[]
dict_pos={}
dict_neg={}
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
          
oup.write("feature\tenrichment\tlog.qval\n")

dict_pos_sorted = sorted(dict_pos.items(), key=operator.itemgetter(1), reverse=True) #sorts based on values
for key, val in dict_pos_sorted: 
    oup.write("%s\t+\t%.3f\n" % (key, val))

dict_neg_sorted = sorted(dict_neg.items(), key=operator.itemgetter(1), reverse=True) #sorts based on values
for key, val in dict_neg_sorted: 
    oup.write("%s\t-\t%.3f\n" % (key, val))
    