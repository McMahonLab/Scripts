# Clean up any results from the previous run
rm -r ../results
mkdir ../results

rm -r pairs
rm mclInput

# Run OrthoMCL
orthomclBlastParser ../blast/all-vs-all.tsv ../genomes/compliant > ../results/similarSequences.txt
orthomclLoadBlast ../orthomcl.config ../results/similarSequences.txt 
orthomclPairs ../orthomcl.config ../results/orthomclPairs.log cleanup=yes
orthomclDumpPairsFiles ../orthomcl.config 

# Move the output from OrthoMCL
mv pairs/ ../results/
mv mclInput ../results/

# Run MCL
mcl ../results/mclInput --abc -I 1.5 -o ../results/mclOutput

# Parse the MCL results
orthomclMclToGroups group 0000 < ../results/mclOutput > ../results/groups.txt
orthomclSingletons ../genomes/good.fasta ../results/groups.txt > ../results/singletons.txt
