"""
bandList.py
Jim Fingal and Brian Fife, for Music Hack Day Boston ][

Take a user's last.fm data and search for upcoming concerts in their location.
Currently hard-coded to Jim's Last.FM account.

Saves a json file bandlist.json that contains the ranked list of favourite bands.
"""

import urllib
import json

##
## Grab Last.FM data
##

# fixme: hardcoded last.fm information! 
myURL='http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user=jimmytheleaf&api_key=dbc675ab62528258254f6a6164074a55&period=12month&format=json'

data = urllib.urlopen(myURL).read()
data = json.loads(data)

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
for artist in data[u'topartists'][u'artist']:
    artists[artist[u'name']]= {u'mbid':artist[u'mbid'], u'rank':int(artist[u'@attr']['rank'])} 

# here's a nice breakkpoint where JSON can be exported

f = open("bandlist.json", "w")
bandList = json.dump(artists, f, indent=4)
f.close()

