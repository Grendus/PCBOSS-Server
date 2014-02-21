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

    def export(self):
        data = {"submitter_name":self.submitter_name,
                "filename":self.filename,
                "key":str(self.key.id()),
                "time":self.time.strftime("%Y %m %d %H:%M:%S"),
                "description":self.description,
                "CADFile":self.CADFile,
                "status":self.status}
        return data
    
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

def getUserInfo(uname):
    userData = user.gql("WHERE email_address = :1", uname).get()
    userDict = {"email":userData.email_address,
                "fname":userData.first_name,
                "lname":userData.last_name}
    return userDict

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

def updateAccount(email, fname, lname, pword=False):
    selectedUser = user.gql("WHERE email_address = :1", email).get()
    if pword:
        selectedUser.password = pword
    selectedUser.first_name = fname
    selectedUser.last_name = lname
    selectedUser.put()

def listJobs():
    jobs = CADFile.gql('')
    joblist = []
    for job in jobs:
        jobdict = job.export()
        del jobdict["CADFile"]
        joblist.append(jobdict)
    return joblist

def getJob(filenum):
    #todo: fix the GQL injection vulnerability here. Probably safe, it's behind an authorization wall, but still bad form to leave it there
    job = CADFile.gql("WHERE __key__ = KEY('CADFile', "+str(filenum)+")").get()
    return job.export()

def updateStatus(filenum, status):
    job = getJob(filenum)
    job.status = status
    job.put()

def mostRecentFile():
    job = CADFile.gql("ORDER BY time DESC LIMIT 1").get()
    return job.export()

def mostRecentTimestamp():
    return mostRecentFile()["time"]

def listUsers():
    users = user.gql("")
    userlist = []
    for userinfo in users:
        userlist.append((userinfo.email_address, userinfo.first_name, userinfo.last_name))
    return userlist
