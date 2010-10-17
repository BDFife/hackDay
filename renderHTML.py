import json

"""
[
    {
        "7digital_id": "6007080", 
        "release_image": "http://cdn.7static.com/static/img/sleeveart/00/005/426/0000542623_200.jpg", 
        "trackname": "Reckoner", 
        "album_id": "542623", 
        "trackid": "SOYOAAM12AB01841AD", 
        "preview_url": "http://previews.7digital.com/clips/34/6007080.clip.mp3", 
        "artistname": "Radiohead", 
        "artist_url": "http://us.7digital.com/artists/radiohead/?partner=722", 
        "album_url": "http://us.7digital.com/artists/global-underground/gu37-james-lavelle-bangkok/?partner=722", 
        "album_title": "GU37 James Lavelle Bangkok"
    }
]
"""

def main():
        f = open("enhancedTracksToExplore.json", "r")
	web = open("index.html", "w")
        tracks = json.load(f)
        f.close()
	web.write("<html><head><title>Foo</title></head><body>")
	web.write(str(tracks))
	web.write("</body></html>")
        web.close()


main()
