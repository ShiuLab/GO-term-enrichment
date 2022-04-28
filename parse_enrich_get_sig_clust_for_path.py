## loop through .fisher.pqvalue files
## get specific pathway
## get enriched clusters in that pathway
## if no cluster enriched, go to next file
## if cluster enriched, get other clusters with pathway genes in that file
## option to just get all significant clusters (not just for specific pathway)
import sys, os

# default:
pthwy_list="NA"
for i in range (1,len(sys.argv),2): 
	if sys.argv[i] == "-dir":
		start_dir = sys.argv[i+1] #directory with .fisher.pqvalue files
	if sys.argv[i] == "-split":
		splitby= sys.argv[i+1]  #what is the dividing character between cluster and pathway in enrichment file
	if sys.argv[i] == "-path":
		pthwy_list= sys.argv[i+1].strip().split(',')
		pthwy_list = [str(j) for j in pthwy_list] #convert items to string
oup = open(start_dir + "/sig_path_enriched_clusters.txt", "w")


def get_sigs(fisherfile, oup, name2, pthwy_list):
    D={}
    sig_pth_list=[]
    print(pthwy_list)
    for line in fisherfile:
        x = line.strip().split('\t')
        a = x[5]
        q = float(x[7])
        path = str(x[0].split(str(splitby))[0])
        cluster = str(x[0].split(str(splitby))[1])
        line_list= x[1:]
        if path in pthwy_list:
            if a == '+':
#                 D[(path,cluster)]=line_list
                if q <= 0.05:
                     print(path,cluster)
                     datastr= "\t".join(line_list)
                     oup.write("%s\t%s\t%s\t%s\n" % (name2, path, cluster, datastr))
#                     if path not in sig_pth_list:
#                         sig_pth_list.append(path)
#     if sig_pth_list != []:
#         print(D)
#         for path in sig_pth_list:
#             for key in D.keys():
#                 data=D[key]
#                 if path == key[0]:
#                     tup=(name2,key[0],key[1])
#                     tup_str= "\t".join(tup)
#                     datastr= "\t".join(data)
#                     oup.write("%s\t%s\n" % (tup_str, datastr))
#     else:
#         pass

def get_sigs2(fisherfile, oup, name2):
    for line in fisherfile:
        x = line.strip().split('\t')
        #print(x)
        a = x[5]
        q = float(x[7])
        path = str(x[0].split(str(splitby))[0])
        cluster = str(x[0].split(str(splitby))[1])
        line_list= x[1:]
        if a == '+':
            if q <= 0.05:
                datastr= "\t".join(line_list)
                oup.write("%s\t%s\t%s\t%s\n" % (name2, path, cluster, datastr))
                
oup.write("file\tpathway\tcluster\tpos-pos\tpos-neg\tneg-pos\tneg-neg\tenrich\tpval\tqval\n")
for file in os.listdir(start_dir):
    if file.endswith(".fisher.pqvalue"):
        name1= file.strip().split("Enrichment_")[1]
        name= name1.strip().split(".fisher")[0]
        fisherfile = open(start_dir + "/" + file, 'r') # pqvalue file (output of fishers- .pqvalue)
        print (name)
        lines= fisherfile.readlines()
        print("getting significant pathway clusters from file")
        if pthwy_list== 'NA':
            get_sigs2(lines, oup, name)
        else:
            get_sigs(lines, oup, name, pthwy_list)
        fisherfile.close()

oup.close()