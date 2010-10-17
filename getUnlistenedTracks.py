from pyechonest import artist, config, song, playlist
import urllib, urllib2
import json
import py7digital
from py7digital import Track
from xml.dom import minidom

api_key = "dbc675ab62528258254f6a6164074a55"
user = "jimmytheleaf"
config.ECHO_NEST_API_KEY = "LOKZT65Q6JWADXZTU"
userartisttracks = "http://ws.audioscrobbler.com/2.0/?method=user.getartisttracks&format=json"
sevendigtrack = "http://api.7digital.com/1.2/track/details?oauth_consumer_key=musichackday&country=US&trackid="
sevendigrelease = "http://api.7digital.com/1.2/release/details?oauth_consumer_key=musichackday&country=US&releaseid="

# Test: band listened to, unlistened to track
# Band not listened to
# Band listend to, listened to track
sampledata = [ "Radiohead :: Bulletproof", "Taj Mahal :: Cakewalk Into Town", "Radiohead :: Reckoner"]


def main(somedata):
	all_unplayed_tracks = []
	# TODO: Real parsing function from Brian's data
	a_hash = {}
	print sampledata
	for s in sampledata:
		at = s.split(" :: ")
		a = at[0]
		t = at[1]
		if (a in a_hash):
			a_hash[a][t] = 1
		else:
			a_hash[a] = {t : 1}
	print a_hash
	for k, v in a_hash.iteritems():
		print k
		print v
		played_tracks = get_tracks_from_artist(api_key, user, k, 0)
		print played_tracks
		for k2, v2 in v.iteritems():
			if k2 in played_tracks:
				do_nothing = 1;
			else:
				all_unplayed_tracks.append({'artistname' : k, 'trackname' : k2})
	print all_unplayed_tracks
	f = open("unplayedTracks.json", "w")
	json.dump(all_unplayed_tracks, f, indent=4)
	f.close()

	


# TODO: Parse out all unique artists; map them to track names

def get_tracks_from_artist(key, user, artist, page):
	track_dict = {}
        url = userartisttracks + "&user=" + user + "&artist=" + urllib.quote(artist) + "&api_key=" + key
	if page == 0:
		pages = "666"
	while page < int(pages):
		page +=1
		newurl = url + "&page=%d" % (page)
		print newurl
		data = urllib.urlopen(newurl).read()
        	result = json.loads(data)
		try:
			pages = result[u'artisttracks']['@attr']['totalPages']
			print "Going through page %d of %s" % (page, pages)
			for this_t in result[u'artisttracks'][u'track']:
        			name = this_t['name']
        			if (name in track_dict):
                			track_dict[name] += 1
        			else:
                			track_dict[name] = 1
		except:
			print "Didn't find anything by this artist"
			return track_dict
        return track_dict

main("foo")
