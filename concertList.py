"""
concertList.py
Jim Fingal and Brian Fife, for Music Hack Day Boston ][

Imports a JSON file that contains a ranked list of bands. 

Matches this against songKick's APIs to determine if there are any upcoming concerts.

Saves a list of upcoming concerts. 
"""

import json
import urllib


def getConcertsByID(mbID, loc, min, max):
    """
    Get a list of concerts by musicBrainzID.
    
    Takes a musicBrainzID. SongKick location ID, min-date and max-date.
    Returns a dict of concert IDs, with associated data. 
    """
    
    skID = 'musichackdayboston'

    myURL='http://api.songkick.com/api/3.0/artists/mbid:%s/events.json?apikey=%s&location=%s&min_date=%s&max_date=%s' % (mbID, skID, loc, min, max )
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



if __name__ == "__main__":
    
    # import the band list file
    f = open("bandlist.json", "r")
    bands = json.load(f)
    f.close()

    """
    bands has the structure:
        band name
            mbid
            rank
    """
    allConcerts = {}

    loc = 'sk:18842'
    min = '2010-10-20'
    max = '2011-10-20'

    for band in bands:
        allConcerts.update(getConcertsByID(bands[band]['mbid'], loc, min, max))

    f = open("concertlist2.json", "w")
    json.dump(allConcerts, f, indent=4)
    f.close()


