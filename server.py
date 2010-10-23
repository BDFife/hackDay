import web
import json
import logging
from web import form
from bandList import getTopArtistsFromID
from concertList import getConcertsByID
from setLists import getSetLists
from getMultimediaFromTracks import getFullData
from getUnlistenedTracks import getUnplayedTracks

urls = (
    '/', 'index',
)

app = web.application(urls, globals())

render = web.template.render('templates/')

myUser = form.Form(
    form.Textbox('LFMID', form.notnull),
    form.Dropdown('Location', [('sk:18842', 'Boston'),]),
    )

class static:
    def GET(self):
        return render.index2()

class index:
    def GET(self):
        user = myUser
        return render.index(user)
    def POST(self):
        user = myUser


        if user.validates():

            lfmID = user['LFMID'].value
            loc = user['Location'].value
            numBands = 10
            
            logging.info("requesting response for LFM:%s loc:%s"%( str(lfmID), str(loc)))
            
            # extract list of top artists based on LFM ID. 
            logging.info("entering getTopArtists. numBands = %s" %(str(numBands)))
            topArtists = getTopArtistsFromID(lfmID, numBands)
            logging.info("exiting getTopArtists.")

            # create a ref table for MBID and band name:
            artistByID = {}
            
            for band in topArtists:
                artistByID[topArtists[band]['mbid']] = band
            
            # look for upcoming concerts in area based on top artists
            min = '2010-10-20'
            max = '2011-10-20'

            logging.info("entering getConcertsByID loop for local shows")
            upConcerts = {}
            for band in topArtists:
                upConcerts.update(getConcertsByID(topArtists[band]['mbid'], loc, min, max))
                logging.info("Looked up concerts for %s"%(band))
            logging.info("exiting getConcertsByID local loop")

            # pull out the list of bands
            upBands = []
            for band in upConcerts:
                upBands.append(upConcerts[band]['mbid'])
            # deduplicate list
            upBands = list(set(upBands))
            logging.info("list of bands prepared")

            # cross-reference against all concerts in the DB from past year.
            bandSetlists = {}
            for band in upBands:
                logging.info("getting past concerts for %s" % (band))
                bandSetlists[band] = []
                cids = getConcertsByID(band, None, '2009-10-20', '2010-10-20')
                for cid in cids.keys():
                    logging.info("searching setlist for %s" % (cid))
                    songList = getSetLists(cid, cids[cid]['mbid'])
                    if songList:
                        logging.info("setlist found for %s" %(band))
                        bandSetlists[band].extend(songList)
            
            unplayed_tracks = getUnplayedTracks(bandSetlists)
            full_data = getFullData(unplayed_tracks)

            pull_data = {}
            
            for items in full_data:
                if "preview_url" in items:
                    pull_data[items["7digital_id"]] = { 
                        'trackname':items['trackname'],
                        'preview_url':items['preview_url'],
                        'release_image':items['release_image'],
                        'artistname':items['artistname']
                        }
            
                
            
            #print full_data
            #f = open("pull_data.json", "w")
            #bandList = json.dump(pull_data, f, indent=4)
            #f.close()


            return render.response(upConcerts, pull_data)
            
if __name__ == "__main__": 
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s:%(levelname)7s: %(message)s")
    logging.info("Initializing web.py server")
    app.run()
