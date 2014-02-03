from google.appengine.ext import ndb

class user(ndb.Model):
    email_address = ndb.StringProperty()
    password = ndb.StringProperty(indexed=False)
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()

    def query_user(self, username, password):
        users = self.query(user.email_address==username)
        if users.count()>0 and users.fetch()[0].password==password:
            return True
        return False
    
class CADFile(ndb.Model):
    submitter_name = ndb.StringProperty()
    filename = ndb.StringProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)
    description = ndb.TextProperty()
    CADFile = ndb.BlobProperty()
    status = ndb.StringProperty()
    
#checks the validity of every username/password combo
def isValid(uname, pwd):
    return user().query_user(uname,pwd)

#returns a list of dictionaries. Each one should have a filename, upload time, description, and status
def getJobs(uname):
    filelist = []
    users_files = CADFile.gql("WHERE submitter_name = :1", uname)
    for stored_file in users_files:
        filepoint={}
        filepoint['time'] = stored_file.time
        filepoint['name'] = stored_file.filename
        filepoint['description'] = stored_file.description
        filepoint['status'] = stored_file.status
        filelist.append(filepoint)
    return filelist

#stores a file in the datastore
def storeFile(ID, encFile, filedesc):
    uploadedFile = CADFile(submitter_name=ID,
                           filename=encFile[0]['filename'],
                           description=filedesc,
                           status="Pending")
    uploadedFile.CADFile = encFile[0]['body']
    uploadedFile.put()

#adds a user to the system; should only be done by the home system
def addUser(email, encpwd, fname, lname):
    try:
        newUser = user(email_address=email,
                       password=encpwd,
                       first_name=fname,
                       last_name=lname)
        newUser.put()
    except:
        return False
    return True
