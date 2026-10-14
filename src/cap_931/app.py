import streamlit as st

st.title("My First Streamlit Application")

user_name = st.text_input("Enter your name")

if st.button("Submit"):
    st.write(f"Hello, {user_name}!")