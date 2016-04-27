###############################################################################
# Preprocessing.py
# Copyright (c) 2016, Joshua J Hamilton and Katherine D McMahon
# Affiliation: Department of Bacteriology
#              University of Wisconsin-Madison, Madison, Wisconsin, USA
# URL: http://http://mcmahonlab.wisc.edu/
# All rights reserved.
################################################################################
# Alternative preprocessing script for MetaPathways. Written to bypass the
# problem of MetaPathways handling of contigs with ambiguous nucleotides.

# Operates on the list of genomes in /path-to-metapathways/input
# First, identifies those genomes which contain ambiguous nucleotides.
# Second, renames contigs to be of the form genome_#
# Third, drops all contigs shorter than the specified length (180 bp)
################################################################################

#%%#############################################################################
### Import packages
################################################################################
import os
import re
import pandas as pd
from Bio import SeqIO

#%%#############################################################################
### Define folder structure
################################################################################
inputFolder = '../input'
outputFolder = '../output'
inputExtension = '.fna'
lengthThreshold = 180 
badNucleotide = set('MRWSYKVHDBXN')

#%%#############################################################################
### Generate the list of genomes
genomeList = []
for genome in os.listdir(inputFolder):
    if genome.endswith(inputExtension):
       genomeList.append(genome.rstrip(inputExtension))

################################################################################

badGenomeSet = set()

for genome in genomeList:
    # Create an empty data frame to store the mapping info
    mappingTable = pd.DataFrame(columns=['MP ID', 'IMG ID', 'Length'])
    
    # Create output directory and a fileHandle to write the output
    if not os.path.exists(outputFolder+'/'+genome+'/preprocessed'):
        os.makedirs(outputFolder+'/'+genome+'/preprocessed')
    fastaHandle = open(outputFolder+'/'+genome+'/preprocessed/'+genome+'.fasta', "w")

    # Define sequence number
    seqNum = 0

    # Boolean to monitor if we've found a bad sequence        
    skip=False

    # Iterate over sequence records
    for seqRecord in SeqIO.parse(inputFolder+'/'+genome+inputExtension, 'fasta'):
            
        # Check that the sequence meets the length threshold
        if len(seqRecord) > lengthThreshold:

            # If the sequence contains a bad nucleotide, update the badGenomeSet
            if skip == False:
                if any((nucleotide in badNucleotide) for nucleotide in seqRecord.seq):
                    badGenomeSet.add(genome)
                # Update the Boolean so we stop checking
                    skip = True

            # Create a new entry for the mapping table
            mappingTable = mappingTable.append(pd.DataFrame([[genome+'_'+str(seqNum), seqRecord.id, len(seqRecord)]], columns=['MP ID', 'IMG ID', 'Length']))

            # Write the new sequence to file
            fastaHandle.write('>'+genome+'_'+str(seqNum)+'\n')
            fastaHandle.write(str(seqRecord.seq)+'\n')

            # Increase sequence number
            seqNum = seqNum + 1

    # Close the fasta file
    fastaHandle.close()
    
    # Write the mapping table to file
    mappingTable[['Length']] = mappingTable[['Length']].astype(int)
    mappingTable.to_csv(outputFolder+'/'+genome+'/preprocessed/'+genome+'.mapping.txt', sep='\t', header=False, index=False)
    

# Write the list of bad genomes to file
badGenomeHandle = open('badGenomes.txt', "w")
for genome in badGenomeSet:
  badGenomeHandle.write(genome+'\n')
badGenomeHandle.close()
