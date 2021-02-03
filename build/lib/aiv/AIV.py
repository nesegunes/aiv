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
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

def annotate_mutations(file):
    # Open variant file with pandas
    identified_variants = pd.read_csv(file, sep='\t')

    doc_name = 'aim_report.pdf'
    report = SimpleDocTemplate(doc_name)
    style_ = getSampleStyleSheet()
    content = []

    title = Paragraph("Annotation of Identified Variants", style_['Heading1'])
    content.append(title)

    p = Paragraph('Variant Call File Name: ' + '\t' + '\t' + '\t' + str(file) + '\n', style_['BodyText'])
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
            variant_annotations = []
            
            # Increase the number of clinically annotated variants by 1 (one).
            annotated_variants +=1

            # Get information about variant
            gene_ = dir_['civic']['entrez_name']
            protein_change_ = dir_['civic']['name']
                                    
            # Get variant annotation for identified variant
            if 'description' in dir_['civic']:
                variant_annotations.append(dir_['civic']['description'])
            
            # Add info about variant to the report
            title = Paragraph('Clinical Variant: ' + str(annotated_variants), style_['Heading2'])
            content.append(title)
            
            p = Paragraph('Gene Name: ' + '\t'+ '\t'+ '\t' + str(gene_) + '\n', style_['BodyText'])
            content.append(p)
            
            p = Paragraph('Protein Change: ' + '\t'+ '\t' + str(protein_change_) + '\n', style_['BodyText'])
            content.append(p)
            
            p = Paragraph('Coordinates: ' + '\t'+ '\t'+ '\t' + str(v) + '\n', style_['BodyText'])
            content.append(p)
            
            title = Paragraph('Variant Annotation: ', style_['Heading3'])
            content.append(title)
            
            # Add annotations to the report
            if len(variant_annotations):
                for annot in variant_annotations:
                    p = Paragraph(str(annot), style_['BodyText'])
                    content.append(p)
            else:
                p = Paragraph('Not found...' + '\n', style_['BodyText'])
                content.append(p)
            
    title = Paragraph('Additional information', style_['Heading3'])
    content.append(title)
                
    # Give additional information
    p = Paragraph('Total Number of Variants Processed: ' + str(total_variants) + '\n', style_['BodyText'])
    content.append(p)

    p = Paragraph('The Number of Clinical Annotations: ' + str(annotated_variants) + '\n', style_['BodyText'])
    content.append(p)

    # Save report
    report.build(content)
