# Scripts

This repo contains scripts, protocols, and workflows for computational analyses.

## Table of Contents

### KBase
Scripts for batch generation of genome-scale metabolic models using KBase.
* `ModelBuilding` - Instructions for batch generation of genome-scale metabolic models using KBase.
* `loadGenomes.pl` - Perl script for pushing local genomes to KBase.

### MetaPathways
Information pertaining to installation of MetaPathways and for building PGDBs using MetaPathways and PathwayTools.
* `MetaPathwaysInstallation.md` - Instructions for installing MetaPathways on the server.
* `MetaPathwaysProtocol.md` - Protocol for building a PGDB
* `Config` and `Param` files - configuration and parameter files for running MetaPathways locally and on the server.

### Phylogeny
Scripts for building phylogenetic trees. Currently only contains scripts for building tree using Phylosift marker genes.

### 16S_sequence_processing
mothur workflow for our 16S time series data. This workflow is designed to start with a BIOM table and .fasta file of unique sequences.
* `16S_deblurred_table_mothur_workflow.docs` - Instructions for running the BIOM table through mothur and explanation of commands and scripts used
* `names_from_shared.R` - Creates a .names file from a .shared file
* `remove_seqs_from_shared.R` - If sequences have been removed from the .names file, this script will also remove these from the .shared file
* `shared_to_count.R'- Converts .shared file to a .count file