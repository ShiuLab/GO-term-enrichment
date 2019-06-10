# GO-term-enrichment

## Cluster enrichment
1. get enrichment table with a cluster file

    Need a cluster tab delimited file which lists gene:cluster; cluster file must include negative set (cluster or all genes to be    compared against.
    
    Need a GO term file which contains GO term: gene
    
        python cluster_enrichment_final.py <cluster file> <GO term file>
        
    Output: table for enrichment file: tableforEnrichment_clusterfilename
    
2. do fisher's exact test

  Before doing the FET, purge module and load R modules and reload python:
  
        module purge
        module load GCC/7.3.0-2.30
        module load OpenMPI/3.1.1
        module load R/3.5.1-X11-20180604
        module load Python/3.7.0
  
  Use enrichment table to find significant clusters:
  
       python ~/Github/GO-term-enrichment/Test_Fisher.py tableforEnrichment_D21_down_cluster1.txt 1
       
 3. Get only the significant under (-) or over (+) represented clusters
 
        python ~/Github/GO-term-enrichment/parse_enrichment_get_sig.py <.pqvalue file>
        
 4. Merge GO term description into results file 
 
        python ~/Github/GO-term-enrichment/merge_description.py -key [GO term key] -table [output from step 3] 
        
 ## Variations
