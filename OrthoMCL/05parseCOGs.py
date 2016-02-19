###############################################################################
# parseCOGs.py
# Copyright (c) 2016, Joshua J Hamilton and Katherine D McMahon
# Affiliation: Department of Bacteriology
#              University of Wisconsin-Madison, Madison, Wisconsin, USA
# URL: http://http://mcmahonlab.wisc.edu/
# All rights reserved.
################################################################################
# Rearrange groups.txt output from OrthoMCL into a more usable format
################################################################################

#%%#############################################################################
### Import packages
################################################################################

from Bio import SeqIO
import math
import pandas as pd

#%%#############################################################################
### User-defined files and folder structure
################################################################################
genomeFolder = '../genomes/faa'
resultsFolder = '../results'

#%%#############################################################################
### Create a hash for mapping names to taxon IDs
### Create a dataFrame to store the results
################################################################################

taxonDict = {}
with open('taxonMapping.txt') as dictFile:
    for line in dictFile:
       (val, key) = line.split() 
       taxonDict[key] = val
       
inCogDict = {}
with open(resultsFolder+'/groups.txt') as dictFile:
    for line in dictFile:
       (key, val) = line.split(':') 
       inCogDict[key] = val

outCogFrame = pd.DataFrame(index=inCogDict.keys(), columns=taxonDict.values())

#%%#############################################################################
### Parse the inCogDict
### For each key, split the line on whitespace
### For each element, split along the '|'
### Use the prefix to look up the genome in taxonDict
### Write the results to the appropriate dataFrame element
################################################################################

for key in inCogDict.keys():
    cogList = inCogDict[key].split()
    for cogLocus in cogList:
        code = cogLocus.split('|')[0]
        locus = cogLocus.split('|')[1]
#        locus = locus.split('.')[2]+'.'+locus.split('.')[3]
        outCogFrame.loc[key, taxonDict[code]] = locus

outCogFrame.to_csv(resultsFolder+'/cogTable.csv')

#%%#############################################################################
### Assign annotations to COGs
### For each genome (column of outCogFrame), read the annotation information
### into a hash.
### For each cog in that genome, look up the annotation and assign it to
### cogAnnotFrame
################################################################################

cogAnnotFrame = outCogFrame

for genome in outCogFrame.columns:
# Create the annotation hash
    annotHash = {}        
    inFile = open(genomeFolder+'/'+genome+'.faa', 'r')
    for record in SeqIO.parse(inFile, 'fasta'):
        locus = record.description.split()[1]
#        locus = locus.split('.')[2]+'.'+locus.split('.')[3]
        annotation = record.description.split()[2:]
        annotation = ' '.join(annotation)
        if not annotation:
            annotation = 'None Provided'
        annotHash[locus] = annotation
    
    for index in cogAnnotFrame.index:
        if not pd.isnull(cogAnnotFrame.loc[index, genome]):
            cogAnnotFrame.loc[index, genome] = annotHash[outCogFrame.loc[index, genome]]
        
    inFile.close()
    
cogAnnotFrame.to_csv(resultsFolder+'/annotTable.csv')

#%%#############################################################################
### Extract uniqe annotations
### Create a empty DF indexed by groups
### For each group, extract unique annotations and drop 'nan'
### Add to dataframe
################################################################################

annotSummary = pd.DataFrame(index=inCogDict.keys(), columns=['Annotations'])

for group in cogAnnotFrame.index:
    annotation = cogAnnotFrame.loc[group].unique()
    annotation = annotation[~pd.isnull(annotation)]
    annotation = '; '.join(annotation)
    annotSummary.loc[group] = annotation.strip(';')

annotSummary.to_csv(resultsFolder+'/annotSummary.csv')