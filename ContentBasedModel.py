from sklearn.metrics.pairwise import cosine_similarity
from DbHandler import DbHandler

class ContentBasedModel:
    def __init__(self, dbHandler : DbHandler):
        self.dbHandler = dbHandler
        self.similarity_matrix = cosine_similarity(dbHandler.game_df)

        print(dbHandler.game_df)
        print(self.similarity_matrix)
    
    def content_based_recommendations(self, top_n=5):
        idx = self.dbHandler.game_df.index \
                  .get_loc(self.dbHandler.user_games_df.loc[self.dbHandler.user_games_df['playtime_forever'].idxmax()]['appid'])
        sim_scores = list(enumerate(self.similarity_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n+1]
        
        recommended_games = [self.dbHandler.game_df.index[i[0]] for i in sim_scores]
        return list(filter(lambda d: d['appid'] in recommended_games, self.dbHandler.game_data))
