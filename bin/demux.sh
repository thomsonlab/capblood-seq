SAMPLE=AM1
NUM_CORES=31

mkdir -p barcodes
wget https://caltech.box.com/shared/static/evjhzh50rk6zk2jtjpfg3myddxxmnqn5.txt -O barcodes/3M-february-2018.txt
aws s3 sync s3://thomsonlab/capblood-seq-demux/$SAMPLE/ aligned/
wget https://cf.10xgenomics.com/supp/cell-exp/refdata-cellranger-hg19-1.2.0.tar.gz
tar -xzf refdata-cellranger-hg19-1.2.0.tar.gz
rm refdata-cellranger-hg19-1.2.0.tar.gz
sudo yum update -y
sudo yum install -y git
sudo yum groupinstall -y "Development Tools"
sudo yum install -y bzip2-devel
sudo yum install -y xz-devel
sudo yum install -y libcurl-devel
sudo yum install -y openssl-devel
sudo yum install -y ncurses-devel
sudo yum install -y python3-devel
sudo yum install -y cmake
sudo pip3 install --upgrade pip
sudo ln -s /usr/local/bin/pip3 /usr/bin/pip3

cd barcodes
python3 ../split_barcodes.py $NUM_CORES

cd ~
git clone https://github.com/samtools/htslib.git
cd htslib
git checkout tags/1.10.2
autoheader
autoconf
./configure
make
sudo make install

cd ~
git clone https://github.com/samtools/samtools.git
cd samtools
git checkout tags/1.10
autoheader
autoconf -Wno-syntax
./configure
make
sudo make install
cd ~
samtools faidx refdata-cellranger-hg19-1.2.0/fasta/genome.fa -o refdata-cellranger-hg19-1.2.0/fasta/genome.fai

cd ~
git clone https://github.com/ekg/freebayes.git
cd freebayes
git checkout tags/v1.3.2
git submodule update --init --recursive
make
sudo make install
cd vcflib
make
sudo make install
sudo ln -s ~/freebayes/vcflib/bin/vcfuniq /usr/bin/vcfuniq

cd ~
wget https://ftp.gnu.org/gnu/parallel/parallel-20200822.tar.bz2
bzip2 -d parallel-20200822.tar.bz2
tar -xf parallel-20200822.tar
rm parallel-20200822.tar
cd parallel-20200822
autoheader
autoconf
./configure
make
sudo make install

cd ~
git clone https://github.com/statgen/popscle.git
cd popscle
git checkout fad43920be74461b8236c144b4a0b69f2e8812c9
mkdir build
cd build
cmake ..
make

cd ~/freebayes/scripts
python3 fasta_generate_regions.py ../../refdata-cellranger-hg19-1.2.0/fasta/genome.fa.fai 100000 > ../../refdata-cellranger-hg19-1.2.0/fasta/regions.fai

cd ~
if [ ! -f aligned/combined.vcf ]; then
	./freebayes-parallel ../../refdata-cellranger-hg19-1.2.0/fasta/regions.fai $NUM_CORES -f ../../refdata-cellranger-hg19-1.2.0/fasta/genome.fa ../../aligned/possorted_genome_bam.bam > ../../aligned/combined.vcf
	aws s3 cp ../../aligned/combined.vcf s3://thomsonlab/capblood-seq-demux/$SAMPLE/
fi

cd ~
mkdir -p demux

for (( core=0; core <= $NUM_CORES - 1; core++ ))
do
	printf -v barcode_file_name "3M-february-2018-%03d.txt" $core
	printf -v output_prefix "pileup-%03d" $core
	./popscle/bin/popscle dsc-pileup --sam aligned/possorted_genome_bam.bam --vcf aligned/combined.vcf --out demux/$output_prefix --group-list barcodes/$barcode_file_name &
	pids[${core}]=$!
done

for pid in ${pids[*]}; do
	wait $pid
done

cd ~
aws s3 sync demux s3://thomsonlab/capblood-seq-demux/$SAMPLE/demux/
