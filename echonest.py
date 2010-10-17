from pyechonest import artist, config, song, playlist
config.ECHO_NEST_API_KEY = "LOKZT65Q6JWADXZTU"

#artists = artist.top_hottt()
#for a in artists:
 #       print "%.2f %.2f %s" % (a.get_hotttnesss(), a.get_familiarity(), a.name)


songs = song.search(title="Weird Fishes/Arpeggi", artist="Radiohead", results=1, buckets=["id:7digital", "tracks"], limit="true")
for s in songs:
        print "%s %s %s" % (s.id, s.artist_name, s.title)
	tracks = s.get_tracks("7digital")
	for track in tracks:
		print track

