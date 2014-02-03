import tornado.web
import WebEventHandler

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html')

class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        ID = WebEventHandler.getID(username, password)
        if ID:
            self.set_cookie("sessionID", ID)
            self.redirect("/Index")
        else:
            self.redirect("/")

class ViewHistoryHandler(tornado.web.RequestHandler):
    def get(self):
        sessionID = self.get_cookie('sessionID')
        if WebEventHandler.validateID(sessionID):
            jobList = WebEventHandler.requestJobHistory(sessionID)
            self.render("history.html", JobHistory=jobList)
        else:
            self.redirect("/")


class UploadHandler(tornado.web.RequestHandler):
    def get(self):
        if WebEventHandler.validateID(self.get_cookie('sessionID')):
            self.render('upload.html')
        else:
            self.redirect('/')

    def post(self):
        if WebEventHandler.validateID(self.get_cookie('sessionID')):
            CADFile = self.request.files["file-input"]
            filedesc = ""+self.get_argument("file-description")
            if CADFile:
                WebEventHandler.saveFile(self.get_cookie('sessionID'), CADFile, filedesc)
                self.redirect('/ViewHistory')
            else:
                self.redirect('/UploadFile')

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        sessionID = self.get_cookie('sessionID')
        if WebEventHandler.validateID(sessionID):
            self.render('index.html')
        else:
            self.redirect('/')

class AboutHandler(tornado.web.RequestHandler):
    def get(self):
        sessionID = self.get_cookie('sessionID')
        if WebEventHandler.validateID(sessionID):
            self.render('about.html')
        else:
            self.redirect('/')

class ProfileHandler(tornado.web.RequestHandler):
    def get(self):
        sessionID = self.get_cookie('sessionID')
        if WebEventHandler.validateID(sessionID):
            self.render('profile.html')
        else:
            self.redirect('/')
