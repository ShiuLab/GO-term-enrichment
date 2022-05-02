import sys, os, math, collections

start_dir= sys.argv[1] #directory with .fisher.pqvalue files
oup = open(start_dir + "/sig_path_enriched_clusters_matrix.txt", "w")
GO_file = open(sys.argv[2], "r") #file with all features you want to use.. ie. all GO terms, or GO terms only in these clusters
neg_set = sys.argv[3] #ie. Chief_nonDEGs,Dick_nonDEGs,nonDEG_D-C,NON-DEG

if neg_set == "NA":
    pass
else:
    neg_set = neg_set.split(",")
    print (neg_set)

def clear_space(string): #returns tab-delimited
	string = string.strip()
	while "  " in string:
		string = string.replace("  "," ")
	string = string.replace(" ","_")
	return (string)

GO_list = []
for line in GO_file:
    GO= line.split("\t")[0]
    GO= clear_space(GO)
    if GO not in GO_list:
        GO_list.append(GO)
print (len(GO_list))

def get_sigs(fisherfile, dict_score, GO_list):
    feature_list=[]
    for line in fisherfile:
            x = line.strip().split('\t')
            a = x[5]
            q = float(x[6])
            feature = str(x[0].split('|')[0])
            cluster = str(x[0].split('|')[1])
            if feature not in feature_list:
                feature_list.append(feature)
            if neg_set == "NA":
                if a == '+':
                    try:
                        score = float(-(math.log10(q)))
                    except:
                        ValueError
                        score = float(-(math.log10(1e-300)))
                    if feature not in dict_score:
                        dict_score[feature] = [score]
                    else:
                        dict_score[feature].append(score)
                elif a == '-':
                    try:
                        score = float(math.log10(q))
                    except:
                        ValueError
                        score = float(math.log10(1e-300))
                    if feature not in dict_score:
                        dict_score[feature] = [score]
                    else:
                        dict_score[feature].append(score)
    
                else:
                    print (a)
            else:
                if cluster in neg_set:
                    pass
                        #print (cluster)
                else:
                    if a == '+':
                        try:
                            score = float(-(math.log10(q)))
                        except:
                            ValueError
                            score = float(-(math.log10(1e-300)))
                        if feature not in dict_score:
                            dict_score[feature] = [score]
                        else:
                            dict_score[feature].append(score)
    
                    elif a == '-':
                        try:
                            score = float(math.log10(q))
                        except:
                            ValueError
                            score = float(math.log10(1e-300))
                        if feature not in dict_score:
                            dict_score[feature] = [score]
                        else:
                            dict_score[feature].append(score)
                    else:
                        print (a)

    not_needed = []
    for feat in GO_list:
        if feat in feature_list:
            #print (feature)
            if feat not in not_needed:
                not_needed.append(feat)
        else:
            score = 0
            if feat not in dict_score:
                dict_score[feat] = [score]
            else:
                dict_score[feat].append(score)
                        
        
    print ("features in this file", len(feature_list), "all features", len(GO_list), "matching features", len(not_needed))
    print (len(dict_score.keys()))
    
            
    
    #return (dict_pos, dict_neg)

#loop through and get significant dictionarys
gene_D = {}
title_list= []
dict_score={}
#dict_neg={}
for file in os.listdir(start_dir):
    if file.endswith(".fisher.pqvalue"):
        name1= file.strip().split("Enrichment_")[1]
        name= name1.strip().split(".fisher")[0]
        fisherfile = open(start_dir + "/" + file, 'r') # pqvalue file (output of fishers- .pqvalue)
        print (name)
        get_sigs(fisherfile, dict_score, GO_list)
        title_list.append(name)

print (dict_score, "dict_score", len(dict_score.keys()))

title_str= "\t".join(title_list)    
oup.write("feature\t%s\n" % (title_str))

#dict_pos_sorted = collections.OrderedDict(sorted(dict_score.items(), reverse=True)) #sorts based on values
for key in dict_score:
    data = dict_score[key]
    print (len(data))
    if all(i < 1.3 and i > -1.3 for i in data) == True:
        pass
        print (key, "not significant in any cluster")
    else:
        oup.write("%s\t" % (key))
        for x in data:
            oup.write("%.3f\t" % (x))
        oup.write("\n")
        
oup.close()
GO_file.close()    