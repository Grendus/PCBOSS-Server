from google.appengine.ext import ndb

class user(ndb.Model):
    #Unfortunately, UTA is a Microsoft shop, so we can't force users to use a Gmail account. We'll have to do this manually
    email_address = ndb.StringProperty()
    password = ndb.StringProperty(indexed=False)
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()

    def query_user(self, username, password):
        users = self.query(email_address=username)
        if users.count()>0 and users.fetch()[0].password==password:
            return True
        return False
    
class CADFile(ndb.Model):
    submitter_name = ndb.StringProperty()
    filename = ndb.StringProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)
    description = ndb.TextProperty()
    CADFile = ndb.BlobProperty()
    
#checks the validity of every username/password combo
def isValid(uname, pwd):
    return user.query_user(uname,pwd)

#returns a list of dictionaries. Each one should have a filename, upload time, description, and status
def getJobs(uname):
    return [{'name':'j1', 'status':'s1'},{'name':'j1', 'status':'s1'},{'name':'j1', 'status':'s1'},{'name':'j1', 'status':'s1'}]

#stores a file in the datastore
def storeFile(ID, encFile, filedesc):
    pass

#adds a user to the system; should only be done by the home system
def addUser(email, encpwd, fname, lname):
    newUser = user(email_address=email,
                   password=encpwd,
                   first_name=fname,
                   last_name=lname)
    newUser.put()
