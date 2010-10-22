
import json
import urllib
from bandList import getTopArtistsFromID
from concertList import getConcertsByID
from setLists import getSetLists
from renderHTML import writeWebsite
from getMultimediaFromTracks import getFullData
from getUnlistenedTracks import getUnplayedTracks


def getNewSongs(lfmID, loc):
    # jimmytheleaf
    # deuterium64
    # ELCatch22
    # dagdunnit
    #lfmID = 'dagdunnit'      # last FM id
    numArtists = 5            # number of top artists to track
    #numArtists = 100            # number of top artists to track
    #loc = 'sk:18842'            # boston
    min = '2010-10-20'          # sets date range for upcoming concerts
    max = '2011-10-20'          # sets date range for upcoming concerts
    
    # extract top artists from last.fm
    topArtists = getTopArtistsFromID(lfmID, numArtists)
    
    #print topArtists
    
    # pull upcoming concerts from songkick
    
    upConcerts = {}

    for band in topArtists:
        upConcerts.update(getConcertsByID(topArtists[band]['mbid'], loc, min, max))

    # todo: extract concert URLS here. 
    #print upConcerts
    upBands = []
    
    # compress upConcerts to a list of bands playing in Boston in the future
    for band in upConcerts:
        upBands.append(upConcerts[band]['mbid'])
    
    # deduplicate the list
    upBands = list(set(upBands))
    
    # cross-reference against all concerts in the songkick database
    
    bandSetlists = {}
    
    for band in upBands:
        bandSetlists[band] = []
        cids = getConcertsByID(band, None, '2009-10-20', '2010-10-20')
        for cid in cids.keys():
            songList = getSetLists(cid, cids[cid]['mbid'])
            if songList:
                bandSetlists[band].extend(songList)
    
    unplayed_tracks = getUnplayedTracks(bandSetlists)

    #print unplayed_tracks
    full_data = getFullData(unplayed_tracks)
    #print full_data

    # todo: take full_data and manipulate this around.
    # structure it so a table may be generated elegantly and iterated out. 

    return writeWebsite(full_data, upConcerts)    
    

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s:%(levelname)7s: %(message)s")
    logging.info("Initializing getNewSongs standalone")
    getNewSongs('dagdunnit', 'sk:18842')
