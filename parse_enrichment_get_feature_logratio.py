import sys, os, math, numpy

enrichment_file = open(sys.argv[1], 'r') # enrichment_table.txt.fisher.pqvalue
output = open(sys.argv[1] + '_percent_logratio.txt', 'w')
output.write("feature\tclass\tenrichment\tpercent_pos\tpercent_neg\tlogratio\n")
def get_logratio(inp, output):
    for line in inp:
        L2 = line.strip().split('\t')
        feature = L2[0]
        class1 = L2[1]
        SM_dom = L2[2]
        not_SM_dom = L2[3]
        other_dom = L2[4]
        not_other_dom = L2[5]
        enrich = L2[6]
        qval = L2[8]
        if float(qval) < 0.05:
            percent_SM = (float(SM_dom))/(float(not_SM_dom))*100
            percent_other = (float(other_dom))/(float(not_other_dom))*100
            if percent_other == 0:
                #logratio_secother = numpy.log2(float(percent_SM))
                logratio_secother = 'NA'
            else:
                logratio_secother = numpy.log2(float(percent_SM)/float(percent_other))
            output.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (feature, class1, enrich, percent_SM, percent_other, logratio_secother))

    
get_logratio(enrichment_file, output)

output.close()
enrichment_file.close()            
