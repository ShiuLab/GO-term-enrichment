"""
python Test_Fisher.py file 0 #without q-value
  
python Test_Fisher.py file 1 # with q-value
05 08 2008, Revice it to two tail

0800805 add a choice about calculate q-value or not

                           |  having a given property    |  not having a given property
---------------------------------------------------------------------------------------
subset of  population      |           t1                |              t2
the rest of  population    |           t3                |              t4


    t1 number of objects in the subset having a given property
    t2 number of objects in the subset without a given property

    t3 number of objects not in the subset having this property
    t4 number of objects not in the subset without a given property
"""
## make sure enrichment table does not have quotes "" otherwise will not work- R gets columns confused
##fisher package on hpc is fisher/0.1.4
def fisher(tuple_t):# every 4 number tuple
	global t
	"""
    * k number of objects in the selection having a given property
    * n size of the selection
    * C number of objects in the population having this property
    * G size of the population
    * two sided is defaulttail
	"""
	t1=int(tuple_t[0])
	t2=int(tuple_t[1])
	t3=int(tuple_t[2])
	t4=int(tuple_t[3])

	f = FisherExactTest()
	p=f.pvalue(t1,t2+t1,t1+t3,t1+t2+t4+t3)
	en=f.enrichment(t1,t2+t1,t1+t3,t1+t2+t4+t3)
	#print(en)
	if type(en) == float:
	    if en >= 1:
	       en="+" #using right hand side Ha :u
	    else:
	       en="-"
	    
	else:
	   en= 'NA'
		
	#print p
 
	pv=p[t]
	#print pv
	return en,pv

def get_q(file,path):
	
	tmpR=open("%s_tmp.R" % file,"w")
	tmpR.write("setwd(%r)\n" % ("%s"  % path))
	tmpR.write("source(%r)\n" % "~/Desktop/Github/GO-term-enrichment/qvalue.R")
	tmpR.write("test<-read.table(%r,header=F)\n" % ("%s" % file))
	tmpR.write("Q<-qvalue(test$V7,pi0.method=%r,lambda=0)\n" % "bootstrap")
	tmpR.write("q<-Q$qvalue\n")
	tmpR.write("test$V8<-q\n")
	tmpR.write("write.table(test,file=%r,quote=F,eol= %r ,row.names=F,col.names=F,sep=%r)\n" % ('%s.qvalue' % file,'\n','\t'))
	tmpR.close()
	#os.system("module purge")
	#os.system("module load GCC/7.3.0-2.30")
	#os.system("module load OpenMPI/3.1.1")
	#os.system("module load R/3.5.1-X11-20180604")
	#os.system("module load Python/3.7.0")
	os.system("R CMD BATCH %s_tmp.R" % file)
	#os.system("R --vanilla --slave %s_tmp.R" % file)


if __name__ == '__main__':
	
	import os,sys
	#sys.path.append("/mnt/home/seddonal/scripts/6_motif_mapping")
	sys.path.append("~/Desktop/Github/GO-term-enrichment")
	from fisher import FisherExactTest
	
	if len(sys.argv)<3:
		print  ("1 :  5 column	 2X2 table")
		print  ("2 :	1 or 0 1: calculate the q-value,0:do not calculate")
		print  ("3 : left,right ,two  ---left-sided,right-sided or two-sided test")
	file=sys.argv[1]
	q=sys.argv[2] # 1 or 0 1: calculate the q-value,0:do not calculate

	try:
		t= sys.argv[3]
		if sys.argv[3]=="left":
			t=0
		elif sys.argv[3]=="right":
			t=1
	except IndexError:
		t= 2
	
	path = os.getcwd()
	print (path)

	temp_fisher=open("%s_temp_fisher.test" % file,"w")
	overflow   = open("%s_overflow_error" % file, 'w')
	for line in open(file,"r"):
		L=line.strip().split("\t")
		if len(L)==5:

			try:
				result = fisher(L[1:])
			except OverflowError:
				overflow.write(line)
			else:
				temp_fisher.write("%s\t%s\t%s\t%s\n" % (L[0],"\t".join(L[1:]),result[0],result[1]))

	temp_fisher.close()
	
	if q=="0":
		os.system("mv %s_temp_fisher.test %s.fisher.pqvalue" % (file,file))
		os.system("rm %s_overflow_error" % file)
		
	if q=="1":

		get_q("%s_temp_fisher.test" % file,path)
		 
		os.system("mv %s_temp_fisher.test.qvalue %s.fisher.pqvalue" % (file,file))
# 
		os.system("rm %s_temp_fisher.test_tmp.R" % file)
		os.system("rm %s_temp_fisher.test_tmp.Rout" % file)
		os.system("rm %s_temp_fisher.test" % file)
		os.system("rm %s_overflow_error" % file)

