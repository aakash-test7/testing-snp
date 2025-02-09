import streamlit as st

def glossary_page():
    st.title("Glossary")
    st.write("**Key Terms and Definitions**")
    glossary_entries = {
        'GS - Germinating Seedling': '- The early stage of seedling development where the seed begins to sprout and grow.',
        'S - Shoot': '- The above-ground part of the plant, including stems, leaves, and flowers.',
        'ML - Mature Leaf': '- A fully developed leaf, which has completed its growth.',
        'YL - Young Leaf': '- A developing leaf that has not yet reached full maturity.',
        'Brac - Bracteole': '- A small leaf-like structure at the base of a flower or inflorescence.',
        'R - Root': '- The part of the plant that anchors it in the soil and absorbs water and nutrients.',
        'Rtip - Root Tip': '- The growing tip of the root, where new cells are produced.',
        'RH - Root Hair': '- Tiny hair-like structures on the root that increase surface area for water absorption.',
        'Nod - Nodule': '- A swollen structure on plant roots, often containing nitrogen-fixing bacteria.',
        'SAM - Shoot Apical Meristem': '- The tissue at the tip of the shoot where growth and development occur.',
        'FB1-FB4 - Stages of Flower Bud Development': '- Sequential stages representing the development of flower buds.',
        'FL1-FL5 - Stages of Flower Development': '- Sequential stages representing the development of flowers.',
        'Cal - Calyx': '- The outermost whorl of a flower, usually consisting of sepals.',
        'Cor - Corolla': '- The petals of a flower, collectively forming the corolla.',
        'And - Androecium': '- The male reproductive part of the flower, consisting of stamens.',
        'Gyn - Gynoecium': '- The female reproductive part of the flower, consisting of pistils.',
        'Pedi - Pedicel': '- The stalk that supports a flower or an inflorescence.',
        'Emb - Embryo': '- The early stage of development of a plant from the fertilized egg cell.',
        'Endo - Endosperm': '- The tissue that provides nourishment to the developing embryo in seeds.',
        'SdCt - Seed Coat': '- The outer protective layer of a seed.',
        'PodSh - Podshell': '- The outer casing that surrounds the seeds within a pod.',
        '5DAP - Seed 5 Days After Pollination': '- The developmental stage of seed five days after pollination.',
        '10DAP - Seed 10 Days After Pollination': '- The developmental stage of seed ten days after pollination.',
        '20DAP - Seed 20 Days After Pollination': '- The developmental stage of seed twenty days after pollination.',
        '30DAP - Seed 30 Days After Pollination': '- The developmental stage of seed thirty days after pollination.',
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

    con=st.container(border=True)
    search_term = con.text_input("Search Glossary", "")
    
    filtered_entries = {term: definition for term, definition in glossary_entries.items() if search_term.lower() in term.lower() or search_term.lower() in definition.lower()}
    con=st.container(border=True)
    with con:
        for term, definition in filtered_entries.items():
            with st.expander(term):
                st.write(definition)

if __name__ == "__page__":
    glossary_page()
