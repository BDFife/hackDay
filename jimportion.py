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


#TODO: Get many pages
def get_tracks_from_artist(key, user, artist):
        url = userartisttracks + "&user=" + user + "&artist=" + artist + "&api_key=" + key
        print (url)
        data = urllib.urlopen(url).read()
        result = json.loads(data)
        return result

def get_7dig_track(id):
	request = urllib2.Request(sevendigtrack + id)
       	response = urllib2.urlopen(request)
       	doc = minidom.parseString(response.read())
	nodelist = doc.getElementsByTagName("track");
	results = []
	for node in nodelist:
		artist = py7digital._get_artist(node.getElementsByTagName('artist')[0])
      		album = py7digital._get_album(node.getElementsByTagName('release')[0], artist)
       		tr = py7digital._get_track(node, album, artist)
		results.append(tr)
	return results[0]

def get_7dig_album(id):
	request = urllib2.Request(sevendigrelease + id)
       	response = urllib2.urlopen(request)
       	master_node = minidom.parseString(response.read())
	results = []
        for node in master_node.getElementsByTagName('release'):
            artist = py7digital._get_artist(node.getElementsByTagName('artist')[0])
            album = py7digital._get_album(node, artist)
            results.append(album)
        return results[0]


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
	songs = song.search(title=k, artist="Radiohead", results=1, buckets=["id:7digital", "tracks"], limit="true")
	for s in songs:
        	print "%s %s %s" % (s.id, s.artist_name, s.title)
        	tracks = s.get_tracks("7digital")
        	for track in tracks:
			#print track
                	print track['preview_url']
			print track['release_image']
			foreign_id = (track['foreign_id'].split(":"))[2]
			try:
				seventr = get_7dig_track(foreign_id)
				print seventr.get_url()
				alb_id = seventr.album.get_id()
				try:
					sevenalb = get_7dig_album(alb_id)
					print sevenalb.get_url()
					print sevenalb.get_title()
					print sevenalb.get_id()
				except:
					print "failed to get back album"
			except:
				print "failed to get back album"
			




