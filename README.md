# GO-term-enrichment

## Objective
To get enrichment of gene expression clusters using GO-terms or pathways

## Pathway or GO term formatting
Files downloaded from PMN (Plant Metabolic Network) or GO (gene ontology) need to be formatted correctly for the next steps.

### Pathway files
1. Obtain pathway file downloaded from PMN for your species: https://pmn.plantcyc.org/ containing the pathway and genes annotated to that pathway
2. Get the file into pathway:gene format:

        python parse_plantcyc_file_getpath-gene.py <pathway file from PMN> <index where genes are> <index where pathway name is> <index where path ID is>
        
        example:
        
        python ~/Desktop/post_doc/scripts/2_coexpress_pthwy/parse_plantcyc_file_getpath-gene.py All_instances_of_Pathways_in_Zea_mays_mays.txt 3 0 5

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
        
 4. Merge GO term description into results file 
 
        python ~/Github/GO-term-enrichment/merge_description.py -key [GO term key] -table [output from step 3] 
        
 ## Variations
