import os, sys

start_dir = sys.argv[1]
pathway_file = sys.argv[2]

output = open("clust_enrich_cc.sh", "w")

for file in os.listdir(start_dir):
    #if file.endswith(".sig_expr.txt"):
        #filename = str(start_dir)+"/"+str(file)
        output.write("python ~/Github/GO-term-enrichment/cluster_enrichment_final.py %s %s\n" %(file, pathway_file))

output.close()
