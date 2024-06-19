import streamlit as st
import pandas as pd
import requests
import json
import os
import glob

def get_user_games(steamid):
    res_name = requests.get(f"https://api.steampowered.com/IPlayerService/GetPlayerLinkDetails/v1/?key=66EA82E88EC7863E2C15DA88622B37A1&steamids%5B0%5D={steamid}")
    res_games = requests.get(f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key=66EA82E88EC7863E2C15DA88622B37A1&steamid={steamid}&include_appinfo=true")

    username = res_name.json()["response"]["accounts"][0]["public_data"]["persona_name"]
    games_json = res_games.json()


    with open(f"data/{username}OwnedGames.json", 'w') as games_file:
        json.dump(games_json, games_file)

    return games_json["response"]["games"]
    

st.title("Games inventory")

games_json = ""

st.write("Enter your Steam ID")
steamid = st.text_input("Steam ID")

username_response = requests.get(f"https://api.steampowered.com/IPlayerService/GetPlayerLinkDetails/v1/?key=66EA82E88EC7863E2C15DA88622B37A1&steamids%5B0%5D={steamid}").json()["response"]
if "accounts" in username_response:
    username = username_response["accounts"][0]["public_data"]["persona_name"]
    st.write(username)

if st.button("Get your games"):
    games_json = get_user_games(steamid)

st.write("Your games :")
# Résultat de la récup de données
games_json = list(games_json)
games_json.sort(key=lambda x: x["playtime_forever"], reverse=True)

with st.container(height=500):
    st.write(games_json)


"---"

def delete_data_file(profile):
    os.remove(f"data/{profile}OwnedGames.json")

file_todelete = st.selectbox(
    ":red[Choose your data profile to delete :]",
    tuple([ p[5:-15] for p in glob.glob("data/*OwnedGames.json") ]))

st.button(":red[Delete]", on_click=delete_data_file, args=(file_todelete,))