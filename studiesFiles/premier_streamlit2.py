import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache_data
def load_data (fileName : str):
    return pd.read_csv(fileName + ".csv")

def onPageChanged (pageName : str):
    st.session_state["page"] = pageName
    st.write(f"coucou page {pageName}")

st.write('hello !')
name : str = st.text_input("Give us your name", placeholder="Name")
print(f"\"name\" current value : {name}")

if not name == "":
    st.write("Bonjour " + name)

# df1 = pd.read_csv("houses.csv")
df1 = load_data("houses")
st.write(df1)

# df2 = pd.read_csv("temperatures.csv")
# st.line_chart(df2)


fig1 = plt.figure()
plt.scatter(df1["size"], df1["price"])
st.pyplot(fig1)

if 'page' not in st.session_state:
    st.session_state["page"] = "accueil"
st.write(st.session_state)

# if st.session_state["page"] == "accueil":
#     st.write("coucou page accueil")

st.sidebar.button("Accueil", on_click=onPageChanged, args=("Accueil",))
st.sidebar.button("Page 2", on_click=onPageChanged, args=("Page 2",))
st.write(f"coucou page {st.session_state.page}")

df = { "lat" : [ 48.866667, 45.7578137, 43.5298424 ],
       "lon" : [ 2.333333, 4.8320114, 5.4474738 ] }
st.map(df)


# Data
# Input clé steam
# Linear
# Content filter
# Pondération