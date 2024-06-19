import pandas as pd

class DbHandler:
    def __init__(self, game_data, user_game_data):
        self.game_data = game_data
        self.user_game_data = user_game_data
    
    def setupDataFrames(self):
        self.game_df = pd.DataFrame(self.game_data)
        self.user_game_data = list(filter(lambda d: d['appid'] in self.game_df['appid'].values, self.user_game_data))
        self.user_games_df = pd.DataFrame(self.user_game_data)

    def cleanDataFrames (self):
        categories = self.game_df['categories'].explode().unique()
        genres = self.game_df['genres'].explode().unique()

        for category in categories:
            self.game_df[f'category_{category}'] = self.game_df['categories'].apply(lambda x: 1 if type(x) == list and category in x else 0)

        for genre in genres:
            self.game_df[f'genre_{genre}'] = self.game_df['genres'].apply(lambda x: 1 if type(x) == list and genre in x else 0)

        platforms = ['windows', 'mac', 'linux']
        for platform in platforms:
            self.game_df[f'platform_{platform}'] = self.game_df['platforms'].apply(lambda x: 1 if x.get(platform, False) else 0)

        self.game_df['recommendations'] = self.game_df['recommendations'].fillna(0)
        self.game_df['metacritic'] = self.game_df['metacritic'].fillna(self.game_df['metacritic'].mean())

        self.game_df.drop(columns=['categories', 'developers', 'publishers', 'genres', 'platforms', 'release_date', 'price_overview', 'name'], inplace=True)

        self.game_df.set_index('appid', inplace=True)
