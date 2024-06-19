from DbHandler import DbHandler
from ContentBasedModel import ContentBasedModel
from NeuralNetworkModel import NeuralNetworkModel
from json import load

with open("./data/steamGames.json", "r") as f:
    game_data : list = load(f)['applist']['apps']

with open("./data/robinOwnedGames.json", "r") as f:
    user_game_data = load(f)["response"]["games"]

dbHandler = DbHandler(game_data, user_game_data)
dbHandler.setupDataFrames()
dbHandler.cleanDataFrames()

# cbModel = ContentBasedModel(dbHandler)
# cbReco = cbModel.content_based_recommendations()

nnModel = NeuralNetworkModel(dbHandler)
nnModel.setupTrainedData()
nnModel.trainModel()
while True:
    nnReco = nnModel.predict()
    print()
