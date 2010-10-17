import urllib
import json
import lastfm

lastfm = 'http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user=jimmytheleaf&api_key=dbc675ab62528258254f6a6164074a55&period=12month&format=json'

api_key = "dbc675ab62528258254f6a6164074a55"
user = "jimmytheleaf"
api = lastfm.Api(api_key)
me = api.get_user(use)
artists = me.get_top_artists
