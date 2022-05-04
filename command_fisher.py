import os, sys

start_dir = sys.argv[1]
qval = sys.argv[2]

output = open("fisher_cc.sh", "w")

for file in os.listdir(start_dir):
    if file.startswith("tableforEnrichment_"):
        #filename = str(start_dir)+"/"+str(file)
        output.write("python ~/Github/GO-term-enrichment/Test_Fisher.py %s %s\n" %(file, qval))

output.close()
