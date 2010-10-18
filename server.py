import web
from web import form
from getNewSongs import getNewSongs

urls = (
    '/', 'index',
)

app = web.application(urls, globals())

render = web.template.render('templates/')

myUser = form.Form(
    form.Textbox('LFMID', form.notnull),
    form.Dropdown('Location', [('sk:18842', 'Boston'),]),
    )

class static:
    def GET(self):
        return render.index2()

class index:
    def GET(self):
        user = myUser
        return render.index(user)
    def POST(self):
        user = myUser
        if user.validates():
            #return "Good. I know you have values LFM: %s and Loc: %s" % (user['LFMID'].value, user['Location'].value)
            return getNewSongs(user['LFMID'].value, user['Location'].value)

if __name__ == "__main__": app.run()
