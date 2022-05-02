import sys, os, math, operator

fisherfile = open(sys.argv[1], 'r') # pqvalue file (output of fishers- .pqvalue)
out = str(sys.argv[1])
filenum = int(sys.argv[2]) #number of pqvalue files that are concatenated together
oup=open("%s.sig_score" % out ,"w" )

feature_list=[]
list_len=filenum*7

header= fisherfile.readline()
oup.write("%s\n" % (header))
fisherfile.readline()

for line in fisherfile:
    L = line.strip().split('\t')
    enrich = L[5]
    q = L[7]
    feature = str(L[0])
    if q == 'NA':
        lista= [1,2,3,4,5,6,7]
        for i in range(filenum-1):
            new_list = [x+7 for x in lista]
            lista= new_list
            enrich = L[int(lista[4])]
            q = L[int(lista[6])]
            if q == 'NA':
                pass
            elif float(q) < 0.05:
                if feature not in feature_list:
                    feature_list.append(feature)
                    oup.write('%s\n' % (line))
                else:
                    pass
            else:
                pass
    elif float(q) < 0.05:
        if feature not in feature_list:
            feature_list.append(feature)
            oup.write('%s\n' % (line))
        else:
            pass
    else:
        lista= [1,2,3,4,5,6,7]
        for i in range(filenum-1):
            new_list = [x+7 for x in lista]
            lista= new_list
            enrich = L[int(lista[4])]
            q = L[int(lista[6])]
            if q == 'NA':
                pass
            elif float(q) < 0.05:
                if feature not in feature_list:
                    feature_list.append(feature)
                    oup.write('%s\n' % (line))
                else:
                    pass
            else:
                pass
    
fisherfile.close()
oup.close()    

    