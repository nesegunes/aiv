#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 18:18:50 2021

@author: tardis
"""
import sys
import pandas as pd
import myvariant

from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_JUSTIFY


# Get data from given database: 'civic', 'clinvar', 'cosmic', 'snpeff' or anywhere it can find
def _pull_data(dir_, database):
    # Create an empty list to store annotations
    variant_annotations = []
    info = None
    
    # Get information about variant
    if database == 'civic':
        gene_ = dir_[database]['entrez_name']
        protein_change_ = dir_[database]['name']
    else:
        info = dir_[database]
                            
    # Get variant annotation for identified variant
    if 'description' in dir_[database]:
        variant_annotations.append(dir_[database]['description'])
        
    if 'evidence_items' in dir_[database]:
        evidence_items = []
        if isinstance(dir_[database]['evidence_items'], list):
            for d in dir_[database]['evidence_items']:
                evidence_items.append(d['description'])
    
    
    return variant_annotations, gene_, protein_change_, info, evidence_items


def _add_variant_info(variant_annotations, annotated_variants, gene_, protein_change_, info, v, content, style_, evidence_items):
    # Add info about variant to the report
    title = Paragraph('Clinical Variant ' + str(annotated_variants), style_['Heading2'])
    content.append(title)
    
    p = Paragraph('Gene Name: ' + '\t'+ '\t'+ '\t' + str(gene_) + '\n', style_['BodyText'])
    content.append(p)
    
    p = Paragraph('Protein Change: ' + '\t'+ '\t' + str(protein_change_) + '\n', style_['BodyText'])
    content.append(p)
    
    p = Paragraph('Coordinates: ' + '\t'+ '\t'+ '\t' + str(v) + '\n', style_['BodyText'])
    content.append(p)
    
    title = Paragraph('Variant Annotation ', style_['Heading3'])
    content.append(title)
    
    # Add annotations to the report
    if len(variant_annotations):
        for annot in variant_annotations:
            p = Paragraph(str(annot), style_['Justified'])
            content.append(p)
    elif info:
        p = Paragraph(str(info) + '\n', style_['Justified'])
        content.append(p)
    else:
        p = Paragraph('Variant annotation not found...' + '\n', style_['Justified'])
        content.append(p)
        
    title = Paragraph('Evidence Statements ', style_['Heading3'])
    content.append(title)
    
    if len(evidence_items):
        for i, evidence in enumerate(evidence_items):
            content.append(Paragraph('Evidence statement ' + str(i + 1), style_['Heading4']))
            content.append(Paragraph(str(evidence), style_['Justified']))
    else:
        p = Paragraph('Evidence statements not found...' + '\n', style_['Justified'])
        content.append(p)


def _add_additional_info(total_variants, annotated_variants, content, style_):
    title = Paragraph('Additional information', style_['Heading3'])
    content.append(title)
                
    # Give additional information
    p = Paragraph('Total Number of Variants Processed: ' + str(total_variants) + '\n', style_['BodyText'])
    content.append(p)

    p = Paragraph('The Number of Clinical Annotations: ' + str(annotated_variants) + '\n', style_['BodyText'])
    content.append(p)


def getvariant(chromosome, start, ref, var):
    mv = myvariant.MyVariantInfo()

    # Get variant information using 'myvariant' module
    v = myvariant.format_hgvs(chromosome, int(start), ref, var)
    dir_ = mv.getvariant(v)
    
    return dir_


def annotate_mutations(file):
    # Open variant file with pandas
    identified_variants = pd.read_csv(file, sep='\t')

    doc_name = file.split('.')[0] + '_AIM_Report.pdf'
    report = SimpleDocTemplate(doc_name)
    style_ = getSampleStyleSheet()
    style_.add(ParagraphStyle('Justified', alignment=TA_JUSTIFY))
    content = []

    title = Paragraph("Annotation of Identified Variants", style_['Heading1'])
    content.append(title)

    p = Paragraph('File Name: ' + '\t' + '\t' + '\t' + str(file) + '\n', style_['BodyText'])
    content.append(p)

    # Get a myvariant info instance
    mv = myvariant.MyVariantInfo()

    # Initiliaze a counter for variants
    total_variants = 0
    annotated_variants = 0

    # Loop through identified variants and get annotations
    for i, row in identified_variants.iterrows():
        total_variants +=1
        
        # Get chromosome, start, reference and variant columns
        chrom_ = row['Chromosome']
        start_ = row['Start']
        ref_ = row['Ref']
        var_ = row['Var']
        
        # Get variant information using 'myvariant' module
        v = myvariant.format_hgvs(chrom_, int(start_), ref_, var_)
        dir_ = mv.getvariant(v)

        # Get data
        if dir_ and 'civic' in dir_:
            # Create an empty list to store annotations
            variant_annotations, gene_, protein_change_, info, evidence_items = _pull_data(dir_, 'civic')
        
            # Increase the number of clinically annotated variants by 1 (one).
            annotated_variants +=1

            _add_variant_info(variant_annotations, annotated_variants, gene_, protein_change_, info, v, content, style_, evidence_items)
        
        

    _add_additional_info(total_variants, annotated_variants, content, style_)

    # Save report
    report.build(content)
