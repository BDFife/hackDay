import urllib
import json
import elementtree.ElementTree as ET



#myURL = 'hIttp://api.songkick.com/api/3.0/events.json?apikey=musichackdayboston'
#myURL = 'http://api.songkick.com/api/3.0/artists/mbid:9e53f84d-ef44-4c16-9677-5fd4d78cbd7d/events.xml?apikey=musichackdayboston'
#myURL = 'http://api.songkick.com/api/3.0/artists/mbid:9e53f84d-ef44-4c16-9677-5fd4d78cbd7d/events.xml?apikey=musichackdayboston&max_date=2010-10-01&min_date=2009-10-01'
#myURL = 'http://api.songkick.com/api/3.0/events/4683836/setlists.json?apikey=musichackdayboston'
lastfm = 'http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user=jimmytheleaf&api_key=dbc675ab62528258254f6a6164074a55&period=12month&format=json'
#myURL = 'http://api.songkick.com/api/3.0/events/4063381/setlists.json?apikey=musichackdayboston'
songkick = 'http://api.songkick.com/api/3.0/artists/events.json?apikey=musichackdayboston&artist_name=radiohead&min_date=2009-10-01&max_date=2010-10-30'


#print data


#print "SOME DATA \n\n\n"

#print result['resultsPage']['results']['event'][0]['venue']['uri']
#print "\n\n\n"


data2 = urllib.urlopen(lastfm).read()
result2 = json.loads(data2)

foo = result2['topartists']['artist']

artists = {}
artistlist = []

for bar in foo:
	myname = bar['name']
	myid = bar['mbid']
	artists[myname] = myid;
	artistlist.append(myname);


for artist in artistlist:
	print artist

for k, v in artists.iteritems():
	print k, v


songbase = "http://api.songkick.com/api/3.0/artists/mbid:"
songend = "/events.json?apikey=musichackdayboston&min_date=2009-10-16&max_date=2010-10-16"

for k, v in artists.iteritems():
	print k, v
	uri = songbase + v + songend
	#print uri
	data = urllib.urlopen(uri).read()
	result = json.loads(data);
	r = result['resultsPage']['results']
	if r:
		r_array = r['event']
		url = r['event'][0]['venue']['uri']	
		print url
