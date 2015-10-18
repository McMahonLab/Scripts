# Installing MetaPathways
##### Joshua J Hamilton  
##### Last Revision: October 13, 2015

Details on MetaPathways installation can be found on the [MetaPathways wiki](https://github.com/hallamlab/metapathways2/wiki). This document contains additional details for installing the software for our lab.

## Installing Pathway Tools
Pathway Tools must be installed by a user with `root` privileges. As of October 2015, that user is Sarah Stevens.

## Installing MetaPathways
MetaPathways can be downloaded from the [MetaPathways Github site](https://github.com/hallamlab/metapathways2/releases). Download and extract the source code, and place the folder on Zissou in `/shared_software`.

Note: Consult with the server administrator if you do not have read and write privileges to this folder.

## Installing Databases
Databases are sourced from a variety of locations on the Internet. The following databases must be downloaded and installed:

### Database Availability
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

### Database Installation

#### **MetaCyc Databases**
1. Download the MetaPathways_DBs.zip and CAZY_2014_09_04.zip folders from the [MetaPathways Github site](https://github.com/hallamlab/metapathways2/releases).  
2. Extract both folders, and place the `CAZY_2014_09_04` file inside `MetaPathways_DBs/functional`.  
3. Remove the `LSURef_115_tax_silva_2013-12-12` file from `MetaPathways_DBs/taxonomic`, as there is a newer version available.
4. Place the `MetaPathways_DBs` folder on Zissou in `/shared_software`.

#### **NCBI RefSeq**
1. Download the [NCBI batch downloader script](http://www.ncbi.nlm.nih.gov/blast/docs/update_blastdb.pl) and place it in `MetaPathways_DBs/functional`.  
2. Run the command `perl update_blastdb.pl refseq_protein` to download the databases. This takes approximately 90 minutes.  
3. Extract the archives using ``for a in `ls *.tar.gz`; do tar -zxvf $a; done``.  
4. When done, delete the original `.tar.gz` files: `rm *.tar.gz`.
5. Extract the FASTA sequences from the `refseq_protein` database using the `blastdbcmd` command: `blastdbcmd -db refseq_protein -dbtype prot -entry all -outfmt %f -out refseq-YYYY-MM-DD`, where `YYYY-MM-DD` corresponds to the date of the latest release. This takes approximately 30 minutes.  
6. Delete the original databases: `rm refseq_protein*`.

#### ** SEED Database **
1. Navigate to the `MetaPathways_DBs/functional` folder on Zissou.
2. Connect to The SEED [FTP server](ftp://ftp.theseed.org) by entering the following commands at the prompt:  
  a. `ftp`: start the FTP client  
  b. `passive`:  set the FTP to passive mode, which tells the FTP server that all connections will be initiated on the client side (basically to prevent commands from the server being blocked by the firewall)  
  c. `open ftp.theseed.org`: initiate connection
3. At the prompt, enter `anonymous` as the username, and your e-mail address as the password.
4. Navigate to the directory containg The SEED's `fasta` files: `cd genomes/SEED/`
6. Download the `fasta` file: `get all.faa.gz`. (This takes approximately 15 minutes.)
7. Exit the ftp client: `quit`
8. Extract the `fasta` file: `gzip -d all.faa.gz`. (This takes approximately 5 minutes.)
9. Rename it to `SEED-YYYY-MM-DD`, where `YYYY-MM-DD` corresponds to the date of the latest release.

#### ** GreenGenes Database **
1. Download the latest [GreenGenes](http://greengenes.secondgenome.com) database (`gg_13_5.fasta.gz`) and taxonomy (`gg_13_5_taxonomy.txt.gz`) files.
2. Extract the files and place them in `MetaPathways_DBs/taxonomic` on Zissou. Remove the `.fasta` extension.

#### ** SILVA Database **
1. Download the latest SSU (`SILVA_123_SSURef_Nr99_tax_silva.fasta`) and LSU (`	SILVA_123_LSURef_tax_silva.fasta`) databases from [SILVA](http://www.arb-silva.de/no_cache/download/archive/release_123/Exports/). Databases should be in `.fasta` format.
2. Extract the files and rename them to `SILVA_LSURef_YYYY-MM-DD` and
`SILVA_SSURef_Nr99_YYYY-MM-DD`, where `YYYY-MM-DD` corresponds to the date of the latest release.
3. Place the files in `MetaPathways_DBs/taxonomic` on Zissou. Remove the `.fasta` extension.

## Formatting the Databases
After the databases are installed they must be formatted. The easiest way to do this is to call MetaPathways without any input, skipping all pipeline execution flags. (Instructions for running MetaPathways are available in MetaPathwaysProtocol.md. Use the parameter file `param_formatDBs.txt`) If the databases are unformatted, MetaPathways will attempt to format them. This process takes around 12 hours.
