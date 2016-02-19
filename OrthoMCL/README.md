OrthoMCL
===
Copyright (c) 2016, Joshua J. Hamilton
URL: [https://github.com/joshamilton/](https://github.com/joshamilton/)  
All rights reserved.

Overview
---
This document describes how to use OrthoMCL to construct a set of orthologs from a set of genomes. For more on OrthoMCL, consult the original [publication](http://genome.cshlp.org/content/13/9/2178.full).

Prerequisites
---
* [OrthoMCL](http://www.OrthoMCL.org/OrthoMCL/) - Software for finding orthologs.
* [blastp](http://www.ncbi.nlm.nih.gov/books/NBK279690/) - Called by OrthoMCL to identify candidate orthologs.
* [mcl](http://micans.org/mcl/) - Called by OrthoMCL to cluster genes into ortholog groups.
* [MySQL](https://www.mysql.com/) - Used by OrthoMCL to store the data.

As of 2016-02-11, all of this software is installed on Zissou. Should you need to reinstall it, the following links may be helpful

* The [published protocol](http://onlinelibrary.wiley.com/doi/10.1002/0471250953.bi0612s35/full) for installing and running OrthoMCL
* [Biostars tutorial](https://www.biostars.org/p/120773/) for installing OrthoMCL
* [Github tutorial](https://github.com/apetkau/OrthoMCL-pipeline/blob/master/INSTALL.md) for installing OrthoMCL

Getting Started
---

The initial folder structure should look like the following.

    ├── README.md               # This document
    ├── genomes                 # Folder containing genomes
    │   ├── faa                 # Folder containing individual proteomes in fasta amino acid format
    ├── OrthoMCL.config         # Configuration file for OrthoMCL
    ├── scripts                 # Folder containing script to run this workflow
    │   ├── 01faaParser.py      # Converts faa files to an OrthoMCL compatabile format
    │   ├── 02parallelBlast.py  # Runs the all-vs-all BLAST job in parallel
    │   ├── 03setupMySql.sh     # Prepare the MySQL DB for use with OrthoMCL
    │   ├── 04runOrthoMCL.sh    # Run OrthoMCL
    │   ├── 05parseCOGs.py      # Parse the OrthoMCL output.
    │   └── taxonMapping.txt    # File containing a linkage between your fasta file names and OrthoMCL-compliant four-letter codes

You will need to create the `genomes\faa` folder and `taxonMapping.txt` files as follows:

* `genomes\faa` - This folder should contain a proteome file for each of your genomes. Files should called `genome.fasta`. Fasta headers should be of the format:

        >genome locusTag product

in order to be compatabile with later scripts.

* `taxonMapping.txt` - OrthoMCL requires all proteomes to be named xxxx.fasta, where xxxx is a unique four-letter code. The file `taxonMapping.txt` should be a tab-separated file giving a unique code for each fasta file, where the first column is `genome` and the second column is the code. For example:

        AAA023D18	nokf
        AAA023J06	vaue

Workflow
---

The workflow consists of four scripts, summarized below.

* `01faaParser.py` - This file converts the fasta files in `genomes\faa` to a OrthoMCL-compliant format. The results are stored in `genomes\compliant`. Also creates a single file `genomes\good.fasta` for the all-vs-all BLAST job.

* `02parallelBlast.py` - This file runs the all-vs-all BLAST on multiple processors by splitting the all-vs- all job into multiple some-vs-all jobs. Users can specify the number of processors (`numCores`) and number of sequences in each some-vs-all job (`jobSize`). Also creates the BLAST database `blast\proteins.db` and aggregates the BLAST results into `blast\all-vs-all.tsv`.

* 03setupMySql.sh - Prepares the MySQL database for use with OrthoMCL.

* 04runOrthoMCL.sh - Runs OrthoMCL. Results are stored in the `results` folder.

* 05parseCOGs.py - Processes the MCL output into reader-friendly tables, as described:

  * cogTable.csv - Rows are COGs. Columns are genomes. Matrix elements are gene loci for each (COG, genome) pair, if such a locus exists.
  * annotTable.csv - Rows are COGs. Columns are genomes. Matrix elements are gene annotation for each (COG, genome) pair, if such a locus exists. If annotation is given, the entry will state 'None Provided.'
  * annotSummary.csv - Rows are COGs. Lists all annotations associated with that COG across all genomes.

They are configured to be run from the `scripts` folder.

Final Folder Structure
---

When the workflow is complete, your directory should look as follows:

    ├── README.md                 # This document
    ├── blast                     # Folder containing BLAST information
    │   ├── all-vs-all.tsv        # Results of all-vs-all BLAST
    │   ├── proteins.db.phr       # BLAST database
    │   ├── proteins.db.pin       # BLAST database
    │   └── proteins.db.psq       # BLAST database
    ├── genomes                   # Folder containing genomes
    │   ├── bad.fasta             # FASTA file of proteins which will be left out of ortholog search. Determined by OrthoMCL.
    │   ├── compliant             # OrthoMCL-compliant FASTA proteome files
    │   ├── faa                   # Folder containing individual proteomes in fasta amino acid format
    │   ├── good.fasta            # FASTA file of proteins for ortholog search. Determined by OrthoMCL.
    │   └── splitFastas           # FASTA files for some-vs-all BLAST jobs
    ├── OrthoMCL.config           # Configuration file for OrthoMCL
    ├── results
    │   ├── groups.txt            # Ortholog groups
    │   ├── mclInput              # Input to MCL
    │   ├── mclOutput             # Outout to MCL
    │   ├── OrthoMCLPairs.log     # OrthoMCL gene-gene pairs which are used by MCL
    │   ├── pairs
    │   │   ├── coorthologs.txt   # Co-orthologs
    │   │   ├── inparalogs.txt    # In-paralogs
    │   │   └── orthologs.txt     # Orthologs
    │   ├── similarSequences.txt  # Candidates for ortholog pairs
    │   └── singletons.txt        # Proteins which don't belong to an ortholog group
    ├── scripts                   # Folder containing script to run this workflow
    │   ├── 01faaParser.py        # Converts faa files to an OrthoMCL compatabile format
    │   ├── 02parallelBlast.py    # Runs the all-vs-all BLAST job in parallel
    │   ├── 03setupMySql.sh       # Prepare the MySQL DB for use with OrthoMCL
    │   ├── 04runOrthoMCL.sh      # Run OrthoMCL
    │   ├── 05parseCOGs.py      # Parse the OrthoMCL output.
    │   └── taxonMapping.txt      # File containing a linkage between your fasta file names and OrthoMCL-compliant four-letter codes
