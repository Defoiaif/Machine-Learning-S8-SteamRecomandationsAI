import json
from requests import Session
from time import sleep

SESSION = Session()

def getUsefulData (game : dict):
    if 'dlc' in game:
        game['dlc'] = len(game['dlc'])
    if 'achievements' in game:
        game['achievements'] = game['achievements']['total']
    if 'metacritic' in game:
        game['metacritic'] = game['metacritic']['score']
    game['release_date'] = game['release_date']['date']
    if 'recommendations' in game:
        game['recommendations'] = game['recommendations']['total']
    return {key: game[key] for key in game.keys() & {'required_age', 'pc_requirements', 'mac_requirements',
                                                     'linux_requirements', 'developers', 'publishers', 'price_overview',
                                                     'platforms', 'metacritic', 'categories', 'genres', 'recommendations',
                                                     'release_date', 'ratings'
                                                    }}

with open("steamGames.json", "r+") as gamesList:
    applist = json.load(gamesList)
    games : list = applist['applist']['apps']
    c = 0
    for i in range(len(games)):
        if 'price_overview' in games[i] and games[i]['price_overview'] >= 10000:
            try:
                response = SESSION.get("https://store.steampowered.com/api/appdetails?appids=" + str(games[i]['appid']))
                # response = SESSION.get("https://store.steampowered.com/api/appdetails?appids=" + str(2407760))
                while not response.status_code == 200:
                    print(games[i]['appid'])
                    print(response.status_code)
                    sleep(60)
                    response = SESSION.get("https://store.steampowered.com/api/appdetails?appids=" + str(games[i]['appid']))
                    if response.status_code == 200:
                        print('Aquired !')
                x = json.loads(response.text)[str(games[i]['appid'])]
                if x['success'] == True:
                    x = x['data']
                    t = games[i]
                    if x['type'] == 'game': 
                        if games[i]['price_overview'] != x['price_overview']['final']:
                            games[i]['price_overview'] = x['price_overview']['final']
                            c += 1
                            print(c)
                    else:
                        games.pop(i)
                        i -= 1
                else:
                        games.pop(i)
                        i -= 1
                i += 1
            except (Exception, BaseException) as err:
                print(games[i]['appid'])
                print(response.status_code)
                applist['applist']['apps'] = games
                gamesList.seek(0)
                json.dump(applist, gamesList)
                gamesList.truncate()
                raise err
    
    applist['applist']['apps'] = games
    gamesList.seek(0)
    json.dump(applist, gamesList)
    gamesList.truncate()
