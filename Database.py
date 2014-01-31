from google.appengine.ext import ndb

class user(ndb.Model):
    #Unfortunately, UTA is a Microsoft shop, so we can't force users to use a Gmail account. We'll have to do this manually
    email_address = ndb.StringProperty()
    password = ndb.StringProperty(indexed=False)
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    
class CADFile(ndb.Model):
    filename = ndb.StringProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)
    description = ndb.TextProperty()
    CADFile = ndb.BlobProperty()
    
#checks the validity of every username/password combo
def isValid(uname, pwd):
    return True

#returns a list of dictionaries. Each one should have a filename, upload time, description, and status
def getJobs(uname):
    return [{'name':'j1', 'status':'s1'},{'name':'j1', 'status':'s1'},{'name':'j1', 'status':'s1'},{'name':'j1', 'status':'s1'}]

#stores a file in the datastore
def storeFile(ID, encFile, filedesc):
    pass

