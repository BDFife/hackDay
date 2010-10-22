import web
import logging
from web import form
from bandList import getTopArtistsFromID
from concertList import getConcertsByID

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
            
            min = '2010-10-20'
            max = '2011-10-20'

            # look for upcoming concerts in area based on top artists
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
            for bands in upBands:
                bandSetlists[band] = []
#                cids = 

            return render.response(upConcerts)
            
if __name__ == "__main__": 
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s:%(levelname)7s: %(message)s")
    logging.info("Initializing web.py server")
    app.run()
  
