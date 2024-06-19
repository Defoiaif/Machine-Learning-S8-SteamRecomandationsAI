import streamlit as st
import glob
import json
from DbHandler import DbHandler
from NeuralNetworkModel import NeuralNetworkModel

st.set_page_config("Neural Network")

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

    model = NeuralNetworkModel(dbHandler)
    model.setupTrainedData()
    model.trainModel()

    st.title("Neural network")

    reco = model.predict()
    st.write("Your recommendations :")
    st.write([x["name"] for x in reco])
    st.write("JSON :")
    with st.container(height=500):
        st.write(reco)