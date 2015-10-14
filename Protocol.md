# Running MetaPathways on Zissou
##### Joshua J Hamilton
##### Last Revision: October 13, 2015

## Installation Directories
* Pathways Tools: `/usr/local/pathway-tools`
* PGDBs: `/shared_software/ptools-local/pgdbs/user`
* MetaPathways:		`/shared_software/metapathways2-2.5.2`
* Shared Databases:	`/shared_software/MetaPathways_DBs`

## Overview
This protocol provides instructions on how to use MetaPathways and PathwayTools to annotate genomes and construct a PGDB for the genome. Scripts included with MetaPathways can be used to extract pathway information from the PGDB.

The protocol has two phases. In the first phase, genomes are annotated on Zissou. In the second phase, the annotated genome is converted to a PGDB on a local computer.

Users must be members of the `ptools` group to access the PathwayTools and MetaPathways database folders.

## Software Availability
Pathway Tools Software – currently version 19.0					http://bioinformatics.ai.sri.com/ptools/dist-473256968.html

MetaPathways – currently version 2.5.2
https://github.com/hallamlab/metapathways2.git


## Database Availability
Available through the MetaPathways distribution:  
  * CAZY_2014_09_04  
  * COG_2013-12-27  
  * metacyc-v5-2011-10-21

Manually downloaded:  
  * refseq-2015-09-03
  * SEED-2013-03-13  
  * gg_13_5
  * SILVA_LSURef_2015-07-23
  * SILVA_SSURef_Nr99_2015-07-23

## Pre-requisites
MetaPathways and Pathway Tools installed on your local computer

## Phase 1: Annotating Genomes on the Server
1.	On Zissou, remove the inputs and outputs of all previous runs, by deleting the contents of the following directories:
  * MP input: `/shared_software/metapathways2-2.5.2/input`
  * MP output: `/shared_software/metapathways2-2.5.2/output`
  * PGDBs: `/shared_software/ptools-local/pgdbs/user`  
If the directories are non-empty, contact the file’s owner to make sure you can safely delete them!

2.	Copy your genomes to /shared_software/metapathways2.5/input. Genomes should be in fasta nucleotide format. Genomes can be found on zissou in the data folder, or downloaded from IMG. Note that file names cannot contain internal periods (e.g., MEint.metabat.3163.fna should be renamed MEintmetabat3163.fna.

3.	Ensure the configuration and parameter files are correct.
a.	Configuration: /shared_software/metapathways2.5/config/config_server.txt
Items to check include …

# Paths for the Python …
PYTHON_EXECUTABLE '/usr/bin/python'
PGDB_FOLDER '/data/ptools-local/pgdbs/user'
METAPATHWAYS_PATH '/shared_software/metapathways2.5'
PATHOLOGIC_EXECUTABLE '/usr/local/pathway-tools/aic-export/pathway-tools/ptools/18.0/pathway-tools'
REFDBS '/shared_software/databases'

# Executables
EXECUTABLES_DIR 'executables/ubuntu'

b.	Parameter:       /shared_software/metapathways2.5/ config/param_server.txt
Items to check include …

INPUT:format fasta

annotation:algorithm LAST

annotation:dbs CAZY_2014_09_04, COG_2013-12-27, metacyc-v5-2011-10-21, refseq-nr-2015-03-04, SEED-2013-03-13

rRNA:refdbs greengenes_2013_05, SILVA_119_LSURef_tax_silva_2014-08-12, SILVA_119_SSURef_Nr99_tax_silva_2014-08-12

# pipeline execution flags
metapaths_steps:PREPROCESS_INPUT yes
metapaths_steps:ORF_PREDICTION yes
metapaths_steps:FILTER_AMINOS yes
metapaths_steps:FUNC_SEARCH yes
metapaths_steps:PARSE_FUNC_SEARCH yes
metapaths_steps:SCAN_rRNA yes
metapaths_steps:SCAN_tRNA yes
metapaths_steps:ANNOTATE_ORFS yes
metapaths_steps:BUILD_PGDB skip
metapaths_steps:COMPUTE_RPKM skip

Note: it is important that BUILD_PGDB is set to skip because the Pathway Tools GUI invoked by that step does not work on the server.

4.	From the /shared_software/metapathways2.5 folder, run MetaPathways via the following command:
python MetaPathways.py
-i /shared_software/metapathways2.5/input
-o /shared_software/metapathways2.5/output
-c /shared_software/metapathways2.5/config/config_server.txt
-p /shared_software/metapathways2.5/config/param_server.txt
–v

Information about the command:
-i is the input folder
-o is the output folder
-c is the configuration file
-p is the parameter file
-v tells MetaPathways to run in verbose mode

Your genome has now been annotated! The running time of this command is highly variable. In the worst-case scenario, MetaPathways should take about 1 hr per MB of sequence.

5.	Copy the input and output folders from /shared_software/metapathways2.5 to your home directory. Then, delete the contents of the input and output folders.


Phase 2: Building a PGDB on your local computer

6.	On your local computer, remove the inputs and outputs of all previous runs, by deleting the contents of the following directories.
MP input	/path/to/metapathways2.5/input
MP output	/path/to/metapathways2.5/output
PGDBs		/path/to/ptools-local/pgdbs/user
If the directories are non-empty, copy the folder contents to a safe location!

7.	Copy the MetaPathways input and output from your home directory on zissou to /path/to/metapathways2.5/input and /path/to/metapathways2.5/output, respectively.

8.	Ensure the configuration and parameter files are correct.
a.	Configuration: example on zissou at
/shared_software/metapathways2.5/config_local.txt
Items to check include …

# Paths for the Python …
PYTHON_EXECUTABLE '/path/to/python'
PGDB_FOLDER '/path/to/ptools-local/pgdbs/user'
METAPATHWAYS_PATH '/path/to/metapathways2.5'
PATHOLOGIC_EXECUTABLE '/path/to/pathway-tools/aic-export/pathway-tools/ptools/VERSION/pathway-tools'
REFDBS '/path/to/metapathways2.5/databases'

# Executables
EXECUTABLES_DIR 'executables/yourOS'

b.	Parameter: example on zissou at
/shared_software/metapathways2.5/param_local_buildPGDB.txt
Items to check include …

INPUT:format fasta

annotation:algorithm LAST

annotation:dbs # should be blank
rRNA:refdbs # should be blank

# pipeline execution flags
metapaths_steps:PREPROCESS_INPUT skip
metapaths_steps:ORF_PREDICTION skip
metapaths_steps:FILTER_AMINOS skip
metapaths_steps:FUNC_SEARCH skip
metapaths_steps:PARSE_FUNC_SEARCH skip
metapaths_steps:SCAN_rRNA skip
metapaths_steps:SCAN_tRNA skip
metapaths_steps:ANNOTATE_ORFS skip
metapaths_steps:BUILD_PGDB yes
metapaths_steps:COMPUTE_RPKM skip

Note: it is important that all commands except BUILD_PGDB are set to skip, otherwise MetaPathways will needlessly repeat the analysis you ran on the server.

9.	From the /path/to/metapathways2.5 folder, run MetaPathways via the following command:
python MetaPathways.py
-i /path/to/metapathways2.5/input
-o /path/to/metapathways2.5/output
-c /path/to/metapathways2.5/config/config_local.txt
-p /path/to/metapathways2.5/config/param_local_buildPGDB.txt
-d 8
-v
-r overlay

Information about the command:
-i is the input folder
-o is the output folder
-c is the configuration file
-p is the parameter file
-d 8 closes Pathway Tools and re-open at invocation
-v tells MetaPathways to run in verbose mode
-r overlay accepts pre-existing results

You now have a PGDB! The running time of this command is highly variable. I didn’t time this step, so I don’t know how long it takes.

10.	To run post-processing scripts, from /path/to/pathway-tools invoke Pathway Tools in api mode via the following command: ./pathway-tools –api and follow the examples online at https://github.com/hallamlab/mp_tutorial/wiki/Pathway-Analysis
