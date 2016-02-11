###############################################################################
# faaParser.py
# Copyright (c) 2016, Joshua J Hamilton and Katherine D McMahon
# Affiliation: Department of Bacteriology
#              University of Wisconsin-Madison, Madison, Wisconsin, USA
# URL: http://http://mcmahonlab.wisc.edu/
# All rights reserved.
################################################################################
# Format fasta protein files for use with orthoMCL
################################################################################

#%%#############################################################################
### Import packages
################################################################################

import os
import subprocess
from Bio import SeqIO

#%%#############################################################################
### User-defined files and folder structure
################################################################################
# Define data folders
genomeFolder = '../genomes/faa'
outputFolder = '../genomes/compliant'

# Create the output directory
if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

# Get genome list
genomeList = []
for genome in os.listdir(genomeFolder):
    if genome.endswith('.faa'):
       genomeList.append(genome)

genomeList = [genome.replace('.faa', '') for genome in genomeList]

#%%#############################################################################
### Create a hash for mapping names to taxon IDs
################################################################################
taxonDict = {}
with open('taxonMapping.txt') as dictFile:
    for line in dictFile:
       (key, val) = line.split()
       taxonDict[key] = val
       
#%%#############################################################################
### Read in each FASTA file. Update the file 
################################################################################

for genome in genomeList:
        inFile = open(genomeFolder+'/'+genome+'.faa', 'r')
        outFile = open(outputFolder+'/'+taxonDict[genome]+'.fasta', 'w')
        for record in SeqIO.parse(inFile, 'fasta') :
            record.id = taxonDict[genome]+'|'+ record.description.split()[1]
            record.description = ''
            SeqIO.write(record, outFile, 'fasta')
        inFile.close()
        outFile.close()

#%%#############################################################################
### Subprocess call to orthomclFilterFasta
################################################################################
subprocess.call(['orthomclFilterFasta',
                 outputFolder, '10', '20',
                 '../genomes/good.fasta', '../genomes/bad.fasta' ])
