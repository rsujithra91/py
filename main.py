import streamlit as st
st.title("Streamlit App")
name=st.text_input("Enter your name")
if st.button("submit"):
  st.write("Name is {name}")
