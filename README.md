[![PyPI](https://img.shields.io/pypi/v/aiv)](https://pypi.org/project/aiv/)  [![GitHub](https://img.shields.io/github/license/nesegunes/aiv)](https://pypi.org/project/aiv/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aiv)](https://pypi.org/project/aiv/)
[![PyPI - Format](https://img.shields.io/pypi/format/aiv)](https://pypi.org/project/aiv/)


## AIV: Annotation of Identified Variants

Annotation of Identified Variants to Create Reports for Clinicians to Assist Therapeutic Decisions

## Prerequisites

It requires three main modules: pandas, myvariant and reportlab

```
pip install pandas
pip install myvariant
pip install reportlab
```

## Installation

```
pip install aiv
```

## Upgrade

```
pip install aiv --upgrade
```

## Usage

```javascript
import aiv

# Get variant info 
aiv.getvariant('chr1', 69635, 'G', 'C')


# Annotate variants, reference genome: hg38
aiv.annotate_mutations('variant_calls.tsv', assembly='hg38')

# Annotate variants, reference genome: hg19
aiv.annotate_mutations('bwa_mutect2_nb09_50_lines.txt', assembly='hg19')
```
## Tests

You can test your installation with sample variant call files. Input test files can be found at: 

```
./tests/test_annotate_variants.tsv
./tests/bwa_mutect2_nb09_50_lines.txt
./tests/my_data.txt
```
## Input File Format

![Input file](https://github.com/nesegunes/aiv/blob/master/images/input.png?raw=true)


## Report Preview

![Output file](https://github.com/nesegunes/aiv/blob/master/output/test_annotate_variants_AIV_Report-01.png?raw=true)

## Future Work

- Performance can be determined by calculating the running time for a given input file with 6000+ mutations.
