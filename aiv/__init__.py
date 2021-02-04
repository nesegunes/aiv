#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 18:18:50 2021

@author: tardis
"""
import sys
import pandas as pd
import myvariant

# Used to create a report in pdf format
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_JUSTIFY


# Get data from given database: 'civic', 'clinvar', 'cosmic', 'snpeff' or anywhere it can find
def _pull_data(dir_, database):
    # Create an empty list to store annotations
    variant_annotations = []
    evidence_items = []
    info = []
    
    # Get information about variant
    if 'civic' in dir_ and database == 'civic':
        gene_ = dir_[database]['entrez_name']
        protein_change_ = dir_[database]['name']
                            
    # Get variant annotation for identified variant
    if 'civic' in dir_ and 'description' in dir_[database]:
        variant_annotations.append(dir_[database]['description'])
    
    # Get evidence statements if known
    if 'civic' in dir_ and 'evidence_items' in dir_[database]:
        if isinstance(dir_[database]['evidence_items'], list):
            for d in dir_[database]['evidence_items']:
                evidence_items.append(d['description'])
 
    # If short summaries for the mutation not found in 'civic', store 'ann' values instead
    for key, value in dir_.items():
        if isinstance(value, dict) and 'ann' in value.keys():
            info.append((key, value['ann']))
            ann = value['ann']
            gene_ = value['ann']['genename' if isinstance(value['ann'], dict) else 0]
            if isinstance(gene_, dict): gene_ = gene_['genename']
            protein_change_ = value['ann']['effect' if isinstance(value['ann'], dict) else 0]
            if isinstance(protein_change_, dict): protein_change_ = protein_change_['transcript_biotype']
    
    if not len(variant_annotations):
        if isinstance(ann, dict):
            description = 'In database ' + info[0][0] + ' mutation with the gene ID ' + ann['genename'] + ' and Human Genome Variant Society nomenclature ' + ann['hgvs_c'] + ' is found to be ' + ann['effect'] + ' and has a putative impact of ' + ann['putative_impact'] + '.'
        elif isinstance(ann, list):
            description = 'In database ' + info[0][0] + ' mutation with the gene ID ' + ann[0]['genename'] + ' and Human Genome Variant Society nomenclature ' + ann[0]['hgvs_c'] + ' is found to be ' + ann[0]['effect'] + ' and has a putative impact of ' + ann[0]['putative_impact'] + '.'
            
        variant_annotations.append(description)

    return variant_annotations, gene_, protein_change_, info, evidence_items


def _add_variant_info(variant_annotations, annotated_variants, gene_, protein_change_, info, v, content, style_, evidence_items, assembly):
    # Add info about variant to the report: Gene Name, Protein Change and Coordinates
    content.append(Paragraph('Clinical Variant ' + str(annotated_variants), style_['Heading2']))
    content.append(Paragraph('Gene Name: ' + '\t'+ '\t'+ '\t' + str(gene_) + '\n', style_['BodyText']))
    content.append(Paragraph('Protein Change: ' if assembly == 'hg19' else 'Transcript Biotype: ' + '\t'+ '\t' + str(protein_change_) + '\n', style_['BodyText']))
    content.append(Paragraph('Coordinates: ' + '\t'+ '\t'+ '\t' + str(v) + '\n', style_['BodyText']))
    
    # Make a title for variant annotation section
    content.append(Paragraph('Variant Annotation ', style_['Heading3']))
    
    # Add annotations to the report if found
    if len(variant_annotations):
        for annot in variant_annotations:
            p = Paragraph(str(annot), style_['Justified'])
            content.append(p)
    elif len(info):
        for i in range(len(info)):
            content.append(Paragraph('In database ' + info[i][0] + ' mutation is found to be ' + info[i][1]['effect'] if isinstance(info[i][1], dict) else info[i][1][0]['effect'] + '\n', style_['Justified']))
    else:
        p = Paragraph('Variant annotation not found...' + '\n', style_['Justified'])
        content.append(p)
        
    # Put a 'evidence statements' title
    content.append(Paragraph('Evidence Statements ', style_['Heading3']))
    
    # Add evidence statements to the report if found
    if len(evidence_items):
        for i, evidence in enumerate(evidence_items):
            content.append(Paragraph('Evidence statement ' + str(i + 1), style_['Heading4']))
            content.append(Paragraph(str(evidence), style_['Justified']))
    else:
        p = Paragraph('Evidence statements not found...' + '\n', style_['Justified'])
        content.append(p)


def _add_additional_info(total_variants, annotated_variants, content, style_):
    # Add additional info: processed variants and annotated variants
    content.append(Paragraph('Additional information', style_['Heading3']))
                
    # Give the number of processed variants
    content.append(Paragraph('Total Number of Variants Processed: ' + str(total_variants) + '\n', style_['BodyText']))

    # Give the number of annotated variants
    content.append(Paragraph('The Number of Clinical Annotations: ' + str(annotated_variants) + '\n', style_['BodyText']))


def getvariant(chromosome, start, ref, var):
    # Create myvariant info instance
    mv = myvariant.MyVariantInfo()

    # Get variant information for: chromosome, int(start), ref, var
    v = myvariant.format_hgvs(chromosome, int(start), ref, var)
    dir_ = mv.getvariant(v)
    
    # Return variant information found in all databases as a directory
    return dir_


def annotate_mutations(file, assembly = 'hg19'):
    # Open variant file with pandas
    identified_variants = pd.read_csv(file, sep='\t')
    
    # Give a name to the output file: 'test_filename' + '_AIM_report.pdf'
    doc_name = file.split('.')[0] + '_AIV_Report.pdf'
    
    # Create a sample document and sample style sheet
    report = SimpleDocTemplate(doc_name)
    style_ = getSampleStyleSheet()
    
    # Add a paragraph style to justify text
    style_.add(ParagraphStyle('Justified', alignment=TA_JUSTIFY))
    
    # Create a list to store all the content which will be written into the report
    content = []

    # Put main title of the annotation report
    content.append(Paragraph("Annotation of Identified Variants", style_['Heading1']))
    
    # Add given input file name
    content.append(Paragraph('File Name: ' + '\t' + '\t' + '\t' + str(file) + '\n', style_['BodyText']))

    # Get a myvariant info instance
    mv = myvariant.MyVariantInfo()

    # Initiliaze a counter for variants
    total_variants = 0
    annotated_variants = 0

    # Loop through identified variants and get annotations
    for i, row in identified_variants.iterrows():
        # Store the total number of variants given in the input file
        total_variants +=1
        
        # Get chromosome, start, reference and variant columns
        chrom_ = row['Chromosome']
        start_ = row['Start']
        ref_ = row['Ref']
        var_ = row['Var']
        
        # Get variant information
        v = myvariant.format_hgvs(chrom_, int(start_), ref_, var_)
        dir_ = mv.getvariant(v, assembly=assembly)

        # Get data from 'civic'
        if dir_:
            # Create an empty list to store annotations
            variant_annotations, gene_, protein_change_, info, evidence_items = _pull_data(dir_, 'civic')
        
            # Increase the number of clinically annotated variants by 1 (one).
            annotated_variants +=1
            
            # Add content to the report: general info, annotations & evidence statements
            _add_variant_info(variant_annotations, annotated_variants, gene_, protein_change_, info, v, content, style_, evidence_items, assembly)
        
        
    # Add processing information: total processed variants and number of annotated variants
    _add_additional_info(total_variants, annotated_variants, content, style_)

    # Save report in the same directory
    report.build(content)
