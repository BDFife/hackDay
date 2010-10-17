"""
setLists.py
Jim Fingal and Brian Fife, for Music Hack Day Boston ][

Imports a JSON file that contains a list of upcoming concerts in the area.

Matches this against songKick's APIs to determine if there are available setlists.

Saves a list of "must-know" tracks.
"""

import json
import urllib

def getConcerts(mbID):
    """
    Get a list of concerts by musicBrainzID.
    
    Takes a musicBrainzID. Currently date range is hardcoded.
    Returns a dict of concert IDs, with associated data. 
    """
    # &min_date=2010-10-20&max_date=2011-10-20
    myURL='http://api.songkick.com/api/3.0/artists/mbid:%s/events.json?apikey=musichackdayboston&min_date=2009-10-20&max_date=2010-10-20' % (mbID)
    data = urllib.urlopen(myURL).read()
    data = json.loads(data)
    
    """
     format for this data:
       resultsPage
           totalEntries
           page    (maximum 50 entries per page, navigated with &page=n)
           results
               event
                   type (concert, festival)
                   popularity
                   status
                   uri
                   location
                       lat
                       long
                       city
                   start
                       date
                       time
                       datetime
                   venue
                       lat
                       uri
                       lng
                       displayName
                       id
                       metroArea
                           state
                               displayName
                           country
                               displayName
                           displayName
                           id
                   displayName (pretty string for concert)
                   performance (may be a list of artists if a festival)
                       billingIndex
                       billing
                       displayName (for the band)
                       id
                       artist
                           displayName
                           identifier
                               href
                               mbid
                           id
                   id
    """

    concerts = {}

    # fixme: totally disregarding case where results span multiple pages.
    # no matches will return an empty results set.
    if data[u'resultsPage'][u'results']:
        for concert in data[u'resultsPage'][u'results'][u'event']:
            # not extracting mbID from the returned JSON, because performance is 
            # a list which can contain a number of artists, if a festival, etc.
            concerts[concert[u'id']] = {u'date':concert[u'start'][u'date'], 
                                        u'venue':concert[u'venue'][u'displayName'],
                                        u'name':concert[u'displayName'],
                                        u'mbid':mbID}
                                        

    return concerts


def getSetLists(cID, mbID):
    """
    Gets set lists, if available, based on a concert ID
    """
    
    myURL='http://api.songkick.com/api/3.0/events/%s/setlists.json?apikey=musichackdayboston' % (cID)
    data = urllib.urlopen(myURL).read()
    data = json.loads(data)
    
    setList = {}

#########
# stopping for the evening. getting sloppy. 
# suggest to d/l a single ID with lyrics and parse through that example first. 
# I'm getting tangled in the lyric JSON syntax. 
#########
    
    if data[u'resultsPage'][u'results']:
        for setList in data[u'resultsPage'][u'results'][u'setlist']:
            if setList['artist']['identifier']['href'] == mbID:
                print setList
            else:
                print "!!!***!!!rejected"
           
    
#        print json.dumps(data, indent=4)


f = open("concertlist.json", "r")
concerts = json.load(f)
f.close()

bands = []

for band in concerts:
    bands.append(concerts[band]['mbid'])

# deduplicate the list
bands = list(set(bands))

for band in bands:
    cids = getConcerts(band)
    for cid in cids.keys():
        getSetLists(cid, cids[cid]['mbid'])

#print bands

# scan the bands' past 12 months activity for concerts with setlists. 


