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


for k, v in tc.iteritems():
	print k, " :: ",  v
	searcher = py7digital.search_track("radiohead " + k)
	print searcher.get_total_result_count()
	while searcher.has_results():
    		for track in searcher.get_next_page():
        		print track, track.get_id(), track.get_url(), track.get_audio()

