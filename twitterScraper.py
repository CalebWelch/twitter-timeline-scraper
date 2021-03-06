import os
import tweepy
import pandas as pd
import json


def grabTweets(api, maxId=None):
    homeTweets = api.home_timeline(since_id=maxId)
    data = []
    for t in homeTweets:
        normal = True
        if "retweeted_status" in t._json.keys():
            retweeted = True
            normal = False
        else:
            retweeted = False
        if "favorited_status" in t._json.keys():
            favorited = True
            normal = False
        else:
            favorited = False
        dictTemp = {
            "timestamp": t.created_at,
            "id": t.id,
            "user": t.user.name.encode('utf-8'),
            "retweeted": retweeted,
            "favorited": t.favorited,
            "quoted": t.is_quote_status,
            "normal": normal
        }
        data.append(dictTemp)
    data.reverse()
    return (data)


def saveData(data):
    if len(data) is not 0:
        script_path = os.path.dirname(os.path.abspath(__file__))
        df = pd.DataFrame(data)
        print (df)
        cols = df.columns.tolist()
        df = df[[
            "user", "normal", "retweeted", "quoted", "favorited", "id", "timestamp"
        ]]
        f = script_path + '\my_csv.csv'
        df.to_csv(f, float_format='{:f}'.format, header=False, mode='a')
    else:
        print('No new tweets')


def scrapeTwitter(df, api):
    try:
        idStart = df.id.iloc[-1]
    except IndexError:
        idStart = None
    saveData(grabTweets(api, idStart))


def main():
    script_path = os.path.dirname(os.path.abspath(__file__))
    keysFile = open((script_path + "\keys.txt"), "r")
    keys = keysFile.read().splitlines()
    keysFile.close()
    CONSUMER_KEY = keys[0]
    CONSUMER_SECRET = keys[1]
    ACCESS_TOKEN = keys[2]
    ACCESS_TOKEN_SECRET = keys[3]

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    df = pd.DataFrame(columns=[
            "user", "normal", "retweeted", "quoted", "favorited", "id", "timestamp"
    ])
    f = script_path + '\my_csv.csv'
    if not os.path.isfile(f):
        df.to_csv(f, float_format='{:f}'.format, header='column_names')
    else:
        df = pd.read_csv(f)
    scrapeTwitter(df, api)


if __name__ == "__main__":
     main()
