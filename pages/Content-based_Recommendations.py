import streamlit as st
import glob
import json
import matplotlib.pyplot as plt
from DbHandler import DbHandler
from ContentBasedModel import ContentBasedModel

st.set_page_config("Content-based Recommendation")


profile = st.selectbox(
    "Choose your data profile :",
    tuple([ p[5:-15] for p in glob.glob("data/*OwnedGames.json") ]),
    index=None)

if profile:
    with open(f"data/{profile}OwnedGames.json", 'r') as file:
        user_game_data = json.load(file)["response"]["games"]

    with open("data/steamGames.json", "r") as f:
        game_data : list = json.load(f)['applist']['apps']

    dbHandler = DbHandler(game_data, user_game_data)
    dbHandler.setupDataFrames()
    dbHandler.cleanDataFrames()

    model = ContentBasedModel(dbHandler)


    st.title("Content based recommendations")

    reco = model.content_based_recommendations()
    st.write("Your recommendations :")
    st.write([x["name"] for x in reco])
    st.write("JSON :")
    with st.container(height=500):
        st.write(reco)