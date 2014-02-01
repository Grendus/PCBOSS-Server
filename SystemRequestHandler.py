import tornado.web
import Database

class SystemRequestHandler(tornado.web.RequestHandler):
    def post(self):
        if self.get_argument("Auth")=="PCBOSS":
            requestType = self.get_argument("type")
            if requestType == "Add User":
                email = self.get_argument("email")
                password = self.get_argument("password")
                first_name = self.get_argument("first_name")
                last_name = self.get_argument("last_name")
                if Database.addUser(email, password, first_name, last_name):
                    self.render("Success")
                else:
                    self.render("Failure")
        else:
            self.render("Error: Unrecognized Request")
            
