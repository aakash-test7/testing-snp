import streamlit as st
from backend import user_input_menu, multi_user_input_menu, process_locid, process_mlocid

def start_task_page():
    st.title("Start Task")
    st.write("**Begin the task by interacting with the backend process.**")
    col1, col2 = st.columns(2)

    with col1:
        con1=st.container(border=True)
        tid = con1.text_input("Enter the Gene ID: ", placeholder="e.g., Ca_00001", key="Tid_input1").strip()
        mtid = con1.text_input("Enter multiple Gene IDs: ", placeholder="e.g., Ca_00001, Ca_00002", key="mTid_input2").strip()
        if mtid:
            mtid_list = [item.strip() for item in mtid.replace(",", " ").split()]
            mtid_list = list(set(mtid_list))
            mtid = ",".join(mtid_list)

    with col2:
        con2=st.container(border=True)
        locid = con2.text_input("Enter the NCBI ID: ", placeholder="e.g., LOC101511858", key="Locid_input1").strip()
        mlocid = con2.text_input("Enter multiple NCBI IDs: ", placeholder="e.g., LOC101511858, LOC101496413", key="mLocid_input2").strip()
        if mlocid:
            mlocid_list = [item.strip() for item in mlocid.replace(",", " ").split()]
            mlocid_list = list(set(mlocid_list))
            mlocid = ",".join(mlocid_list)

    if st.button("Start"):
        if tid:
            result = user_input_menu(tid)
            st.write(result)
            st.toast("Task completed successfully.")
        elif mtid:
            result = multi_user_input_menu(mtid)
            st.write(result)
            st.toast("Task completed successfully.")
        elif locid:
            tid = process_locid(locid)
            result = user_input_menu(tid)
            st.write(result)
            st.toast("Task completed successfully.")
        elif mlocid:
            mtid = process_mlocid(mlocid)
            result = multi_user_input_menu(mtid)
            st.write(result)
            st.toast("Task completed successfully.")
        else:
            st.warning("Need either a Gene ID or NCBI ID to proceed.")
    elif tid == "":
        st.warning("Need Gene ID/ NCBI ID to proceed.")
    else:
        st.write("Press the 'Start' button to begin the task.")
        st.write("Follow the instructions or check out demonstrations")

if __name__ == "__page__":
    start_task_page()
