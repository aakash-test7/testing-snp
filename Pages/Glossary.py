import streamlit as st

def glossary_page():
    st.title("Glossary")
    st.write("**Key Terms and Definitions**")
    glossary_entries = {
        'GO - Gene Ontology': '- a framework for the model of biology that describes gene functions in a species-independent manner.',
        'KEGG - Kyoto Encyclopedia of Genes and Genomes': '- a database resource for understanding high-level functions and utilities of biological systems.',
        'FPKM - Fragments Per Kilobase of transcript per Million mapped reads': '- a normalized method for counting RNA-seq reads.',
        'miRNA - MicroRNA': '- small non-coding RNA molecules that regulate gene expression by binding to complementary sequences on target mRNA.',
        'lncRNA - Long Non-Coding RNA': '- a type of RNA molecule that is greater than 200 nucleotides in length but does not encode proteins.',
        'ST - Seed Tissue': '- the tissue in seeds that supports the development of the embryo and storage of nutrients.',
        'FDS - Flower Development Stages': '- the various phases of growth and development that a flower undergoes from bud to bloom.',
        'FP - Flower Parts': '- the various components that make up a flower, including petals, sepals, stamens, and carpels.',
        'GT - Green Tissues': ' - plant tissues that are photosynthetic, primarily found in leaves and stems.',
        'RT - Root Tissues': '- the tissues found in the root system of a plant, involved in nutrient absorption and anchorage.',
        'TF - Transcription Factor': '- a protein that controls the rate of transcription of genetic information from DNA to messenger RNA.',
        'Non-TF - Non-Transcription Factors': '- proteins or molecules that do not directly bind to DNA to initiate or regulate transcription, but still influence gene expression through other mechanisms.',
        'WGCNA - Weighted Gene Co-expression Network Analysis': '- a method for finding clusters (modules) of highly correlated genes and studying their relationships to clinical traits.',
        'PPI - Protein-Protein Interaction': '- physical contacts between two or more proteins that occur in a living organism and are essential for various biological functions, including signal transduction and gene regulation.',
        'SNP CALLING - Single Nucleotide Polymorphism': 'The process of identifying single nucleotide polymorphisms (SNPs) in a genome from sequencing data. SNPs are variations at a single position in the DNA sequence, and SNP calling is crucial for genetic studies and disease association analyses.',
        'PEPTIDE SEQUENCE': 'A sequence of amino acids that make up a peptide, which is a short chain of amino acids linked by peptide bonds.',
        'CDS SEQUENCE - Coding Sequence': '- the portion of a gene\'s DNA or RNA that codes for a protein.',
        'TRANSCRIPT SEQUENCE': 'The RNA sequence transcribed from a gene, which may be translated into a protein or may function as non-coding RNA.',
        'GENOMIC SEQUENCE': 'The complete sequence of nucleotides (DNA or RNA) that make up the entire genome of an organism.'
    }

    for term, definition in glossary_entries.items():
        with st.expander(term):
            st.write(definition)

if __name__ == "__page__":
    glossary_page()