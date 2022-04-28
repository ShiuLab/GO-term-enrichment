import sys, os
import pandas as pd
import numpy as np
import statsmodels
from statsmodels import robust


def main():

    for i in range (1,len(sys.argv),2):
            if sys.argv[i] == "-df":
                DF1 = sys.argv[i+1]

    df = pd.read_csv(DF1, sep='\t', index_col = 0)

    # def get_MAD_stat(inp): #input is a numpy matrix)
    #     result= robust.mad(inp, axis=1)
    #     #result: array([ 2.22390333,  5.18910776]) ##returns an array
    #     return (result)

    def get_max_med_stat(inp):
        #for each row in inp
        resultmax = max(inp)
        resultmed = np.median(inp)
        return (resultmax, resultmed)
        
    df2= pd.DataFrame(data=robust.mad(df, axis=1), index=df[1:,0], columns='MAD')
    #df2['MAD']= robust.mad(df, axis=1)
    df2['max','median']= df.apply(get_max_med_stat, axis=1)
    print (df2)
    df2.to_csv(path_or_buf=str(DF1)+".MAD_max_med.txt", sep="\t", header=True)
        
if __name__ == '__main__':
	main()