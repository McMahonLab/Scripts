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
0. Prior to running MetaPathways, reserve space on the server!  
  * MetaPathways requires 1 processor, consumes 5GB of RAM, and takes about 40 minutes per MB of sequence.  
  * This is an example of a [good reservation](https://www.google.com/calendar/event?action=TEMPLATE&tmeid=YmRlMWlzMjlkYjU5ODRmdGpsc2syODczdmsgYXU1cW9kMHE0bWNyZWM5MXJ2cjFmbXV1NzBAZw&tmsrc=au5qod0q4mcrec91rvr1fmuu70%40group.calendar.google.com).

1.	On Zissou, check the inputs and outputs of all previous runs, by examining the contents of the following directories:
  * MP input: `/shared_software/metapathways2-2.5.2/input`
  * MP output: `/shared_software/metapathways2-2.5.2/output`
  * PGDBs: `/shared_software/ptools-local/pgdbs/user`  
If the directories are non-empty, contact the file’s owner to make move the files to another location.

2.	Copy your genomes to `/shared_software/metapathways2-2.5.2/input`. Genomes should be in `fasta` nucleotide format. File names cannot contain internal periods (e.g., `MEint.metabat.3163.fna` should be renamed `ME3163.fna`.

3.	Ensure the configuration and parameter files are correct.  
  * Configuration file: `/shared_software/metapathways2-2.5.2/config/config_server.txt`.  
  Items to check include:  
          * PYTHON_EXECUTABLE: `/usr/bin/python`
          * PGDB_FOLDER: `/shared_software/ptools-local/pgdbs/user`
          * METAPATHWAYS_PATH: `/shared_software/metapathways2-2.5.2`
          * PATHOLOGIC_EXECUTABLE: `/usr/local/pathway-tools/aic-export/pathway-tools/ptools/19.0/pathway-tools`
          * REFDBS `/shared_software/MetaPathways_DBs`
          * EXECUTABLES_DIR `executables/ubuntu`
    * Parameter file: `/shared_software/metapathways2-2.5./config/param_server.txt`. Items to check include:
          * INPUT:format `fasta`
          * annotation:algorithm `LAST`
          * annotation:dbs `CAZY_2014_09_04, COG_2013-12-27, metacyc-v5-2011-10-21, refseq-2015-09-03, SEED-2013-03-13`
          * rRNA:refdbs `gg_13_5, SILVA_LSURef_2015-07-23, SILVA_SSURef_Nr99_2015-07-23`
          * metapaths_steps:PREPROCESS_INPUT `yes`
          * metapaths_steps:ORF_PREDICTION `yes`
          * metapaths_steps:FILTER_AMINOS `yes`
          * metapaths_steps:FUNC_SEARCH `yes`
          * metapaths_steps:PARSE_FUNC_SEARCH `yes`
          * metapaths_steps:SCAN_rRNA `yes`
          * metapaths_steps:SCAN_tRNA `yes`
          * metapaths_steps:ANNOTATE_ORFS `yes`
          * metapaths_steps:BUILD_PGDB `skip`
          * metapaths_steps:COMPUTE_RPKM `skip`  

          Note: it is important that BUILD_PGDB is set to skip because the Pathway Tools GUI invoked by that step does not work on the server.

4.	From the `/shared_software/metapathways2-2.5.2 folder`, run MetaPathways via the following command:  
      `python MetaPathways.py  
      -i /shared_software/metapathways2-2.5.2/input  
      -o /shared_software/metapathways2-2.5.2/output  
      -c /shared_software/metapathways2-2.5.2/config/config_server.txt  
      -p /shared_software/metapathways2-2.5.2/config/param_server.txt  
      –v`

      Information about the command:  
      `-i` is the input folder  
      `-o` is the output folder  
      `-c` is the configuration file  
      `-p` is the parameter file  
      `-v` tells MetaPathways to run in verbose mode

  Your genome has now been annotated! The running time of this command is highly variable. In the worst-case scenario, MetaPathways should take about 1 hr per MB of sequence.

5.	Copy the input and output folders from /shared_software/metapathways2-2.5.2 to your home directory. Then, delete the contents of the input and output folders.

## Phase 2: Building a PGDB on your local computer

1.	On your local computer, remove the inputs and outputs of all previous runs, by deleting the contents of the following directories.
  * MP input: `/path/to/metapathways2-2.5.2/input`
  * MP output: `/path/to/metapathways2-2.5.2/output`
  * PGDBs: `/path/to/ptools-local/pgdbs/user`

  If the directories are non-empty, copy the folder contents to a safe location!

2.	Copy the MetaPathways input and output from your home directory on Zissou to `/path/to/metapathways2-2.5.2/input` and `/path/to/metapathways2-2.5.2/output`, respectively.

3.	Ensure the configuration and parameter files are correct:  
  * Configuration file: `/path/to/metapathways2-2.5.2/config/config_local.txt`.  
  Items to check include:  
        * PYTHON_EXECUTABLE `/path/to/python`
        * PGDB_FOLDER `/path/to/ptools-local/pgdbs/user`
        * METAPATHWAYS_PATH `/path/to/metapathways2-2.5.2`
        * PATHOLOGIC_EXECUTABLE `/path/to/pathway-tools/aic-export/pathway-tools/ptools/VERSION/pathway-tools`
        * REFDBS `/path/to/metapathways2-2.5.2/databases`
        * EXECUTABLES_DIR `executables/yourOS`
    * Parameter file: `/path/to/metapathways2-2.5./config/param_local.txt`.  
    Items to check include:
        * INPUT:format `fasta`
        * annotation:algorithm `LAST`
        * annotation:dbs # should be blank
        * rRNA:refdbs # should be blank
        * metapaths_steps:PREPROCESS_INPUT `skip`
        * metapaths_steps:ORF_PREDICTION `skip`
        * metapaths_steps:FILTER_AMINOS `skip`
        * metapaths_steps:FUNC_SEARCH `skip`
        * metapaths_steps:PARSE_FUNC_SEARCH `skip`
        * metapaths_steps:SCAN_rRNA `skip`
        * metapaths_steps:SCAN_tRNA `skip`
        * metapaths_steps:ANNOTATE_ORFS `skip`
        * metapaths_steps:BUILD_PGDB `yes`
        * metapaths_steps:COMPUTE_RPKM `skip`

        Note: it is important that all commands except BUILD_PGDB are set to skip, otherwise MetaPathways will needlessly repeat the analysis you ran on the server.

        `python MetaPathways.py  
        -i /shared_software/metapathways2-2.5.2/input  
        -o /shared_software/metapathways2-2.5.2/output  
        -c /shared_software/metapathways2-2.5.2/config/config_server.txt  
        -p /shared_software/metapathways2-2.5.2/config/param_server.txt  
        –v`

      Example parameter and configuration files are available in this repo.

9.	From the `/path/to/metapathways2-2.5.2` folder, run MetaPathways via the following command:  
      `python MetaPathways.py
      -i /path/to/metapathways2-2.5.2/input
      -o /path/to/metapathways2-2.5.2/output
      -c /path/to/metapathways2-2.5.2/config/config_local.txt
      -p /path/to/metapathways2-2.5.2/config/param_local.txt
      -d 8
      -v
      -r overlay`

      Information about the command:
      `-i` is the input folder  
      `-o` is the output folder  
      `-c` is the configuration file  
      `-p` is the parameter file  
      `-d 8` closes Pathway Tools and re-open at invocation  
      `-v` tells MetaPathways to run in verbose mode  
      `-r` overlay accepts pre-existing results  

      You now have a PGDB! On a Mid-2012 MacBook Pro, this step takes approximately 15 minutes per MB of sequence. New Pathway Tools windows will frequently open during this step. We recommend you only run this step when you aren't using your computer for something else.

10.	To run post-processing scripts, from `/path/to/pathway-tools` invoke Pathway Tools in api mode via the following command: `./pathway-tools –api` and follow the examples [online](https://github.com/hallamlab/mp_tutorial/wiki/Pathway-Analysis).
