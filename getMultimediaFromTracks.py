from pyechonest import artist, config, song, playlist
import urllib, urllib2
import json
import py7digital
from py7digital import Track
from xml.dom import minidom

api_key = "dbc675ab62528258254f6a6164074a55"
user = "jimmytheleaf"
config.ECHO_NEST_API_KEY = "LOKZT65Q6JWADXZTU"
sevendigtrack = "http://api.7digital.com/1.2/track/details?oauth_consumer_key=musichackday&country=US&trackid="
sevendigrelease = "http://api.7digital.com/1.2/release/details?oauth_consumer_key=musichackday&country=US&releaseid="


def getFullData(unplayed_tracks):
	full_data = []
	for trackdata in unplayed_tracks:
		artist = trackdata['artistname']
		track = trackdata['trackname']
        	#print artist, " :: ",  track
		songs = searchtracks(artist, track)
		for s in songs: # only ever one
			enhanced_data = get_track_data(s, trackdata, artist)
			full_data.append(enhanced_data)
	return full_data

			
def get_track_data(s, trackdata, artist):
	trackdata["trackid"] = s.id
	trackdata["trackname"] = s.title
	if (s.artist_name != artist):
		#print "no exact match on artist for this track :: " + s.artist_name
		return trackdata
       	tracks = s.get_tracks("7digital")
       	for track in tracks:
		trackdata['preview_url'] = track['preview_url']
		trackdata['release_image'] = track['release_image']
		foreign_id = (track['foreign_id'].split(":"))[2]
		trackdata['7digital_id'] = foreign_id
		try:
			seventr = get_7dig_track(foreign_id)
			trackdata['artist_url'] = seventr.get_url()
			alb_id = seventr.album.get_id()
			trackdata['album_id'] = alb_id
			try:
				sevenalb = get_7dig_album(alb_id)
				trackdata['album_url'] = sevenalb.get_url()
				trackdata['album_title'] = sevenalb.get_title()
				return trackdata
			except:
				#print "failed to get back album"
				return trackdata
		except:
			#print "failed to get back enhanced track info"
			return trackdata

def searchtracks(k, v):
	songs = song.search(title=v, artist=k, results=1, buckets=["id:7digital", "tracks"], limit="true")
	return songs

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


if __name__ == "__main__":
	f = open("unplayedTracks.json", "r")
	unplayed_tracks = json.load(f)
	f.close()
	full_data = getFullData(unplayed_tracks)
	f = open("enhancedTracksToExplore.json", "w")
        json.dump(full_data, f, indent=4)
        f.close()

