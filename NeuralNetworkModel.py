from sklearn.neural_network import MLPRegressor
from DbHandler import DbHandler
import numpy as np

class NeuralNetworkModel:
    def __init__(self, dbHandler : DbHandler):
        self.dbHandler = dbHandler
        self.countReco = 0
        self.recommandations = []
    
    def setupTrainedData (self):
        self.user_playtime_df = self.dbHandler.user_games_df[['appid', 'playtime_forever']].set_index('appid')
        self.all_playtime_df = self.dbHandler.game_df.merge(self.user_playtime_df, left_index=True, right_index=True, how='left').fillna(0)
    
    def trainModel(self):
        self.model = MLPRegressor(hidden_layer_sizes=(128, 64, 32), activation='relu', solver='adam', max_iter=500)
        self.model.fit(self.dbHandler.game_df[self.dbHandler.game_df.index.isin(self.dbHandler.user_games_df['appid'])],
                       self.user_playtime_df.values)
    
    def predict(self, n=5):
        if len(self.recommandations) <= 0:
            predicted_scores = self.model.predict(self.dbHandler.game_df)
            owned_game_ids = self.dbHandler.user_games_df['appid'].values
            not_owned_mask = ~self.all_playtime_df.index.isin(owned_game_ids)
            c = len(list(filter(lambda d: not d, not_owned_mask)))
            predicted_playtime_not_owned = predicted_scores[not_owned_mask]
            self.game_indices_not_owned = self.all_playtime_df.index[not_owned_mask]
            self.recommandations = np.argsort(predicted_playtime_not_owned)
        top_recommended_indices = self.recommandations[-(n + self.countReco):]
        recommended_games = self.game_indices_not_owned[top_recommended_indices[:n]]
        self.countReco += n
        return list(filter(lambda d: d['appid'] in recommended_games, self.dbHandler.game_data))
