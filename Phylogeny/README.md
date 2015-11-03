# Building Phylogenetic Trees From Marker Genes

Copyright (c) 2015, Joshua J Hamilton
Contact: joshamilton@gmail.com

This readme will show you how to build a phylogenetic tree using a concatenated alignment of 37 marker genes.

## Prerequisites
*  [Phylosift](https://phylosift.wordpress.com/) - Software for extracting and aligning marker gene sequences. This software can be installed and run locally or on the server.

* [FastTree](http://www.microbesonline.org/fasttree/) - Software for rapidly building phylogenetic trees. Installed along with Phylosift.

*  [RAxML](http://sco.h-its.org/exelixis/web/software/raxml/index.html) - Software for building phylogenetic trees via maximum likelihood. You should install this in your `home` folder on the lab server, but it also accessible via the [CIPRES Science Gateway](https://www.phylo.org/).

## Building Phylogenetic Trees

**Input**

* A set of `fasta` files in nucleotide format. One per genome. For ease of use, genome names should contain alphanumeric characters only. No spaces and no symbols.

**Workflow**

1. For each genome, contigs are concatenated into a continuous alignment:

    `perl 01FastaSequenceMerger.pl`

Steps 2 to 4 should be run from the `Phylosift` installation directory.

2. Phylosift extracts marker genes from each genome:

    `perl 02RunPyhlosift.pl`

3. For each genome, marker genes are concatenated into a continuous alignment:

    `perl 03CreateAlignmentFile.pl`

    The concatenated alignment should be called ```lineage.aln```, where lineage is a short lineage name (acI, CAP, etc).

4. Construct an approximate maximum-likelihood phylogenetic tree using FastTree:

    `./bin/FastTree lineage.aln > lineageFastTree.nwk`

    If the tree looks good ...  

Step 5 should be run from the `RAxML` installation directory.

5. Constuct a maximum-likelihood tree using RAxML using 100 rapid bootstraps:


    ```./raxmlHPC-PTHREADS-AVX -f a -m PROTGAMMAAUTO -p 12345 -x 12345 -# 100 -s lineage.aln -T 24 -n lineage```

    RAxML will generate the following output files:  
    - ```RaxML_info.lineage``` - information about call to RAxML  
    - ```RAxML_bestTree.lineage``` - best ML tree  
    - ```RAxML_bipartitions.lineage``` - best ML tree with bootstrap support values. Suitable for viewing in ```FigTree``` or another program.  
    - ```RAxML_bipartitionsBranchLabels.lineage``` - same as above but with bootstrap values displayed as branch (instead of node) labels  
    - ```RAxML_bootstrap.lineage``` - contains all boostrap trees  
