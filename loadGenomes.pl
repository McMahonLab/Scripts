###############################################################################
# loadGenomes.pl
# Copyright (c) 2015, Joshua J Hamilton and Katherine D McMahon
# Affiliation: Department of Bacteriology
#              University of Wisconsin-Madison, Madison, Wisconsin, USA
# URL: http://http://mcmahonlab.wisc.edu/
# All rights reserved.
################################################################################
# Load genomes into a KBase workspace. Converts fasta files to proper format then
# pushes to KBase. Inputs are a genome directory and a workspace ID.
################################################################################

#!/usr/bin/env perl
use strict;
use warnings;
# Taken from sample script from Chris Henry
use Bio::KBase::workspace::ScriptHelpers qw(printObjectInfo get_ws_client workspace workspaceURL parseObjectMeta parseWorkspaceMeta printObjectMeta);
use Bio::KBase::fbaModelServices::ScriptHelpers qw(save_workspace_object get_workspace_object fbaws get_fba_client runFBACommand universalFBAScriptCode );

my $usage  = "Command sequence: perl loadGenomes.pl username password genomeDirectory workspaceID \n";
my $username  = shift or die $usage;
my $password  = shift or die $usage;
my $inputDirectory  = shift or die $usage;
my $workspaceID  = shift or die $usage;

# Login to the KBase server
system("kbase-login", $username, "-p", $password);
  
# Read in the list of genomes in genomeDir
my @genomes;

opendir (DIR, $inputDirectory) or die $!;
while (my $file = readdir(DIR)) {
  # Ignore files beginning w/ a period
  next if ($file =~ m/^\./);
  # Remove file extension
  $file =~ s/\.fna//;
  push (@genomes, $file);
}
closedir(DIR);

# Counter and empty hash where contig objects will be stored
my $iter = 1;
my $numGenomes = @genomes;

foreach my $genome (@genomes) {
	print "Processing contig set ", $iter, " of ", $numGenomes, "\n";

	# Assign metadata
	my $object = {
		id => $genome."."."contigs",
		name => $genome,
		source_id => $genome.".fna",
		source => "Freshwater",
		type => "Organism",
		contigs => [],
		md5 => undef
		     };

	# Read in the FASTA file
	my $filename = $inputDirectory."/".$genome.".fna";
	open FILE, "<",$filename  or do {
		die "$0: open ".$filename.": $!";
	      };

	# Assign metadata to the contigs
	my $contig;
	my $sequence = "";
	my $description;
	my $length = 0;
	my $lengths = [];
	my $contigids = [];
	my $contigseq = {};
	my $gc = 0;
	my $numcontigs = 0;

	# Process the fasta header and sequence and assign metadata
	while (my $line = <FILE>) {
		chomp($line);
		if ($line =~ m/\>(.+)/) {
			if (defined($contig)) {
				$numcontigs++;
				push(@{$lengths},length($sequence));
				push(@{$contigids},$contig);
				$length += length($sequence);
				$contigseq->{$contig} = $sequence;
				push(@{$object->{contigs}},{
					id => $genome.".contig.".$numcontigs,
					"length" => length($sequence),
					md5 => Digest::MD5::md5_hex($sequence),
					sequence => $sequence,
					genetic_code => 11,
					name => $genome.".contig.".$numcontigs,
					complete => 1,
					description => $description
				});
				$sequence =~ s/[atAT]//g;
				$gc += length($sequence);
			}
			$sequence = "";
			$contig = $1;
			$description = $1;
			if($contig =~ /(.*)?\s(.+)/ ) {
				$contig = $1;
				$description = $2;
			}
		} else {
			$sequence .= $line;
		}
	      }

	# Assign more metadata
	if (defined($contig)) {
		$numcontigs++;
		push(@{$lengths},length($sequence));
		push(@{$contigids},$contig);
		$length += length($sequence);
		$contigseq->{$contig} = $sequence;
		push(@{$object->{contigs}},{
			id => $genome.".contig.".$numcontigs,
			"length" => length($sequence),
			md5 => Digest::MD5::md5_hex($sequence),
			sequence => $sequence,
			genetic_code => 11,
			name => $genome.".contig.".$numcontigs,
			complete => 1,
			description => $description
		});
		$sequence =~ s/[atAT]//g;
		$gc += length($sequence);
	}
	$gc = $gc/$length;
	close(FILE);

	# Create the contig object
	my $str = "";
	for (my $i=0; $i < @{$object->{contigs}}; $i++) {
		if (length($str) > 0) {
			$str .= ";";
		}
		$str .= $object->{contigs}->[$i]->{sequence};
	}
	$object->{md5} = Digest::MD5::md5_hex($str);

	# Upload the workspace
	save_workspace_object($username.":".$workspaceID."/".$object->{id},$object,"KBaseGenomes.ContigSet");
	
	$iter = $iter + 1;
};


