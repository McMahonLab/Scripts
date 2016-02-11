###############################################################################
# parallelBlast.py
# Copyright (c) 2016, Joshua J Hamilton and Katherine D McMahon
# Affiliation: Department of Bacteriology
#              University of Wisconsin-Madison, Madison, Wisconsin, USA
# URL: http://http://mcmahonlab.wisc.edu/
# All rights reserved.
################################################################################
# This script performs an all-vs-all BLAST on multiple cores. The script takes
# as input a fastaFile of sequences for all-vs-all BLASTing. The file is split
# into smaller files, and each is BLASTed against a database created from the
# original list. The results are concatenated together at the end.

# The parameters jobSize and numCores should be specified by the user, along with
# the file and folder structure for the jobs.
################################################################################

#%%#############################################################################
### Import packages
################################################################################
from Bio import SeqIO
from joblib import Parallel, delayed 
import os
import shutil
import subprocess

#%%#############################################################################
### Run parameters
################################################################################
jobSize = 1000 # number of sequences to include in each BLAST
numCores = 25 # number of cores to use

#%%#############################################################################
### User-defined files and folder structure
################################################################################
# Define data folders
genomeFolder = '../genomes' # Location of fasta files
splitFolder = genomeFolder+'/splitFastas' # Location to store split fasta files
fastaFile = genomeFolder+'/good.fasta' # Name of file containing all fastas

blastFolder = '../blast' # location to put BLAST results
blastDBFile = blastFolder+'/proteins.db' # name of BLAST database

# Delete contenst of previous splitFasta folder, if they exist
if os.path.exists(splitFolder):
        shutil.rmtree(splitFolder)
        
# Then recreate the directory
if not os.path.exists(splitFolder):
        os.makedirs(splitFolder)

# Do the same for BLAST results
if os.path.exists(blastFolder):
        shutil.rmtree(blastFolder)
        
if not os.path.exists(blastFolder):
        os.makedirs(blastFolder)

#%%#############################################################################
### Split the file of all protein sequences into smaller files for indidivual jobs
################################################################################
# Courtesy of http://biopython.org/wiki/Split_large_file

def batchIterator(iterator, jobSize) :
    """Returns lists of length jobSize.
 
    This can be used on any iterator, for example to batch up
    SeqRecord objects from Bio.SeqIO.parse(...), or to batch
    Alignment objects from Bio.AlignIO.parse(...), or simply
    lines from a file handle.
 
    This is a generator function, and it returns lists of the
    entries from the supplied iterator.  Each list will have
    batch_size entries, although the final list may be shorter.
    """
    entry = True #Make sure we loop once
    while entry :
        batch = []
        while len(batch) < jobSize :
            try :
                entry = iterator.next()
            except StopIteration :
                entry = None
            if entry is None :
                #End of file
                break
            batch.append(entry)
        if batch :
            yield batch
            
fastaIterator = SeqIO.parse(open(fastaFile),'fasta')

for i, batch in enumerate(batchIterator(fastaIterator, jobSize)) :
    splitFile = splitFolder+'/group_%i.fasta' % (i+1)
    handle = open(splitFile, 'w')
    count = SeqIO.write(batch, handle, 'fasta')
    handle.close()

# Create a list of these files for BLASTing
blastList = []
for blastFile in os.listdir(splitFolder):
    if blastFile.endswith('.fasta'):
       blastList.append(blastFile)
      
blastList = [blastFile.replace('.fasta', '') for blastFile in blastList]

#%%#############################################################################
### Create the BLAST database
################################################################################
subprocess.call(['makeblastdb',
    '-dbtype', 'prot',
    '-in', fastaFile,
    '-input_type', 'fasta',
    '-out', blastDBFile])

#%%#############################################################################
### Define a function to run the BLAST jobs
################################################################################
def runBlast(blastFile):
    subprocess.call(['blastp',
                 '-db', blastDBFile,
                 '-query', splitFolder+'/'+blastFile+'.fasta',
                 '-out', blastFolder+'/'+blastFile+'-vs-all.tsv',
                 '-seg', 'yes', '-soft_masking', 'true',
                 '-max_target_seqs', '1000000', 
                 '-evalue', '1E-5',
                 '-outfmt', '6'])

#%%#############################################################################
### Run the BLAST jobs
################################################################################
Parallel(n_jobs=numCores)(delayed(runBlast)(blastFile) for blastFile in blastList)

#%%#############################################################################
### Put the results back together again
################################################################################

# Iterate over the list of group-vs-all BLAST files and concatenate them
with open(blastFolder+'/all-vs-all.tsv', 'w') as outfile:
    for blastFile in blastList:
        with open(blastFolder+'/'+blastFile+'-vs-all.tsv') as infile:
                outfile.write(infile.read())
                
# Clean up the individual files
for blastFile in blastList:
    os.remove(blastFolder+'/'+blastFile+'-vs-all.tsv')
