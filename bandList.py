"""
bandList.py
Jim Fingal and Brian Fife, for Music Hack Day Boston ][

Take a user's last.fm data and search for upcoming concerts in their location.
Currently hard-coded to Jim's Last.FM account.

Saves a json file bandlist.json that contains the ranked list of favourite bands.
"""

import urllib
import json

def getTopArtistsFromID(lfmID, numBands):
    """
    Grab last.FM top artists when provided with a last.fm ID. 
    
    Returns a json-friendly dictionary that contains artist name associated with 'rank' and mbID. 
    """
    
    lfmAPI = u'dbc675ab62528258254f6a6164074a55'
    period = u'12month'
    user = lfmID
    
    myURL='http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user=%s&api_key=%s&period=%s&format=json' % (user, lfmAPI, period)
    
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
    
    # fixme: there is a more elegant way to do this. 
    dropKeys = []

    # prune the list based on the user's request
    for artist in artists:
        if artists[artist]['rank'] > numBands:
            dropKeys.append(artist)
    
    for key in dropKeys:
        del artists[key]

    # here's a nice breakpoint where JSON can be exported
    return artists

if __name__ == "__main__":
    
    topArtists = getTopArtistsFromID('jimmytheleaf')
    
    f = open("bandlist2.json", "w")
    bandList = json.dump(topArtists, f, indent=4)
    f.close()

