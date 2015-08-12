# Batch Model Building with KBase
Copyright (c) 2015, Joshua J Hamilton  
Contact: joshamilton@gmail.com

This readme will show you how to upload a group of genomes to KBase and build metabolic models for them.

## Usage Instructions
1. Download and install the [KBase Client](https://github.com/ModelSEED/KBaseClient) following the instructions in the readme. Some notes:  

  a. You should install git for this. Follow the instructions from the [McMahon Lab Git Workshop](https://github.com/McMahonLab/git_wksp).  

  b. I was unable to install Carton in my native perl (step 3) and had to follow steps 1 and 2.  

  c. In step 7, the correct command is:  
   `kbase-login kbasetest -p @Suite525`

2. Login to KBase and create a copy of the public narrative [Batch Model Building](https://narrative.kbase.us/narrative/ws.9560.obj.2). This is the narrative we will use to build metabolic models. Delete all the data in your copy of the narrative, as you will upload your own data to it later on.

3. Using the [Workspace Brower](https://narrative.kbase.us/functional-site/#/ws/), find the ID of the workspace containing the narrative you just copied. Your workspaces will be at the top, with the form `username:#################`. The `workspaceID` is the ### part.

4. Download all of your genomes in fasta nucleotide format to a folder `genomeDir`. File names should be of the form `genome.fna`

6. Run the script loadGenomes.pl to push your genomes to KBase:  
`perl loadGenomes.pl username password genomeDir workspaceID`  
where `username` and `password` are your KBase username and password, and `genomeDir` and `workspaceID` are from the above steps.  
If you used perlbrew for this step, feel free to revert to your original perl installation when you're done: `perlbrew off`

7. You should now see your genomes (as `ContigSet`) objects in the narrative we copied above. To build metabolic models, run the code cells in the narrative. (Code cells can be run by selecting the cell and pressing Shift+Enter). This typically takes between 5 and 10 minutes per genome. When you are done, you can download SBML files of the models via the hyperlink generated in the final step.
