
import json
import urllib
from bandList import getTopArtistsFromID
from concertList import getConcertsByID
from setLists import getSetLists
from renderHTML import writeWebsite
from getMultimediaFromTracks import getFullData
from getUnlistenedTracks import getUnplayedTracks


if __name__ == "__main__":

    # jimmytheleaf
    # deuterium64
    # ELCatch22
    # dagdunnit
    lfmID = 'dagdunnit'      # last FM id
    numArtists = 5            # number of top artists to track
    #numArtists = 100            # number of top artists to track
    loc = 'sk:18842'            # boston
    min = '2010-10-20'          # sets date range for upcoming concerts
    max = '2011-10-20'          # sets date range for upcoming concerts
    
    # extract top artists from last.fm
    topArtists = getTopArtistsFromID(lfmID)
    
    # optionally, cut out some artists from the list
    dropKeys = []

    for artist in topArtists:
        if topArtists[artist]['rank'] > numArtists:
            dropKeys.append(artist)
            
    for key in dropKeys:
        del topArtists[key]
        
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
    
    #print bandSetlists
    #f = open("setlists.json", "r")
    #bandSetlists = json.load(f)
    #f.close()
    unplayed_tracks = getUnplayedTracks(bandSetlists)

    #print unplayed_tracks
    full_data = getFullData(unplayed_tracks)
    #print full_data

    #f = open("enhancedTracksToExplore.json", "r")
    #full_data = json.load(f)
    #f.close()

    writeWebsite(full_data)    
    
