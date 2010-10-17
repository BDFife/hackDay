"""
setLists.py
Jim Fingal and Brian Fife, for Music Hack Day Boston ][

Imports a JSON file that contains a list of upcoming concerts in the area.

Matches this against songKick's APIs to determine if there are available setlists.

Saves a list of "must-know" tracks.
"""

import json
import urllib
from concertList import getConcertsByID

def getSetLists(cID, mbID):
    """
    Gets set lists, if available, based on a concert ID
    """
    
    myURL='http://api.songkick.com/api/3.0/events/%s/setlists.json?apikey=musichackdayboston' % (cID)
    data = urllib.urlopen(myURL).read()
    data = json.loads(data)
    
    songList = []
    
    if data[u'resultsPage'][u'results']:
        for setList in data[u'resultsPage'][u'results'][u'setlist']:
            # got stuck on this for a while. Array of artists.
            # fixme: look at permutations of this. multiple artists mashing into
            # a single setlist?
            # this code is likely blatantly *wrong*. It sorts out the dross, though.
            for artists in setList['artist']['identifier']:
                if artists['mbid'] == mbID:
                    # fixme: losing encore information here.
                    for songs in setList[u'setlistItem']:
                        songList.append(songs['name'])

    return songList


if __name__ == "__main__":

    f = open("concertlist.json", "r")
    concerts = json.load(f)
    f.close()
    
    bands = []
    
    for band in concerts:
        bands.append(concerts[band]['mbid'])
    
    # deduplicate the list
    bands = list(set(bands))
    
    bandSetlists = {}
    
    for band in bands:
        bandSetlists[band] = []
        cids = getConcertsByID(band, None, '2009-10-20', '2010-10-20')
        for cid in cids.keys():
            songList = getSetLists(cid, cids[cid]['mbid'])
            if songList:
                bandSetlists[band].extend(songList)
    
    f = open('setlists3.json', 'w')
    json.dump(bandSetlists, f, indent=4)
    f.close()





