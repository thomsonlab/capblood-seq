# Capillary Blood Sequencing (capblood-seq)

This is a companion repository and package for the capillary blood single-cell
sequencing project from Caltech.

## Installing
```
pip install capblood-seq
```

## Prerequisites


### Preprocessing
- Cell Ranger v3.0.0 (https://support.10xgenomics.com/single-cell-gene-expression/software/downloads/3.0/)

### Demultiplexing
- 23andme2vcf (https://github.com/arrogantrobot/23andme2vcf/,
commit @6ba76f6dc753919553236dedebdeab99c318fd1f)
- demuxlet (https://github.com/statgen/demuxlet, 
commit @85dca0a4d648d18e6b240a2298672394fe10c6e6)
- htslib (https://github.com/samtools/htslib,
commit @5f5c1a557eb9d65f8b7854b6ca4c898713e86c04)
- vcftools (https://github.com/vcftools/vcftools.git,
commit @15db94b968d963e1b5188b8918b6659b25798ec1)
- tabix 1.7-2

## Usage

This package revolves around the usage of the capblood_seq DATASET object, which
you can quickly access with:
```
import capblood_seq

dataset = capblood_seq.load_dataset()
```

This will download all relevant data for the paper (both raw and processed)
and save it to a local ```data``` directory. You can then proceed with any
of the functionality in the ```examples``` Jupyter notebooks.

There are two intended usage modes for the package:
### 1. Download raw 10X Cell Ranger data and perform preprocessing yourself

To do this, start with the Preprocessing section below. The raw feature
BC matrices will be automatically downloaded, and you can initialize a dataset
and process it, which will overwrite any downloaded already processed data.

### 2. Download processed data and jump into generating figures

To do this, skip the preprocessing and jump straight into running the figure
scripts. These scripts will download the already processed data for you.

## Demultiplexing

To generate the subject cell labels, we used 23andMe genome files to demultiplex
the cells in each sample.

First, we convert the 23andMe files to VCF using 23andme2vcf. We created the VCF
against the manually curated 23andMe references, using the v4 reference
```
perl 23andme2vcf.pl S1_v4_Full.txt S1.vcf 4
```

Next, we compress and index the VCFs:
```
bgzip S1.vcf; tabix -p vcf S1.vcf.gz
```

And we use vcftools' vcf-merge to merge them into a single VCF file:
(we provide a custom column headers file, headers.txt, in ```data\genomes```
to give proper subject column names)
```
vcf-merge S1.vcf.gz S2.vcf.gz S3.vcf.gz S4.vcf.gz -H "headers.txt" > capblood_seq.vcf
```

Next we remove 'chr' from the beginning of each line:
```
sed -i 's/^chr//' capblood_seq.vcf
```

And then sort the entries lexicographically: (thank you https://www.biostars.org/p/133487/#133489)

```
grep '^#' capblood_seq.vcf > capblood_seq_sorted.vcf && grep -v '^#' capblood_seq.vcf | LC_ALL=C sort -t $'\t' -k1,1 -k2,2n >> capblood_seq_sorted.vcf
```

And finally compress the new combined VCF:
```
bgzip capblood_seq_sorted.vcf
```

We can then use this to generate a cell barcode label file using demuxlet
for each sample. This requires the raw possorted_genome_bam.bam file from
running the 10X Cell Ranger pipeline

```
demuxlet --sam possorted_genome_bam.bam --tag-group CB --tag-UMI UB --vcf capblood_seq_sorted.vcf.gz --out demuxed --field GT
```

## Preprocessing

After receiving the output from 10X Cell Ranger, we convert the data into
SCRAP workspaces for downstream manipulation. An example of this is in
 ```Initialize Datasets.ipynb```.
 
 Then, we preprocess the data through several steps, an example of which is in
 ```Preprocessing.ipynb```
 1. Filter out any remaining debris, empty droplets, and red blood cells. This
 is done by a function in scrapi, but a step by step example is in 
 ```Debris Removal.ipynb```
 2. Remove low count genes (any genes that have a maximum count < 3)
 3. Convert gene counts into transcripts per cell
 4. (For visualization only) Transform the normalized gene counts via PCA, and
 then t-SNE
 
 ## Cell Subject Assignment
 
 After a workspace is created and filtered for debris, and demuxlet has
 assigned cells to subjects, we add it to our workspace label files. An example
 of this is in ```Assign Cells to Subject IDs.ipynb```

## Figures
The figures in the paper were generated by the Jupyter notebook examples in the
```examples/``` directory as below:

- Figure 1.c: ```Combined t-SNE.ipynb```
- Figure 1.d: ```Cell Type Distribution Suburst.ipynb```
- Figure 1.e: ```Cell Type Diurnal Count Box Plot.ipynb```
- Figure 2.a: ```Diurnal Gene Detection.ipynb```
- Figure 2.b: ```Gene AM vs PM Overlapping Histogram.ipynb```
- Figure 2.c: ```Gene Diurnality Box Plots.ipynb```
- Figure 2.d: ```Gene Diurnality Box Plots.ipynb```
- Figure 3.a: ```Individuality and Cell Type Specificity.ipynb```
- Figure 3.b: ```Diurnal Individual Pathway Enrichment.ipynb```
- Figure 3.c: ```Gene Expression by Subject Over Time.ipynb```
- Figure 3.c: ```Gene Subject vs All Overlapping Histogram.ipynb```
- Extended Figure 1: ```Cell Type Marker Gene Violin Plots.ipynb```
- Extended Figure 2: ```Gene Subject vs Others Box Plot.ipynb```
