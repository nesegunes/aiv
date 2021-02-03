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


# Annotate variants
aiv.annotate_mutations('variant_calls.tsv')
```
