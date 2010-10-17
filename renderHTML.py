import json
import codecs


def writeWebsite(tracks, upconcerts = {}):
    web = []
    web.append("<html><head><title>Music You should Listen To</title></head><body>\n")
    if (upconcerts):
        web.append("\t<h1>Your Upcoming shows are:</h1>\n");
        web.append("\t<center><table border='1' width='500'>\n");
        web.append("\t<tr><th>Show</th><th>Venue</th><th>Date</th></tr>\n");
        for k, v in upconcerts.iteritems():
            web.append("<tr>")
            web.append("<td>" + v['name'] + "</td>")
            web.append("<td>" + v['venue'] + "</td>")
            web.append("<td>" + v['date'] + "</td>")
            web.append("</tr>")
        web.append("\t</center></table>\n");
    web.append("\t<h1>Based on your last.fm listens and upcoming shows in your area, you should listen to:</h1>\n");
    web.append("\t<center><table border='1' width='950'>\n");
    for data in tracks:
        release_image = ''
        artist_url = ''
        artistname = ''
        album_url = ''
        album_title = ''
        preview_url = ''
        trackname = ''
        if "preview_url" in data:
            preview_url = data['preview_url']   
        if (preview_url):
            if "release_image" in data:
                release_image = data['release_image']   
            if "artist_url" in data:
                artist_url = data['artist_url'] 
            if "artistname" in data:
                artistname = data['artistname'] 
            if "album_url" in data:
                album_url = data['album_url']   
            if "album_title" in data:
                album_title = data['album_title']   
            if "trackname" in data:
                trackname = data['trackname']   
            web.append("\t\t<tr>\n")
            web.append("\t\t<td>")
            if (album_url): 
                web.append("<a href='" + album_url + "'>")
            web.append("<img src='" + release_image  + "'>")
            if (album_url): 
                web.append("</a>")
            web.append("</td>\n")
            web.append("\t\t<td>")
            if (artist_url): 
                web.append("<a href='" + artist_url + "'>")
            web.append(artistname  + " : " + trackname)
            if (artist_url): 
                web.append("</a>")
            web.append("</td>\n")
            web.append("\t\t<td>" + get_google_player(preview_url)  + "</td>\n")
            web.append("\t</tr>")
    web.append("\t</center></table>\n");
    web.append("</body></html>")
#        web.close()
    return web

def get_google_player(url):
    first = "<embed type='application/x-shockwave-flash' src='http://www.google.com/reader/ui/3523697345-audio-player.swf' flashvars='audioUrl="
    second= "' width='400' height='27' quality='best'></embed>"
    return first + url + second;


if __name__ == "__main__":
        f = open("enhancedTracksToExplore.json", "r")
        tracks = json.load(f)
        f.close()
        f = open("concertlist.json", "r")
        concerts = json.load(f)
        f.close()
        writeWebsite(tracks, concerts)

