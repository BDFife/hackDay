import urllib
import json
import py7digital


api_key = "dbc675ab62528258254f6a6164074a55"
user = "jimmytheleaf"

userartisttracks = "http://ws.audioscrobbler.com/2.0/?method=user.getartisttracks&format=json"


#TODO: Get many pages
def get_tracks_from_artist(key, user, artist):
	url = userartisttracks + "&user=" + user + "&artist=" + artist + "&api_key=" + key
	print (url)
	data = urllib.urlopen(url).read()
	result = json.loads(data)
	return result

foo = get_tracks_from_artist(api_key, user, "radiohead")

pages = foo[u'artisttracks']['@attr']['totalPages']
print pages

tc = {}

for bar in foo[u'artisttracks'][u'track']:
	name = bar['name']
	if (name in tc):
		tc[name] += 1
	else:
		tc[name] = 1


