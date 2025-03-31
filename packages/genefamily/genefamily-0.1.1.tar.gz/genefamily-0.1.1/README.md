GeneFamily

## Installation

```bash
pip install genefamily
```

## Dependencies

### Install miniforge

Install [miniforge](https://github.com/conda-forge/miniforge) according to the instructions on the website.

### Install dependencies

```bash
mamba install conda-forge::biopython=1.85
mamba install bioconda::gffread=0.12.7
mamba install bioconda::seqkit=2.10.0

```

## Usage

### example data

The demo data were downloaded from [RiceSuperPIRdb](http://www.ricesuperpir.com/web/download) from the paper, [A super pan-genomic landscape of rice](https://www.nature.com/articles/s41422-022-00685-z).

```bash
wget http://www.ricesuperpir.com/uploads/common/gene_annotation/NIP-T2T.gff3.gz
wget http://www.ricesuperpir.com/uploads/common/genome_sequence/NIP-T2T.fa.gz

gunzip NIP-T2T.gff3.gz
gunzip NIP-T2T.fa.gz

mv NIP-T2T.gff3 Nipponbare.gff3
mv NIP-T2T.fa Nipponbare.fa
```

### get the longest transcript for each gene

```bash
python3 src/genefamily/parse_longest_mrna.py -g example/Nipponbare.fa -f example/Nipponbare.gff3 -o example/longest.pep.fa
```

```bash
################################################################
Total genes: 57359
Total transcripts: 67818
Genes with multiple transcripts: 6510
################################################################
Successfully extracted 57359 longest transcripts
Longest transcript protein sequences saved to: example/longest.pep.fa
Gene and transcript information saved to: example/Nipponbare.gene.info.txt
```