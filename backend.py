import pandas as pd
import requests
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import base64
import time
import streamlit as st
from streamlit.components.v1 import html as st_components_html
import os
from google.cloud import storage
import io
import json
from google.oauth2 import service_account
from google.cloud import storage
from datetime import timedelta
from google.oauth2 import service_account

secrets = st.secrets["gcp_service_account"]
credentials = service_account.Credentials.from_service_account_info(secrets)

def generate_signed_url(blob_name):
    """Generates a signed URL to access a file in GCS."""
    try:
        bucket_name = "chickpea-transcriptome"  # Replace with your bucket name
        client = storage.Client(credentials=credentials)
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        if not blob.exists():
            print(f"File {blob_name} does not exist in bucket {bucket_name}")  # Debugging
            return None
        url = blob.generate_signed_url(expiration=timedelta(hours=1), method='GET')
        print(f"Generated signed URL for {blob_name}: {url}")  # Debugging
        return url
    except Exception as e:
        print(f"Error generating signed URL for {blob_name}: {e}")  # Debugging
        return None

# Initialize the Google Cloud Storage client
client = storage.Client(credentials=credentials)

bucket_name = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET", "chickpea-transcriptome")

def read_excel_from_gcs(bucket_name, blob_name, header=0):
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    data = blob.download_as_bytes()
    return pd.read_excel(io.BytesIO(data), header=header)

df = read_excel_from_gcs(bucket_name, "Data/FPKM_Matrix(Ca).xlsx")
miRNA_df = read_excel_from_gcs(bucket_name, "Data/8.xlsx")
protein_df = read_excel_from_gcs(bucket_name, "Data/9.xlsx")
combined_data = read_excel_from_gcs(bucket_name, "Data/7.xlsx")
GO_df = read_excel_from_gcs(bucket_name, "Data/10.xlsx")
cello_df = read_excel_from_gcs(bucket_name, "Data/13.xlsx")
tsi_df=read_excel_from_gcs(bucket_name, "Data/12.xlsx")

def normalize_data(data):
    return data.applymap(lambda x: np.log2(x) if x > 0 else 0)

def format_sequence(seq):
    if isinstance(seq, float) and np.isnan(seq):
        return ''
    
    return '\n'.join('\t\t ' + ' '.join([seq[i:i+6] for i in range(j, min(j + 90, len(seq)), 6)]) for j in range(0, len(seq), 90))


def get_string_network_link(protein_transcript):

    api_url = "https://string-db.org/api/tsv/get_link?"

    params = {
        'identifiers': protein_transcript,
        'species': 3827,
        'format': 'json'
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        return response.text.strip()
    else:
        return f"Error: {response.status_code}"
def filter_orthologs(tid):
    bucket = client.get_bucket(bucket_name)
    blob_name = "Data/14.txt"
    blob = bucket.blob(blob_name)
    
    filtered_data = set()

    with blob.open("r") as infile:
        for line in infile:
            if tid in line:
                columns = line.strip().split()
                species_a, species_b = columns[0], columns[1]
                species_pair = tuple(sorted([species_a, species_b]))
                filtered_data.add((species_pair, columns[2]))

    filtered_data_list = [(pair[0][0], pair[0][1], pair[1]) for pair in filtered_data]
    ortho_df = pd.DataFrame(filtered_data_list, columns=["Species A", "Species B", "Score"])

    return ortho_df

def filter_paralogs(tid):
    bucket = client.get_bucket(bucket_name)
    blob_name = "Data/15.txt"
    blob = bucket.blob(blob_name)
    filtered_data = set()

    with blob.open("r") as infile:
        for line in infile:
            if tid in line:
                columns = line.strip().split()
                species_a, species_b = columns[0], columns[1]
                species_pair = tuple(sorted([species_a, species_b]))
                filtered_data.add((species_pair, columns[2]))

    filtered_data_list = [(pair[0][0], pair[0][1], pair[1]) for pair in filtered_data]
    para_df = pd.DataFrame(filtered_data_list, columns=["Species A", "Species B", "Score"])

    return para_df

def web_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--verbose")
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920, 1200")
    options.add_argument('--disable-dev-shm-usage')
    #driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=options)
    return driver

def automate_Cultivated_task(tid):
    driver = web_driver()
    driver.get("https://cegresources.icrisat.org/cicerseq/?page_id=3605")
    time.sleep(3)

    gene_id_dropdown = Select(driver.find_element(By.NAME, "select_crop"))
    gene_id_dropdown.select_by_value("cultivars")

    radio_button = driver.find_element(By.ID, "gene_snp")
    radio_button.click()

    gene_id_dropdown = Select(driver.find_element(By.NAME, "key1"))
    gene_id_dropdown.select_by_value("GeneID")

    intergenic_dropdown = Select(driver.find_element(By.NAME, "key4"))
    intergenic_dropdown.select_by_value("intergenic")

    input_field = driver.find_element(By.ID, "tmp1")
    input_field.clear()
    input_field.send_keys(tid) #Ca_00004

    search_button = driver.find_element(By.NAME, "submit")
    search_button.click()

    time.sleep(5)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    driver.quit()

    return page_source

def automate_Wild_task(tid):
    driver = web_driver()
    driver.get("https://cegresources.icrisat.org/cicerseq/?page_id=3605")
    time.sleep(3)

    gene_id_dropdown = Select(driver.find_element(By.NAME, "select_crop"))
    gene_id_dropdown.select_by_value("wild")

    radio_button = driver.find_element(By.ID, "wgene_snp")
    radio_button.click()

    gene_id_dropdown = Select(driver.find_element(By.NAME, "key2"))
    gene_id_dropdown.select_by_value("GeneID")

    intergenic_dropdown = Select(driver.find_element(By.NAME, "key4"))
    intergenic_dropdown.select_by_value("intergenic")

    input_field = driver.find_element(By.ID, "tmp3")
    input_field.clear()
    input_field.send_keys(tid) #Ca_00004

    search_button = driver.find_element(By.NAME, "submitw")
    search_button.click()

    time.sleep(5)

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')
    driver.quit()

    return page_source

def transcriptid_info(tid):
    if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
        matching_row = df[df['Transcript id'] == tid]

        if not matching_row.empty:
            st.subheader("Sequence data")
            cds_code = format_sequence(matching_row['Cds Sequence'].values[0])
            peptide_code = format_sequence(matching_row['Peptide Sequence'].values[0])
            transcript_code = format_sequence(matching_row['Transcript Sequence'].values[0])
            gene_code = format_sequence(matching_row['Genomic Sequence'].values[0])
            promote_code = format_sequence(matching_row['Promoter Sequence'].values[0])

            # Display as code block with copy functionality
            with st.expander("Genomic Sequence"):
                st.code(gene_code, language="text")
            with st.expander("Transcript Sequence"):
                st.code(transcript_code, language="text")
            with st.expander("CDS Sequence"):
                st.code(cds_code, language="text")
            with st.expander("Peptide Sequence"):
                st.code(peptide_code, language="text")
            with st.expander("Promoter Sequence"):
                st.code(promote_code, language="text")

            header = f">{tid}|{tid}"
            promote_file = f"{header}\n{promote_code}\n"
            b64 = base64.b64encode(promote_file.encode()).decode()  # Convert to base64
            href = f'<a href="data:text/plain;base64,{b64}" download="{tid}_promoter_sequence.txt">Download Promoter Sequence as .txt</a>'
            st.markdown(href, unsafe_allow_html=True)
            #st.download_button( label="Download Promoter Sequence as .txt", data=promote_file, file_name=f"{tid}_promoter_sequence.txt", mime="text/plain" )
            st.write("Paste the promoter sequence on the following link to get promoter region analysis!")
            st.write("https://bioinformatics.psb.ugent.be/webtools/plantcare/html/search_CARE_onCluster.html\n")

            st.subheader("Protein and PPI data")
            protein_matching_row = protein_df[protein_df['Transcript id'] == tid]
            if not protein_matching_row.empty:
                st.dataframe(protein_matching_row)
                st.write("\n")
                protein_transcript = protein_matching_row['preferredName'].values[0]
                st.write(f"Protein Transcript for {tid}: {protein_transcript}")

                network_link = get_string_network_link(protein_transcript)
                st.write("Redirected Network URL -->", network_link)
                st.write("\n")
            else:
                st.write(f"No match found for Gene id: {tid} in protein data\n")
            
            st.subheader("Cellular Localisation data")
            cello_matching_row = cello_df[cello_df['Transcript id'] == tid]
            if not cello_matching_row.empty:
                cello_matching_row = cello_matching_row.head(1)
                cello_matching_row = cello_matching_row.drop(columns=["#Combined:"])
                st.dataframe(cello_matching_row)
                st.write("\n")
            else:
                st.write(f"No match found for Gene id: {tid} in Cellular Protein Localisation data\n")

            st.subheader("GO and KEGG data")
            GO_matching_row = GO_df[GO_df['Transcript id'] == tid]
            if not GO_matching_row.empty:
                st.dataframe(GO_matching_row)
                st.write("\n")
            else:
                st.write(f"No match found for Gene id: {tid} in GO KEGG data\n")

            temp_df = df.copy()
            st.subheader("FPKM Matrix Atlas data")
            result = temp_df[temp_df['Transcript id'] == tid]
            result = result.drop(columns=['Genomic Coordinates', 'mRNA', 'lncRNA','Genomic Sequence','Transcript Sequence','Peptide Sequence','Cds Sequence','Promoter Sequence'])
            st.dataframe(result)

            st.subheader("SNP Calling data")
            st.write("Result data for both Cultivated and Wild varieties will be downloaded in the form of HTML content. Click on the files to view data\n")
            try:
                con1,con2=st.columns(2)
                # Cultivated SNP Download Button
                with con1:
                    html_Cultivated_page_source = automate_Cultivated_task(tid)
                    b64_html = base64.b64encode(html_Cultivated_page_source.encode()).decode()  # Convert to base64
                    html_href = f'<a href="data:text/html;base64,{b64_html}" download="{tid}_Cultivated_SNP.html">Download Cultivated SNP as .html</a>'
                    st.markdown(html_href, unsafe_allow_html=True)
                    iframe_CODE = f'<iframe src="data:text/html;base64,{b64_html}" width="100%" height="500"></iframe>'
                    with st.expander("View Cultivated SNP", expanded=True):
                        st_components_html(iframe_CODE, height=500)

                # Wild SNP Download Button
                with con2:
                    html_wild_page_source = automate_Wild_task(tid)
                    b64_html2 = base64.b64encode(html_wild_page_source.encode()).decode()  # Convert to base64
                    html_href2 = f'<a href="data:text/html;base64,{b64_html2}" download="{tid}_Wild_SNP.html">Download Wild SNP as .html</a>'
                    st.markdown(html_href2, unsafe_allow_html=True)
                    iframe_CODE2 = f'<iframe src="data:text/html;base64,{b64_html2}" width="100%" height="500"></iframe>'
                    with st.expander("View Wild SNP", expanded=True):
                        st_components_html(iframe_CODE2, height=500)

            except Exception as e:
                st.write("Error ! Error ! Error !")
                st.write("Unable to fetch data from the server. Please try again later -->","https://cegresources.icrisat.org/cicerseq/?page_id=3605\n")

            st.subheader("RNA data")
            if pd.notna(matching_row['mRNA'].values[0]):
                st.write("mRNA present : Yes ( 1 )\n")
            else:
                st.write("mRNA absent : No ( 0 )\n")

            st.subheader("lncRNA data")
            if pd.notna(matching_row['lncRNA'].values[0]):
                st.write("lncRNAs present : Yes ( 1 )")
            else:
                st.write("lncRNAs absent : No ( 0 )\n")

            st.subheader("miRNA data")
            miRNA_matching_rows = miRNA_df[miRNA_df['Target_Acc.'] == tid]
            if not miRNA_matching_rows.empty:
                st.dataframe(miRNA_matching_rows)
                st.write("\n")
            else:
                st.write(f"No match found for Gene id: {tid} in miRNA data\n")

            #Orthologous analysis
            st.subheader("Orthologs data")
            ortho_df = filter_orthologs(tid)
            if not ortho_df.empty:
                st.dataframe(ortho_df)
                st.write("\n")
            else:
                st.write(f"No match found for Gene id: {tid} in Orthologs data\n")
            st.subheader("Inparalogs data")
            para_df = filter_paralogs(tid)
            if not para_df.empty:
                st.dataframe(para_df)
                st.write("\n")
            else:
                st.write(f"No match found for Gene id: {tid} in Inparalogs data\n")
            st.write("For detailed results visit the following link -->","https://orthovenn3.bioinfotoolkits.net/result/88e9a64330ba4d64b78fc5fd9561cd64/orthologous\n")
            
        else:
            st.write("Gene ID not found\n")
    else:
        st.write("...Error...\n")

def user_input_menu(tid):
        transcriptid_info(tid)
        if tid in combined_data['Transcript id'].values:
            st.subheader("Model Prediction")
            resultant_value = combined_data[combined_data['Transcript id'] == tid]['Resultant'].values[0]
            st.write(f"Stage/Tissue Group Concerned {tid}: {resultant_value}\n")
            unique_resultant_values = []
            tissues = resultant_value.split(", ")
            for tissue in tissues:
                if tissue not in unique_resultant_values:
                        unique_resultant_values.append(tissue)
            perf_chart(unique_resultant_values)
        else:
            st.subheader("Model Prediction")
            st.write("Expression Status : normal  ( no particular tissue/stage favoured ) 0 \n")


def multi_user_input_menu(mtid):
        multi_transcriptid_info(mtid)
        if "," in mtid:
                mtid_list = mtid.split(",")
        elif " " in mtid:
                mtid_list = mtid.split(" ")
        else:
                mtid_list= [mtid.strip()]
        mtid_list.sort()        
        st.subheader("Model Prediction")
        unique_resultant_values = []
        for tid in mtid_list:
            if tid in combined_data['Transcript id'].values:
                resultant_value = combined_data[combined_data['Transcript id'] == tid]['Resultant'].values[0]
                st.write(f"{tid} Stage/Tissue Group Concerned: {resultant_value}\n")
                tissues = resultant_value.split(", ")
                for tissue in tissues:
                    if tissue not in unique_resultant_values:
                        unique_resultant_values.append(tissue)
            else:
                st.write(f"{tid} Expression Status : normal  ( no particular tissue/stage favoured ) 0 \n")
        if unique_resultant_values:
            perf_chart(unique_resultant_values)

def multi_transcriptid_info(mtid):
    mtid_list = [tid.strip() for tid in mtid.replace(",", " ").split()]
    mtid_list.sort()
    if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
        matching_rows = df[df['Transcript id'].isin(mtid_list)]
        if not matching_rows.empty:
            st.subheader("\nSequences data")
            for tid in mtid_list:
                matching_rows = df[df['Transcript id'] == tid]
                if not matching_rows.empty:
                    cds_code = format_sequence(matching_rows['Cds Sequence'].values[0])
                    peptide_code = format_sequence(matching_rows['Peptide Sequence'].values[0])
                    transcript_code = format_sequence(matching_rows['Transcript Sequence'].values[0])
                    gene_code = format_sequence(matching_rows['Genomic Sequence'].values[0])
                    promote_code = format_sequence(matching_rows['Promoter Sequence'].values[0])

                    with st.expander(f"{tid} Genomic Sequence"):
                        st.code(gene_code, language="text")
                    with st.expander(f"{tid} Transcript Sequence"):
                        st.code(transcript_code, language="text")
                    with st.expander(f"{tid} CDS Sequence"):
                        st.code(cds_code, language="text")
                    with st.expander(f"{tid} Peptide Sequence"):
                        st.code(peptide_code, language="text")
                    with st.expander(f"{tid} Promoter Sequence"):
                        st.code(promote_code, language="text")

                    header = f">{tid}|{tid}"
                    promote_file = f"{header}\n{promote_code}\n"
                    
                    # Convert to base64 for download
                    b64 = base64.b64encode(promote_file.encode()).decode()  # Convert to base64
                    href = f'<a href="data:text/plain;base64,{b64}" download="{tid}_promoter_sequence.txt">Download Promoter Sequence as .txt</a>'
                    st.markdown(href, unsafe_allow_html=True)

                    # Provide link for further analysis
                    st.write(f"Paste the promoter sequence for {tid} on the following link to get promoter region analysis!")
                    st.write("https://bioinformatics.psb.ugent.be/webtools/plantcare/html/search_CARE_onCluster.html\n")
                    st.write("\n")
                else:
                    st.write(f"No matching data found for Gene ID: {tid}\n")

            st.subheader("Protein and PPI data")
            result = pd.DataFrame()
    
            for tid in mtid_list:
                protein_matching_rows = protein_df[protein_df['Transcript id'] == tid]
                if not protein_matching_rows.empty:
                    result = pd.concat([result, protein_matching_rows], ignore_index=True)
                else:
                    st.write(f"No match found for Gene id: {tid} in protein data\n")
            if not result.empty:
                sorted_result = result.sort_values(by="Transcript id")
                st.dataframe(sorted_result)
                for tid in mtid_list:
                    protein_matching_rows = protein_df[protein_df['Transcript id'] == tid]
                    if not protein_matching_rows.empty:
                        protein_transcript = protein_matching_rows['preferredName'].values[0]
                        st.write(f"Protein Transcript for {tid}: {protein_transcript}")
                        
                        network_link = get_string_network_link(protein_transcript)
                        st.write("Redirected Network URL -->", network_link)
                        st.write("\n")
                    else:
                        st.write(f"No match found for Gene id: {tid} in protein data\n")
            else:
                st.write("No protein data found for any of the provided Gene IDs.\n")

            st.subheader("\nCellular Localisation data")
            result = pd.DataFrame()
            for tid in mtid_list:
                temp_result = cello_df[cello_df['Transcript id'] == tid]
                if not temp_result.empty:
                    if '#Combined:' in temp_result.columns:
                        temp_result = temp_result.drop(columns=['#Combined:'])
                    result = pd.concat([result, temp_result], ignore_index=True)
                else:
                    st.write(f"No match found for Gene id: {tid} in Cellular Protein Localisation data\n")
            if not result.empty:
                result = result.drop_duplicates(subset=['Transcript id'])
                st.dataframe(result)
            else:
                st.write("No cellular localisation data found for any of the provided Gene IDs.\n")

            # Gene Ontology and KEGG data
            st.subheader("\nGO and KEGG data")
            GO_matching_row = GO_df[GO_df['Transcript id'].isin(mtid_list)]
            result=pd.DataFrame()
            for tid in mtid_list:
                if not GO_matching_row.empty:
                    temp_result = GO_matching_row[GO_matching_row['Transcript id'] == tid]
                    result = pd.concat([result, temp_result], ignore_index=True)
                else:
                    st.write(f"No match found for Gene ID: {tid} in GO KEGG data\n")
            if not result.empty:
                result = result.drop_duplicates(subset=['Transcript id'])
                st.dataframe(result)        

            result=pd.DataFrame()
            temp_df = df.copy()
            st.subheader("FPKM Matrix Atlas data")
            for tid in mtid_list:
                temp_result = temp_df[temp_df['Transcript id'] == tid]
                temp_result = temp_result.drop(columns=['Genomic Coordinates', 'mRNA', 'lncRNA','Genomic Sequence','Transcript Sequence','Peptide Sequence','Cds Sequence','Promoter Sequence'])
                result = pd.concat([result, temp_result], ignore_index=True)
            sorted_result = result.sort_values(by="Transcript id")
            st.dataframe(sorted_result)

            st.subheader("\nSNP Calling data")
            st.write("Result data for both Cultivated and Wild varieties will be downloaded in the form of HTML content. Click on the files to view data\n")
            for tid in mtid_list:
                try:
                    com1,com2=st.columns(2)
                    # Cultivated SNP Download Button
                    with com1:
                        #st.markdown(f"#### {tid} Cultivated SNP")
                        html_Cultivated_page_source = automate_Cultivated_task(tid)
                        b64_html = base64.b64encode(html_Cultivated_page_source.encode()).decode()  # Convert to base64
                        html_href = f'<a href="data:text/html;base64,{b64_html}" download="{tid}_Cultivated_SNP.html">Download {tid} Cultivated SNP as .html</a>'
                        st.markdown(html_href, unsafe_allow_html=True)
                        iframe_CODE = f'<iframe src="data:text/html;base64,{b64_html2}" width="100%" height="500"></iframe>'
                        with st.expander(f"View {tid} Cultivated SNP", expanded=True):
                            st_components_html(iframe_CODE, height=500)
                    # Wild SNP Download Button
                    with com2:
                        #st.markdown(f"#### {tid} Wild SNP")
                        html_wild_page_source = automate_Wild_task(tid)
                        b64_html2 = base64.b64encode(html_wild_page_source.encode()).decode()  # Convert to base64
                        html_href2 = f'<a href="data:text/html;base64,{b64_html2}" download="{tid}_Wild_SNP.html">Download {tid} Wild SNP as .html</a>'
                        st.markdown(html_href2, unsafe_allow_html=True)
                        iframe_CODE2 = f'<iframe src="data:text/html;base64,{b64_html2}" width="100%" height="500"></iframe>'
                        with st.expander(f"View {tid} Wild SNP", expanded=True):
                            st_components_html(iframe_CODE2, height=500)

                except Exception as e:
                    st.write(f"Error fetching data for Gene ID: {tid}")
                    st.write("Unable to fetch data from the server. Please try again later -->","https://cegresources.icrisat.org/cicerseq/?page_id=3605")

            st.subheader("RNA data")
            for tid in mtid_list:
                matching_row = df[df['Transcript id'] == tid]
                if not matching_row.empty:
                    if pd.notna(matching_row['mRNA'].values[0]):
                        st.write(f"{tid} mRNA present : Yes ( 1 )\n")
                    else:
                        st.write(f"{tid} mRNA absent : No ( 0 )\n")
                else:
                    st.write(f"No match found for Gene id: {tid} in RNA data\n")
            
            st.subheader("lncRNA data")
            for tid in mtid_list:
                matching_row = df[df['Transcript id'] == tid]
                if not matching_row.empty:
                    if pd.notna(matching_row['lncRNA'].values[0]):
                        st.write(f"{tid} lncRNAs present : Yes ( 1 )\n")
                    else:
                        st.write(f"{tid} lncRNAs absent : No ( 0 )\n")
                else:
                    st.write(f"No match found for Gene id: {tid} in lncRNA data\n")

            st.subheader("miRNA data")
            miRNA_matching_rows = miRNA_df[miRNA_df['Target_Acc.'].isin(mtid_list)]
            result=pd.DataFrame()
            for tid in mtid_list:
                if not miRNA_matching_rows.empty:
                    temp_result = miRNA_matching_rows[miRNA_matching_rows['Target_Acc.'] == tid]
                    result = pd.concat([result, temp_result], ignore_index=True)
                else:
                    st.write(f"No match found for Gene id: {tid} in miRNA data\n")
            if not result.empty:
                sorted_result = result.sort_values(by="Target_Acc.")
                st.dataframe(sorted_result)
            
            #Orthologous analysis
            st.subheader("Orthologs data")
            for tid in mtid_list:
                ortho_df = filter_orthologs(tid)
                if not ortho_df.empty:
                    st.write(tid)
                    st.dataframe(ortho_df)
                else:
                    st.write(f"No match found for Gene id: {tid} in Orthologs data")
            st.subheader("\nInparalogs data")
            for tid in mtid_list:
                para_df = filter_paralogs(tid)
                if not para_df.empty:
                    st.write(tid)
                    st.dataframe(para_df)
                else:
                    st.write(f"No match found for Gene id: {tid} in Inparalogs data")
            st.write("For detailed results visit the following link -->","https://orthovenn3.bioinfotoolkits.net/result/88e9a64330ba4d64b78fc5fd9561cd64/orthologous")

        else:
            st.write("Gene ID not found\n")
    else:
        st.write("...Error...\n")

def process_locid(locid):
    result = protein_df[protein_df['preferredName'] == locid]
    if not result.empty:
        result = result.iloc[0]['Transcript id']
        st.write(f"Gene ID for {locid} is {result}")
        return result
    else:
        return None
        
def process_mlocid(mlocid):
    mlocid_list = [item.strip() for item in mlocid.replace(",", " ").split()]
    mlocid_list = list(set(mlocid_list))
    transcript_ids = []
    for locid in mlocid_list:
        transcript_id = process_locid(locid)
        if transcript_id:
            transcript_ids.append(transcript_id)
    result=",".join(transcript_ids)
    return result

def col(selected_tissue):
    if selected_tissue == "ST":
        return "#5E5E5E"
    elif selected_tissue == "GT":
        return "#54AE32"
    elif selected_tissue == "RT":
        return "#F9DB57"
    elif selected_tissue == "FDS":
        return "#C23175"
    elif selected_tissue == "FP":
        return "#3274B5"

def perf_chart(selected_tissues):
    data = {"Tissue/Stages/File": ["ST", "GT", "RT", "FDS", "FP"],
        "Training Accuracy": [0.956180239768499, 0.959487391484084, 0.939024390243902, 0.957833815626292, 0.949359239355106],
        "Test Accuracy": [0.946280991735537, 0.954545454545455, 0.943801652892562, 0.952892561983471, 0.947107438016529],
        "Grid Search": [0.961346970694061, 0.960729486270052, 0.952463100498261, 0.966723572093977, 0.95845419504816],
        "Random Search": [0.964241455639406, 0.963416291332997, 0.956182322425154, 0.967137649884195, 0.957214311964241]}
    df = pd.DataFrame(data)
    df.set_index("Tissue/Stages/File", inplace=True)
    filtered_df = df.loc[selected_tissues]
    if len(selected_tissues) == 1:
        clr = col(selected_tissues[0])
        st.bar_chart(filtered_df.T, height=400, color=clr,x_label='Metrics', y_label='Accuracy/Score')
    else:
        colors = [col(tissue) for tissue in selected_tissues]
        st.bar_chart(filtered_df.T, height=400, color=colors,stack=False,x_label='Metrics', y_label='Accuracy/Score')

def svm_charts():
    data = {"Tissue/Stages/File": ["Seed Tissues", "Green Tissues", "Root Tissues", "Flower Development Stages", "Flower Parts"],
        "Training Accuracy": [0.956180239768499, 0.959487391484084, 0.939024390243902, 0.957833815626292, 0.949359239355106],
        "Test Accuracy": [0.946280991735537, 0.954545454545455, 0.943801652892562, 0.952892561983471, 0.947107438016529],
        "Grid Search": [0.961346970694061, 0.960729486270052, 0.952463100498261, 0.966723572093977, 0.95845419504816],
        "Random Search": [0.964241455639406, 0.963416291332997, 0.956182322425154, 0.967137649884195, 0.957214311964241]}

    df = pd.DataFrame(data)
    df.set_index("Tissue/Stages/File", inplace=True)

    st.title("Model Performance Analysis")
    con9=st.container(border=True)
    with con9:
        col1,col2,col3=st.columns([1,2,1])
        with col2:
            con=st.container(border=True)
            con.subheader("Dataset")
            con.dataframe(df)

        col1,col2=st.columns(2)
        with col1:
            container = st.container(border=True)
            container.subheader("Training Accuracy")
            container.bar_chart(df["Training Accuracy"],x_label='Tissue/Stages/File',y_label='Accuracy')

            # Bar chart for Test Accuracy
            container=st.container(border=True)
            container.subheader("Test Accuracy")
            container.bar_chart(df["Test Accuracy"],x_label='Tissue/Stages/File',y_label='Accuracy',color='#AFDC8F')

        with col2:
            container=st.container(border=True)
            container.subheader("Grid Search")
            container.bar_chart(df["Grid Search"],x_label='Tissue/Stages/File',y_label='Score',color='#FF6347')

            container=st.container(border=True)
            container.subheader("Random Search")
            container.bar_chart(df["Random Search"],x_label='Tissue/Stages/File',y_label='Score',color='#FFD700')

    model_data = {"Algorithm": ["linear", "rbf", "poly_deg1", "poly_deg2", "poly_deg3"],
        "Train Accuracy": [0.8444966831970117, 0.9776840342628969, 0.8444966831970117, 0.9753332903973723, 0.896470664004637],
        "Test Accuracy": [0.8429933024214322, 0.9774600721277692, 0.8429933024214322, 0.9774600721277692, 0.8952859350850078]}

    m_df = pd.DataFrame(model_data)
    m_df.set_index("Algorithm", inplace=True)

    container=st.container(border=True)
    with container:
        col1,col2=st.columns([1,2])
        with col1:
            container=st.container(border=True,height=630)
            container.subheader("Dataset")
            container.dataframe(m_df,use_container_width=True)
            container.expander("Linear",expanded=False).write("Support Vector Machine with a Linear Kernel (SVM Linear) \nDescription: A linear kernel is used when the data is linearly separable. The model tries to find the best hyperplane that separates the classes")
            container.expander("RBF",expanded=False).write("Support Vector Machine with a Radial Basis Function Kernel (SVM RBF) \nDescription: The Radial Basis Function kernel is used when the data is not linearly separable. It is used to map the data into a higher-dimensional space where it can be linearly separable.")
            container.expander("Poly_deg1",expanded=False).write("Support Vector Machine with a Polynomial Kernel of Degree 1 (SVM Poly Degree 1) \nDescription: This is a polynomial kernel with degree 1, which is essentially a linear kernel. In this case, the polynomial kernel behaves the same as the linear kernel.")
            container.expander("Poly_deg2",expanded=False).write("Support Vector Machine with a Polynomial Kernel of Degree 2 (SVM Poly Degree 2) \nDescription: The polynomial kernel of degree 2 allows the decision boundary to be a quadratic function, which can be useful for separating classes in a non-linear way.")
            container.expander("Poly_deg3",expanded=False).write("Support Vector Machine with a Polynomial Kernel of Degree 3 (SVM Poly Degree 3) \nDescription: The polynomial kernel of degree 3 allows for more flexibility in modeling complex, non-linear decision boundaries by fitting cubic curves to separate the data.")
        with col2:
            container=st.container(border=True,height=630)
            container.subheader("Model Performance")
            container.bar_chart(m_df,stack=False,x_label='Algorithms',y_label='Accuracy',color=['#AFDC8F','#FF6347'],height=530)
    return

def tsi_plot():
    df = tsi_df
    st.title("Tissue Specificity Index (TSI) Analysis")
    con=st.container(border=True)
    with con:
        con=st.container(border=True)
        col1,col2=st.columns([10,9])
        with col1:
            con=st.container(border=True,height=500)
            df['Category'] = 'non-TF'
            df.loc[df['TF family'].notna(), 'Category'] = 'TF'
            df.loc[df['lncRNA'].notna(), 'Category'] = 'lncRNA'
            df['TSI value (%)'] = df['TSI value'] * 100
            con.subheader("Dataset")
            con.dataframe(df)
        with col2:
            con=st.container(border=True,height=500)
            con.subheader("Percentage Presence of lncRNA, TF, and non-TF")
            category_counts = df['Category'].value_counts(normalize=True) * 100
            category_counts = category_counts[['non-TF', 'lncRNA', 'TF']]
            con.bar_chart(category_counts,color=['#AFDC8F'],y_label='Percentage (%)',x_label='Category',height=360)

        con=st.container(border=True)
        con.subheader("TSI Value by Tissue Type")
        tsi_by_tissue = df.groupby('TSI tissue')['TSI value (%)'].mean().reset_index()
        con.bar_chart(tsi_by_tissue.set_index('TSI tissue'),color='#FF6347',y_label='TSI value (%)',x_label='Tissue Type')
        con=st.container(border=True)

        con.subheader("Tissue-Specific Distribution of lncRNA, TF, and non-TF")
        category_counts_by_tissue = df.groupby(['TSI tissue', 'Category']).size().unstack(fill_value=0)
        category_percentages = category_counts_by_tissue.div(category_counts_by_tissue.sum(axis=1), axis=0) * 100

        custom_order = ['GS', 'S', 'R', 'Rtip', 'RH', 'YL', 'ML', 'Brac', 'SAM', 'FB1', 'FB2', 'FB3', 'FB4', 'FL1', 'FL2', 'FL3', 'FL4', 'FL5', 'Cal', 'Cor', 'And', 'Gyn', 'Pedi', 'PodSh', 'SdCt', 'Emb', 'Endo', '5 DAP', '10 DAP', '20  DAP', '30  DAP', 'Nod']
        category_percentages = category_percentages.reindex(custom_order)
        category_percentages = category_percentages[['non-TF', 'TF', 'lncRNA']]
        con.bar_chart(category_percentages,y_label='TSI tissue',x_label='Percentage (%)',color=['#FF6347','#FFD700','#0066CC'],height=500,width=700)
    return
