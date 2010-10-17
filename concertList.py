"""
concertList.py
Jim Fingal and Brian Fife, for Music Hack Day Boston ][

Imports a JSON file that contains a ranked list of bands. 

Matches this against songKick's APIs to determine if there are any upcoming concerts.

Saves a list of upcoming concerts. 
"""

import json
import urllib

# import the JSON file

f = open("bandlist.json", "r")
bands = json.load(f)
f.close()

# bands has the structure:
#   band name
#       mbid
#       rank

# fixme: hardcoding location to Boston
# fixme; hardcoding date range to October 20 2010 -> October 20 2011

myURL='http://api.songkick.com/api/3.0/artists/mbid:a96ac800-bfcb-412a-8a63-0a98df600700/events.json?apikey=musichackdayboston'

data = urllib.urlopen(myURL).read()
data = json.loads(data)

# format for this data:
#   resultsPage
#       totalEntries
#       page    (maximum 50 entries per page, navigated with &page=n)
#       results
#           event
#               type (concert, festival)
#               popularity
#               status
#               uri
#               location
#                   lat
#                   long
#                   city
#               start
#                   date
#                   time
#                   datetime
#               venue
#                   lat
#                   uri
#                   lng
#                   displayName
#                   id
#                   metroArea
#                       state
#                           displayName
#                       country
#                           displayName
#                       displayName
#                       id
#               displayName (pretty string for concert)
#               performance
#                   billingIndex
#                   billing
#                   displayName (for the band)
#                   id
#                   artist
#                       displayName
#                       identifier
#                           href
#                           mbid
#                       id
#               id

concerts = {}

# fixme: totally disregarding case where results span multiple pages.
for concert in data[u'resultsPage'][u'results'][u'event']:
    concerts[concert[u'displayName']] = {u'date':concert[u'start'][u'datetime'], 
                                         u'venue':concert[u'venue'][u'displayName'],
                                         u'id':concert[u'id'],}

print concerts