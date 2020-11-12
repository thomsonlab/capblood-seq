# The location of the alignment files output by 10X Cell Ranger (specifically the possorted_genome_bam.bam and possorted_bam_bam.bam.bai files). Within this folder there should be a subfolder for each sample
AWS_S3_ALIGNMENT_PATH=s3://thomsonlab/capblood-seq-demux

aws s3 sync $AWS_S3_ALIGNMENT_PATH/merged/ aligned/
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

cd ~
./popscle/bin/popscle freemuxlet --plp aligned/pileup --nsample 4 --out aligned/freemuxlet

aws s3 sync aligned/ $AWS_S3_ALIGNMENT_PATH/merged/
