import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

def set_page(page: str):
    st.session_state["page"] = page

st.write(st.session_state)
set_page("donnees")

if st.sidebar.button("Accueil", on_click=set_page, args=("donnees",)):
    st.write("Coucou page d'accueil")
    st.button("test1", on_click=print("Test1"))
if st.sidebar.button("Page 2", on_click=set_page, args=("reco",)):
    st.write("Coucou page 2")
    st.write("test2")


df = pd.read_csv("pos.csv")
st.map(df)