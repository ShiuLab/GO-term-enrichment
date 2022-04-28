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

OPTIONAL: If needed, convert gene IDs from pathway file to IDs from your expression data
NEEDED: a BLAST recipricol best match file

        python covert_geneIDs_pathfile.py <BLAST recipricol best match> <pathway file>

### GO term files
1. obtain go.obo file from http://geneontology.org/docs/download-ontology/
2. parse to get GOID: function

        python parse_GO_obo-ID-func.py <go.obo file>

3. for GO term: gene file, need gene associations

### Pfam annotation
1. obtain pfamA.tsv file from http://ftp.ebi.ac.uk/pub/databases/Pfam/Pfam-N/

### gene association
To associate genes, get gene association file from phytozome- this has gene and their pfam IDs and GO IDs
1. https://phytozome-next.jgi.doe.gov/ 
2. sign in and click on species of interest.
3. go to standard data files, select .annotation_info.txt file and download
4. use annotation file, pfamA.tsv file, and go.obo.v1.2_parsed.txt to make table with descriptions:

        python parse_phytozome_ann.py -ann_file <.annotation_info.txt> -pfam_file pfamA.tsv -go_file go.obo.v1.2_parsed.txt -pfam_ind <index with pfam IDs> -go_ind <index with goIDs> -split_by <how pfamIDs and goIDs are delimited- usually a ,>
        
        result: .annotation_info.txt.parsed.txt file with pfam and Go descriptions

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
