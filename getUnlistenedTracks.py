import urllib, urllib2
import json
from pyechonest import artist, config

api_key = "dbc675ab62528258254f6a6164074a55"
user = "jimmytheleaf"
userartisttracks = "http://ws.audioscrobbler.com/2.0/?method=user.getartisttracks&format=json"
config.ECHO_NEST_API_KEY = "LOKZT65Q6JWADXZTU"



def get_unplayed_tracks(setlist):
	all_unplayed_tracks = []
	# TODO: Real parsing function from Brian's data
	a_hash = {}
	for k, v in setlist.iteritems():
		echo_artist = artist.Artist('musicbrainz:artist:' + k)
		a = echo_artist.name
		for t in v:
			if (a in a_hash):
				a_hash[a][t] = 1
			else:
				a_hash[a] = {t : 1}
	#print a_hash
	for k, v in a_hash.iteritems():
		#print k
		#print v
		played_tracks = get_tracks_from_artist(api_key, user, k, 0)
		#print played_tracks
		for k2, v2 in v.iteritems():
			if k2 in played_tracks:
				do_nothing = 1;
			else:
				all_unplayed_tracks.append({'artistname' : k, 'trackname' : k2})
	return all_unplayed_tracks
	


# TODO: Parse out all unique artists; map them to track names

def get_tracks_from_artist(key, user, artist, page):
	track_dict = {}
        url = userartisttracks + "&user=" + user + "&artist=" + urllib.quote(artist) + "&api_key=" + key
	if page == 0:
		pages = "666"
	while page < int(pages):
		page +=1
		newurl = url + "&page=%d" % (page)
		#print newurl
		data = urllib.urlopen(newurl).read()
        	result = json.loads(data)
		try:
			pages = result[u'artisttracks']['@attr']['totalPages']
			#print "Going through page %d of %s" % (page, pages)
			for this_t in result[u'artisttracks'][u'track']:
        			name = this_t['name']
        			if (name in track_dict):
                			track_dict[name] += 1
        			else:
                			track_dict[name] = 1
		except:
			#print "Didn't find anything by this artist"
			return track_dict
        return track_dict

if __name__ == "__main__":
	f = open("setlists.json", "r")
        setlist = json.load(f)
        f.close()
	unplayed = get_unplayed_tracks(setlist)
	f = open("unplayedTracks.json", "w")
	json.dump(unplayed, f, indent=4)
	f.close()

