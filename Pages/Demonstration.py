import streamlit as st
from backend import generate_signed_url

def demonstration_page():
    st.title("Demonstration Page")
    st.write("**Learn how to use this interface**")
    st.write("This page helps you understand how to use the app through video tutorials. Follow the steps below:")

    st.subheader("Navigation Tutorial")
    video_url = generate_signed_url("Videos/navigation.mp4")
    if video_url:
        st.video(video_url, start_time=0)
    else:
        st.warning("Video not found or unable to generate URL.")

    st.subheader("Single Task Tutorial")
    video_url = generate_signed_url("Videos/start_task1.mp4")
    if video_url:
        st.video(video_url, start_time=0)
    else:
        st.warning("Video not found or unable to generate URL.")
    st.markdown("""
    1. Navigate to the **Start Task** page.
    2. Enter the 8-character code when prompted.
    3. Click the **Start** button to begin the task.
    4. Wait for the task to complete and view the results.""")

    st.subheader("Multi Task Tutorial")
    video_url = generate_signed_url("Videos/start_task2.mp4")
    if video_url:
        st.video(video_url, start_time=0)
    else:
        st.warning("Video not found or unable to generate URL.")
    st.markdown("""
    1. Navigate to the **Start Task** page.
    2. Enter the 8-character code when prompted.
    3. Click the **Start** button to begin the task.
    4. Wait for the task to complete and view the results.""")

    st.subheader("Glossary Tutorial")
    video_url = generate_signed_url("Videos/glossary.mp4")
    if video_url:
        st.video(video_url, start_time=0)
    else:
        st.warning("Video not found or unable to generate URL.")

    st.subheader("About Tutorial")
    video_url = generate_signed_url("Videos/contact us.mp4")
    if video_url:
        st.video(video_url, start_time=0)
    else:
        st.warning("Video not found or unable to generate URL.")

if __name__ == "__page__":
    demonstration_page()
