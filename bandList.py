"""
ConcertList.py
Jim Fingal and Brian Fife, for Music Hack Day Boston ][

Take a user's last.fm data and search for upcoming concerts in their location.
"""

import urllib
import json

# fixme: hardcoded last.fm information! 
myURL='http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user=jimmytheleaf&api_key=dbc675ab62528258254f6a6164074a55&period=12month&format=json'

data = urllib.urlopen(myURL).read()
json = json.loads(data)

# higherarchy of last.fm data is:
# topartists
#   artist (list of artists)
#     name  (artist name)
#     playcount
#     mbid (musicbrainz ID)
#     url
#     streamable
#     image
#       <images by size>
#     @attr
#       rank (rank in top artist list)

artists = {}

# fixme: consider if this should be a list rather than a dict, with rank implied. 
# dict keys are listed as unicode strings, so preserving this.
for artist in json[u'topartists'][u'artist']:

    artists[artist[u'name']]= {'mbid':artist[u'mbid'], 'rank':int(artist[u'@attr']['rank'])} 

print artists

