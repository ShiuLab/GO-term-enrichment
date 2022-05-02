import sys, os, math, collections, numpy

start_dir= sys.argv[1] #directory with .fisher.pqvalue files
oup = open("sig_path_enriched_clusters_matrix.txt", "w")
#GO_file = open(sys.argv[2], "r") #file with all features you want to use.. ie. all GO terms, or GO terms only in these clusters
splitby = sys.argv[2] #characheter to split between feature and cluster
neg_set = sys.argv[3] #ie. Chief_nonDEGs,Dick_nonDEGs,nonDEG_D-C,NON-DEG
neg_enrich =sys.argv[4] # do you want negatively enriched clusters (ie -)? if yes, then T. otherwise F

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
	

def get_sigs(fisherfile, dict_score, clust_D, name, feature_list):
	for line in fisherfile:
		x = line.strip().split('\t')
		num= float(x[4])
		a = x[5]
		q = float(x[6])
		feature = str(x[0].split(str(splitby))[0])
		cluster = str(name)+'_'+str(x[0].split(str(splitby))[1])
		if feature not in feature_list:
			feature_list.append(feature)
		if neg_set == "NA":
			if neg_enrich == "T":
				if a == '+' and num > 0:
					try:
						score = float(-(math.log10(q)))
					except:
						ValueError
						score = float(-(math.log10(1e-300)))
					if feature not in dict_score:
						dict_score[feature] = [(cluster,score)]
					else:
						dict_score[feature].append((cluster,score))
					if cluster not in clust_D:
						clust_D[cluster]=[score]
					else:
						clust_D[cluster].append(score)
				elif a == '-' and num > 0:
					try:
						score = float(math.log10(q))
					except:
						ValueError
						score = float(math.log10(1e-300))
					if feature not in dict_score:
						dict_score[feature] = [(cluster,score)]
					else:
						dict_score[feature].append((cluster,score))
					if cluster not in clust_D:
						clust_D[cluster]=[score]
					else:
						clust_D[cluster].append(score)
				else:
					score= float('nan')
					if feature not in dict_score:
						dict_score[feature] = [(cluster,score)]
					else:
						dict_score[feature].append((cluster,score))
					if cluster not in clust_D:
						clust_D[cluster]=[score]
					else:
						clust_D[cluster].append(score)
			else:
				if a == '+' and num > 0:
					try:
						score = float(-(math.log10(q)))
					except:
						ValueError
						score = float(-(math.log10(1e-300)))
					if feature not in dict_score:
						dict_score[feature] = [(cluster,score)]
					else:
						dict_score[feature].append((cluster,score))
					if cluster not in clust_D:
						clust_D[cluster]=[score]
					else:
						clust_D[cluster].append(score)
				else:
					score= float('nan')
					if feature not in dict_score:
						dict_score[feature] = [(cluster,score)]
					else:
						dict_score[feature].append((cluster,score))
					if cluster not in clust_D:
						clust_D[cluster]=[score]
					else:
						clust_D[cluster].append(score)
		else:
			if cluster in neg_set:
				pass
			else:
				if neg_enrich == "T":
					if a == '+'and num > 0:
						try:
							score = float(-(math.log10(q)))
						except:
							ValueError
							score = float(-(math.log10(1e-300)))
						if feature not in dict_score:
							dict_score[feature] = [(cluster,score)]
						else:
							dict_score[feature].append((cluster,score))
						if cluster not in clust_D:
							clust_D[cluster]=[score]
						else:
							clust_D[cluster].append(score)
					elif a == '-'and num > 0:
						try:
							score = float(math.log10(q))
						except:
							ValueError
							score = float(math.log10(1e-300))
						if feature not in dict_score:
							dict_score[feature] = [(cluster,score)]
						else:
							dict_score[feature].append((cluster,score))
						if cluster not in clust_D:
							clust_D[cluster]=[score]
						else:
							clust_D[cluster].append(score)
					else:
						score= float('nan')
						if feature not in dict_score:
							dict_score[feature] = [(cluster,score)]
						else:
							dict_score[feature].append((cluster,score))
						if cluster not in clust_D:
							clust_D[cluster]=[score]
						else:
							clust_D[cluster].append(score)
				else:
					if a == '+' and num > 0:
						try:
							score = float(-(math.log10(q)))
						except:
							ValueError
							score = float(-(math.log10(1e-300)))
						if feature not in dict_score:
							dict_score[feature] = [(cluster,score)]
						else:
							dict_score[feature].append((cluster,score))
						if cluster not in clust_D:
							clust_D[cluster]=[score]
						else:
							clust_D[cluster].append(score)
					else:
						score= float('nan')
						if feature not in dict_score:
							dict_score[feature] = [(cluster,score)]
						else:
							dict_score[feature].append((cluster,score))
						if cluster not in clust_D:
							clust_D[cluster]=[score]
						else:
							clust_D[cluster].append(score)
						
	return dict_score, feature_list, clust_D

#loop through and get significant dictionarys

clust_D= {}
feat_list=[]
dict_score={}

for file in os.listdir(start_dir):
    if file.endswith(".fisher.pqvalue"):
        #name1= file.strip().split("Enrichment_")[1]
        name1= file.strip().split(".fisher")[0]
        name= name1.split("Enrichment_")[1]
        fisherfile = open(start_dir + "/" + file, 'r') # pqvalue file (output of fishers- .pqvalue)
        print (name, "adding file to dictionary")
        lines= fisherfile.readlines()
        dict_score, feat_list, clust_D= get_sigs(lines, dict_score, clust_D, name, feat_list)
        fisherfile.close()
        #title_list.append(name)

print (dict_score, "dict_score ", len(dict_score.keys()))
print ("number of features ", len(feat_list))
print ("number of clusters ", len(clust_D.keys()))

for key1 in list(clust_D):
	datalist= clust_D[key1]
	data1= filter(lambda v: v==v, datalist)
	if all(i < 1.3 and i > -1.3 for i in data1) == True:
		print(key1, "not significant in any feature")
		clust_D.pop(key1, None)
	else:
		pass
		
print ("number of updated clusters ", len(clust_D.keys()))
clust_list= list(clust_D.keys())
print(clust_list)
clust_list.sort()
print(clust_list)
title_str= "\t".join(clust_list)    
oup.write("feature\t%s\n" % (title_str))

#dict_pos_sorted = collections.OrderedDict(sorted(dict_score.items(), reverse=True)) #sorts based on values
print("getting sig clusters and writing matrix")
for feat in feat_list:
	if feat in dict_score.keys():
		data= dict_score[feat]
		tup1_cl_elements = [a_tuple[0] for a_tuple in data]
		tup2_score_elements = [a_tuple[1] for a_tuple in data]
		data2= filter(lambda v: v==v, tup2_score_elements)
		if all(i < 1.3 and i > -1.3 for i in data2) == True:
			pass
			print (feat, "not significant in any cluster")
		else:
			oup.write("%s\t" % feat)
			for clust in clust_list:
				if clust in tup1_cl_elements:
					clind= tup1_cl_elements.index(clust)
					x= tup2_score_elements[clind]
					oup.write("%.3f\t" % (x))
				else:
					oup.write('nan\t')
			oup.write('\n')

oup.close()
