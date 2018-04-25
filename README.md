# GO-term-enrichment

## Cluster enrichment
1. get enrichment table with a cluster file

    Need a cluster tab delimited file which lists gene:cluster; cluster file must include negative set (cluster or all genes to be    compared against.
    
    Need a GO term file which contains GO term: gene
    
        python cluster_enrichment_final.py <cluster file> <GO term file>
        
    Output: table for enrichment file: tableforEnrichment_clusterfilename
    
2. do fisher's exact test

  Use enrichment table to find significant clusters:
  
       python ~/Github/GO-term-enrichment/Test_Fisher.py tableforEnrichment_D21_down_cluster1.txt 1
       
 3. Get only the significant under (-) or over (+) represented clusters
 
        python ~/Github/GO-term-enrichment/parse_enrichment_get_sig.py <.pqvalue file>
        
 ## Variations
