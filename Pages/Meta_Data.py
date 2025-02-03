import streamlit as st
from backend import generate_signed_url, svm_charts, tsi_plot

def meta_data_page():
    st.title("Meta Data")
    st.write("**Key Insights and Analytics from the Application Backend**")
    svm_charts()
    tsi_plot()
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(generate_signed_url("Images/1.png"), caption="Expression Data Heatmap", use_container_width=True)
        st.write("")
        st.image(generate_signed_url("Images/2.png"), caption="SVM Kernel Performance", use_container_width=True)
        st.write("")
        st.image(generate_signed_url("Images/7.png"), caption="Tissue Specific Distribution Plots", use_container_width=True)
        st.write("")

    with col2:
        st.image(generate_signed_url("Images/4.png"), caption="Functional Annotation [Root Tissues]", use_container_width=True)
        st.write("")

    col3, col4 = st.columns(2)
    with col3:
        st.image(generate_signed_url("Images/11.png"), caption="Functional Annotation [Seed Tissues]", use_container_width=True)
        st.write("")

    with col4:
        st.image(generate_signed_url("Images/5.png"), caption="WGCNA Heatmaps", use_container_width=True)
        st.write("")

    st.image(generate_signed_url("Images/3.png"), caption="Performance Charts for All Files", use_container_width=True)

    col5, col6 = st.columns(2)
    with col5:
        st.image(generate_signed_url("Images/8.png"), caption="Functional Annotation [Flower Development Stages]", use_container_width=True)
        st.write("")
        st.image(generate_signed_url("Images/9.png"), caption="Functional Annotation [Flower Parts]", use_container_width=True)
        st.write("")

    with col6:
        st.image(generate_signed_url("Images/10.png"), caption="Functional Annotation [Green Tissues]", use_container_width=True)
        st.write("")
        st.image(generate_signed_url("Images/6.png"), caption="Comparison of lncRNAs, TF, and Non-TF", use_container_width=True)
        st.write("")

if __name__ == "__page__":
    meta_data_page()
